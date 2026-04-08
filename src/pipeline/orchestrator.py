# ./src/pipeline/orchestrator.py

from src.services import MetricsAggregator
from .deps import (
    asyncio,
    List,
    URLUtils,
    URL,
    URLs,
    ScrapeResult,
    ScrapeResults,
    ScrapeStatus,
    HTTPScraper,
    BrowserScraper,
    settings,
    Logger
)

logger = Logger("PipelineOrchestrator")


class PipelineOrchestrator:
    """
    Orchestrates concurrent scraping with HTTP and browser fallback.

    This class manages the full scraping pipeline:
        - Executes concurrent HTTP requests using `HTTPScraper`
        - Applies fallback to `BrowserScraper` for non-success cases
        - Normalizes results and aggregates metrics

    Designed to balance performance (HTTP) and reliability (browser fallback).

    Attributes:
        http_scraper (HTTPScraper): HTTP-based scraper for fast requests.
        browser_scraper (BrowserScraper): Browser-based scraper for complex
                                          pages.
    """

    def __init__(self):
        """
        Initializes the PipelineOrchestrator with HTTP and browser scrapers.
        """
        self.http_scraper = HTTPScraper()
        self.browser_scraper = BrowserScraper()

    # ===== LIFECYCLE =====

    async def launch(self):
        """
        Launch necessary resources for the browser scraper.

        This must be called before fetching any URLs that may require browser
        rendering.
        """
        await self.browser_scraper.launch()

    async def close(self):
        """
        Closes the browser and cleans up resources.

        This should be called after all scraping tasks are completed to free
        memory and resources.
        """
        await self.browser_scraper.close_browser()

    # ===== PIPELINE =====

    async def process_pipeline(self, urls: URLs) -> ScrapeResults:
        """
        Execute the full scraping pipeline.

        Handles lifecycle (launch/close), concurrency execution,
        and summary logging.

        Args:
            urls (URLs): Collection of URLs to scrape.

        Returns:
            ScrapeResults: Normalized list of scraping results.
        """
        if not urls:
            return ScrapeResults()

        total_urls = len(urls)
        await self.launch()

        logger.separator()
        logger.info(
            f"Pipeline started: total={total_urls} "
            f"concurrency={settings.max_concurrency}"
        )

        try:
            results = await self.run(urls)
            self._log_summary(results, total_urls)
            return results
        finally:
            await self.close()

    # ===== CORE LOGIC =====

    async def run(self, urls: URLs) -> ScrapeResults:
        """
        Run scraping tasks with concurrency control.

        Uses asyncio semaphore to limit concurrent requests and
        gathers results safely.

        Args:
            urls (URLs): Collection of URLs to scrape.

        Returns:
            ScrapeResults: Normalized scraping results.
        """
        concurrency = min(settings.max_concurrency, len(urls))
        semaphore = asyncio.Semaphore(concurrency)

        async def worker(id: int, url: URL) -> ScrapeResult:
            async with semaphore:
                return await self.process_url(id, url)

        tasks: List[asyncio.Task[ScrapeResult]] = [
            asyncio.create_task(worker(idx, url))
            for idx, url in enumerate(urls, start=1)
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        return self._normalize_results(results)

    async def process_url(self, id: int, url: URL) -> ScrapeResult:
        """
        Process a single URL with HTTP + fallback strategy.

        Workflow:
            1. Attempt HTTP scraping
            2. If result is non-success → fallback to browser

        Args:
            id (int): Unique identifier of the request.
            url (URL): Target URL.

        Returns:
            ScrapeResult: Final scraping result.
        """
        short_url = URLUtils.short_url(url)

        # 1. HTTPX attempt
        result = await self.http_scraper.fetch(id, url)

        # 2. fallback decision
        if self._should_use_browser(result):
            logger.info(
                f"[ID: {id}][FALLBACK_BROWSER] "
                f"url={short_url} reason={result.status}"
            )

            result = await self.browser_scraper.fetch(id, url)
        return result

    # ===== HELPERS =====

    def _should_use_browser(self, result: ScrapeResult) -> bool:
        """
        Determine whether browser fallback is required.

        Args:
            result (ScrapeResult): Result from HTTP scraping.

        Returns:
            bool: True if fallback should be triggered.
        """
        return result.status in ScrapeStatus.non_success_statuses()

    def _normalize_results(
        self, results: List[ScrapeResult | Exception]
    ) -> ScrapeResults:
        """
        Convert exceptions into standardized failed results.

        Ensures that the pipeline always returns valid `ScrapeResult`
        objects, even when unexpected exceptions occur.

        Args:
            results (List[ScrapeResult | Exception]): Raw results from tasks.

        Returns:
            ScrapeResults: Normalized result collection.
        """
        normalized = []

        for r in results:
            if isinstance(r, Exception):
                logger.exception(f"Unhandled exception: {r}")
                normalized.append(
                    ScrapeResult(
                        id=getattr(r, "id", 0),
                        url=getattr(r, "url", "unknown"),
                        method=getattr(r, "method", None),
                        status=ScrapeStatus.FAILED,
                        latency=0,
                        content_length=0,
                        error=str(r),
                    )
                )
            else:
                normalized.append(r)
        return ScrapeResults(normalized)

    def _log_summary(self, results: ScrapeResults, total: int) -> None:
        """
        Log aggregated pipeline statistics.

        Args:
            results (ScrapeResults): Final scraping results.
            total (int): Total number of processed URLs.
        """
        stats = MetricsAggregator.group_by_status(results)

        logger.info(
            "Pipeline completed: "
            f"total={total} "
            f"success={stats.get(ScrapeStatus.SUCCESS, 0)} "
            f"failed={stats.get(ScrapeStatus.FAILED, 0)} "
            f"timeout={stats.get(ScrapeStatus.TIMEOUT, 0)} "
            f"blocked={stats.get(ScrapeStatus.BLOCKED, 0)} "
            f"empty={stats.get(ScrapeStatus.EMPTY, 0)} "
            f"captcha={stats.get(ScrapeStatus.CAPTCHA, 0)}"
        )
