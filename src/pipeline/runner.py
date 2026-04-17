# ./src/pipeline/runner.py

"""
Pipeline Runner

This module contains the PipelineRunner class which is responsible for\
executing the scraping pipeline in a safe and structured manner. It\
orchestrates the entire workflow from loading URLs to saving results and\
reporting metrics.

Key Responsibilities:
    - Loads URLs from the input file
    - Processes URLs using the orchestrator
    - Saves results to the output file
    - Reports metrics after successful processing
    - Provides a safe execution layer with exception handling

Methods:
    run: Main pipeline execution method
    _safe: Safe wrapper for synchronous operations
    _safe_async: Safe wrapper for asynchronous operations
"""

from .deps import (
    Optional,
    settings,
    URLs,
    URLInputLoader,
    ResultManager,
    ScrapeResults,
    MetricsReporter,
    AppLogger,
)
from .orchestrator import PipelineOrchestrator

INPUT_FILE = settings.urls_file
OUTPUT_FILE = settings.output_csv_file

logger: AppLogger = AppLogger("PipelineRunner")


class PipelineRunner:
    """
    This class is responsible for executing the scraping pipeline in a safe and
    structured manner. It orchestrates the entire workflow from loading URLs to
    saving results and reporting metrics.

    Key Responsibilities:
        - Loads URLs from the input file
        - Processes URLs using the orchestrator
        - Saves results to the output file
        - Reports metrics after successful processing
        - Provides a safe execution layer with exception handling

    Attributes:
        loader: Handles loading URLs
        saver: Handles saving results
        reporter: Handles reporting metrics
        orchestrator: Orchestrates the scraping process
        urls: Loaded URLs to process
        results: Accumulated scrape results

    Methods:
        run: Main pipeline execution method
        _safe: Safe wrapper for synchronous operations
        _safe_async: Safe wrapper for asynchronous operations
        __init__: Initialize the pipeline runner

    Returns:
        None

    Usage:
        import asyncio
        from pipeline import PipelineRunner

        runner = PipelineRunner()
        asyncio.run(runner.run())
    """

    def __init__(self,
                 loader: Optional[URLInputLoader] = None,
                 saver: Optional[ResultManager] = None,
                 reporter: Optional[MetricsReporter] = None,
                 orchestrator: Optional[PipelineOrchestrator] = None
                 ):
        """
        Initialize the pipeline runner.

        This method sets up the pipeline runner with optional dependency
        injection for the loader, saver, reporter, and orchestrator components.
        If any components are not provided, default instances will be created.

        Args:
            loader: Optional URL input loader
            saver: Optional results manager
            reporter: Optional metrics reporter
            orchestrator: Optional pipeline orchestrator

        Returns:
            None
        """
        self.urls: Optional[URLs] = None
        self.results: ScrapeResults = ScrapeResults()

        # dependency injection
        self.loader = loader or URLInputLoader(INPUT_FILE)
        self.saver = saver or ResultManager(OUTPUT_FILE)
        self.reporter = reporter or MetricsReporter()
        self.orchestrator = orchestrator or PipelineOrchestrator()

    # ===== PIPELINE EXECUTION =====

    async def run(self) -> None:
        """
        Execute the entire scraping pipeline.

        This method orchestrates the complete scraping workflow:
            1. Loads URLs from the input file
            2. Processes URLs using the orchestrator
            3. Saves results to the output file
            4. Reports metrics after successful processing
        Each step is wrapped in a safe execution layer to handle exceptions
        gracefully.

        Returns:
            None
        """
        self.urls = self._safe(self._load_urls)
        if not self.urls:
            logger.pipeline.no_urls()
            return

        self.results = await self._safe_async(self._process, self.urls)
        if not self.results:
            logger.pipeline.no_results()
            return

        self._safe(self._save, self.results)
        self._safe(self._report_metrics, self.results)

    # ===== PIPELINE STEPS =====

    def _load_urls(self) -> Optional[URLs]:
        """
        Load URLs using the URL input loader.

        This method delegates URL loading to the configured input loader,
        providing a standardized way to fetch URLs for processing.

        Returns:
            Optional[URLs]: List of URLs if successful, None otherwise
        """
        return self.loader.get_urls()

    async def _process(self, urls: URLs) -> ScrapeResults:
        """
        Process URLs using the orchestrator.

        This method delegates the entire scraping workflow to the pipeline
        orchestrator, which handles concurrent processing with browser
        fallback.

        Args:
            urls: List of URL objects to process

        Returns:
            ScrapeResults: Aggregated results from all URL processing
        """
        return await self.orchestrator.process_pipeline(urls)

    def _save(self, results: ScrapeResults) -> None:
        """
        Save scrape results using the result manager.

        This method delegates result saving to the configured result manager,
        persisting the scraped data to the output location.

        Args:
            results: Scrape results to save

        Returns:
            None
        """
        self.saver.save_all(results)

    def _report_metrics(self, results: ScrapeResults) -> None:
        """
        Report metrics using the metrics reporter.

        This method delegates metric reporting to the configured metrics
        reporter, providing insights into the scraping operation's performance.

        Args:
            results: Scrape results containing metrics data

        Returns:
            None
        """
        self.reporter.report(results)

    # ===== SAFE EXECUTION LAYER =====

    def _safe(self, fn, *args, default=None):
        """
        Safe wrapper for synchronous operations.

        This method executes a synchronous function with exception handling,
        returning a default value if an error occurs.

        Args:
            fn: Synchronous function to execute
            *args: Positional arguments for the function
            default: Default value to return if an exception occurs

        Returns:
            Result of the function or the default value if an exception occurs
        """
        try:
            return fn(*args)
        except Exception as e:
            logger.pipeline.exception(e)
            return default

    async def _safe_async(self, fn, *args, default=None):
        """
        Safe wrapper for asynchronous operations.

        This method executes an asynchronous function with exception handling,
        returning a default value if an error occurs.

        Args:
            fn: Asynchronous function to execute
            *args: Positional arguments for the function
            default: Default value to return if an exception occurs

        Returns:
            Result of the function or the default value if an exception occurs
        """
        try:
            return await fn(*args)
        except Exception as e:
            logger.pipeline.exception(e)
            results = ScrapeResults()
            if default is not None:
                results = default
            return results
