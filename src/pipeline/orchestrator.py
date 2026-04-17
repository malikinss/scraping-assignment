# ./src/pipeline/orchestrator.py

"""
Pipeline Orchestrator Module

This module implements the PipelineOrchestrator class, which serves as the
central coordinator for the scraping pipeline.

It manages the entire scraping workflow, from launching and closing
the browser to processing URLs with both HTTPX and Playwright scrapers.

Core Components:
    - PipelineOrchestrator: Main orchestrator class that orchestrates
        the scraping process.
    - HTTPScraper: Fast HTTP-based scraper for initial attempts.
    - BrowserScraper: Browser-based scraper for fallback scenarios.

Key Responsibilities:
    - Pipeline lifecycle management (launch/close browser)
    - Concurrency control via asyncio.Semaphore
    - Two-stage scraping strategy (HTTPX -> Browser fallback)
    - Result normalization and aggregation
    - Error handling and reporting

Typical Workflow:
    1. PipelineOrchestrator.launch() - Initialize browser
    2. PipelineOrchestrator.run() - Process URLs with concurrency control
    3. PipelineOrchestrator.process_url() - Single URL processing
    4. PipelineOrchestrator.close() - Clean up resources

Design:
    The orchestrator implements a "fast-first" strategy:
    - HTTPX scraper is used for initial requests (fast, low-resource)
    - Browser scraper is used only when needed (fallback for JS-heavy sites)
    - Concurrency is limited to settings.max_concurrency
    - All results are normalized into ScrapeResult objects

Error Handling:
    - Exceptions are caught and converted to failed results
    - Errors from both scraper attempts are merged
    - Pipeline ensures cleanup even when errors occur
"""

from .deps import (
    asyncio,
    List,
    URL,
    URLs,
    ScrapeResult,
    ScrapeResults,
    ScrapeMethod,
    ScrapeStatus,
    HTTPScraper,
    BrowserScraper,
    settings,
    AppLogger,
    Callable,
    Awaitable,
    Counts
)

logger: AppLogger = AppLogger("PipelineOrchestrator")

Task = asyncio.Task[ScrapeResult]
Tasks = List[Task]
Worker = Callable[[int, URL], Awaitable[ScrapeResult]]


class PipelineOrchestrator:
    """
    Orchestrates the entire scraping pipeline.

    This class acts as the central coordinator for the scraping process,
    managing the flow of URL processing from HTTP scraping to browser-based
    fallback.

    Key Responsibilities:
        - Manages lifecycle: launching and closing browser
        - Processes URLs with HTTPX scraper and browser fallback
        - Enforces concurrency limits via semaphore
        - Normalizes and aggregates results
        - Integrates with logging and metrics reporting

    Design:
        - Implements a two-stage scraping strategy:
            1. HTTPX (fast, low-resource) for initial attempt
            2. Playwright (slower, resource-intensive) for fallback
        - Uses asyncio.Semaphore to control concurrency
        - Aggregates results and handles exceptions gracefully

    Usage:
        orchestrator = PipelineOrchestrator()
        await orchestrator.process_pipeline(urls)
    """

    def __init__(self):
        """
        Initialize the pipeline orchestrator with HTTP and browser scrapers.

        This method sets up the two core scraping components that will be used
        to process URLs: the fast HTTPX-based scraper and the slower but more
        capable browser-based scraper.

        Returns:
            None
        """
        self.http_scraper = HTTPScraper()
        self.browser_scraper = BrowserScraper()

    # ===== LIFECYCLE =====

    async def launch(self):
        """
        Launch the browser scraper before starting pipeline.

        This method initializes the browser instance(s) required for browser-
        based scraping operations. It should be called before processing
        any URLs to ensure the browser is ready when needed for fallback
        scraping.

        Returns:
            None
        """
        await self.browser_scraper.launch()

    async def close(self):
        """
        Close the browser scraper after pipeline completes.

        This method releases browser resources and should be called after all
        scraping operations have finished. It ensures a clean shutdown and
        prevents resource leaks.

        Returns:
            None
        """
        await self.browser_scraper.close_browser()

    # ===== PIPELINE =====

    async def process_pipeline(self, urls: URLs) -> ScrapeResults:
        """
        Process all URLs through the scraping pipeline.

        This method orchestrates the complete scraping workflow for a list of
        URLs:
            1. Validates that URLs are provided
            2. Launches the browser scraper
            3. Logs pipeline start with concurrency information
            4. Runs the core scraping logic
            5. Logs pipeline summary statistics
            6. Closes the browser scraper

        The pipeline runs concurrently up to the configured max_concurrency
        level.
        Exceptions during processing are caught and normalized into results.

        Args:
            urls: List of URL objects to process

        Returns:
            ScrapeResults: Aggregated results from all URL processing
        """
        if not urls:
            return ScrapeResults()

        total_urls = len(urls)
        await self.launch()

        logger.pipeline.start(total_urls, settings.max_concurrency)

        try:
            results = await self.run(urls)
            stats: Counts = results.count_by_status()
            logger.pipeline.summary(stats)
            return results
        finally:
            await self.close()

    # ===== CORE LOGIC =====

    async def run(self, urls: URLs) -> ScrapeResults:
        """
        Execute the scraping workflow with concurrency control.

        This method manages the parallel processing of URLs using a semaphore
        to limit the number of concurrent operations to the configured maximum.

        Args:
            urls: List of URL objects to process

        Returns:
            ScrapeResults: Aggregated results from all URL processing
        """
        concurrency = min(settings.max_concurrency, len(urls))
        semaphore = asyncio.Semaphore(concurrency)

        async def worker(id: int, url: URL) -> ScrapeResult:
            async with semaphore:
                return await self.process_url(id, url)

        results = await asyncio.gather(
            *self._build_tasks(urls, worker),
            return_exceptions=True
        )

        return self._normalize_results(results)

    async def process_url(self, id: int, url: URL) -> ScrapeResult:
        """
        Scrape a single URL with fallback mechanism.

        This method first attempts to scrape the URL using the fast HTTPX
        scraper. If the result indicates a failure that could be handled by
        the browser (e.g., network errors, JavaScript rendering requirements),
        it falls back to using the browser-based scraper. Errors from both
        attempts are combined for comprehensive error reporting.

        Args:
            id: The ID of the URL being processed
            url: The URL object to scrape

        Returns:
            ScrapeResult: The result of the scraping operation (HTTPX or
            browser)
        """
        # 1. HTTPX attempt
        result = await self.http_scraper.fetch(id, url)

        # 2. fallback decision
        if self._should_use_browser(result):
            logger.pipeline.fallback(id, url, result.status)
            browser_result = await self.browser_scraper.fetch(id, url)
            if not browser_result.error:
                result = browser_result
            else:
                # combine errors
                browser_result.error = self._merge_errors(
                    result.error, browser_result.error
                )
                result = browser_result

        return result

    # ===== HELPERS =====

    def _build_task(self, id: int, url: URL, worker: Worker) -> Task:
        """
        Build and return a new asyncio Task for a worker.

        This helper wraps the worker coroutine in an asyncio Task, allowing
        it to be scheduled and run concurrently with other tasks.

        Args:
            id: The ID of the URL being processed
            url: The URL object to process
            worker: The worker coroutine to execute

        Returns:
            Task: The created asyncio Task
        """
        return asyncio.create_task(worker(id, url))

    def _build_tasks(self, urls: URLs, worker: Worker) -> Tasks:
        """
        Build a list of Tasks for all URLs.

        Creates a Task for each URL using the provided worker coroutine, with
        unique IDs assigned based on the URL's position in the list.

        Args:
            urls: List of URL objects to process
            worker: The worker coroutine to use for each URL

        Returns:
            Tasks: List of asyncio Tasks ready for execution
        """
        return [
            self._build_task(idx, url, worker)
            for idx, url in enumerate(urls, start=1)
        ]

    def _should_use_browser(self, result: ScrapeResult) -> bool:
        """
        Determine whether to use the browser scraper for fallback.

        Checks if the result indicates a failure that might be resolvable with
        browser-based scraping (e.g., network errors, JS rendering issues).

        Args:
            result: The result from the initial HTTPX scrape attempt

        Returns:
            bool: True if browser fallback should be used, False otherwise
        """
        return result.is_failure

    def _merge_errors(self, *errors: str | None) -> str:
        """
        Merge multiple error messages into a single string.

        Filters out None values and joins the error strings with a separator.

        Args:
            *errors: Variable number of error strings (can be None)

        Returns:
            str: Combined error string
        """
        return " | ".join(e for e in errors if e)

    def _normalize_results(
        self, results: List[ScrapeResult | Exception]
    ) -> ScrapeResults:
        """
        Normalize and aggregate scraping results.

        Converts raw results (which may include exceptions) into structured
        ScrapeResult objects, handling exceptions gracefully and logging them.

        Args:
            results: List of ScrapeResult objects or exceptions from scraping

        Returns:
            ScrapeResults: Aggregated and normalized results
        """
        return ScrapeResults(
            self._normalize_result(r) for r in results
        )

    def _normalize_result(
        self, result: ScrapeResult | Exception
    ) -> ScrapeResult:
        """
        Normalize a single result or exception into a ScrapeResult object.

        If the input is already a ScrapeResult, it's returned as-is. If it's an
        Exception, it's converted into a failed ScrapeResult with appropriate
        metadata.

        Args:
            result: A ScrapeResult object or an Exception

        Returns:
            ScrapeResult: Normalized result
        """
        normalized: ScrapeResult = result
        if isinstance(result, Exception):
            logger.pipeline.exception(result)
            normalized = ScrapeResult(
                id=getattr(result, "id", 0),
                url=getattr(result, "url", "unknown"),
                method=getattr(result, "method", ScrapeMethod.HTTPX),
                status=ScrapeStatus.FAILED,
                latency=0,
                content_length=0,
                error=str(result),
            )
        return normalized
