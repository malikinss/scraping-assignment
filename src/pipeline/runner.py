# ./src/pipeline/runner.py

from .deps import (
    Optional,
    settings,
    URLs,
    URLInputLoader,
    ResultManager,
    ScrapeResults,
    MetricsReporter,
    Logger,
)
from .orchestrator import PipelineOrchestrator

logger = Logger("PipelineRunner")


class PipelineRunner:
    """
    Runner for executing the end-to-end scraping pipeline.

    This class orchestrates the entire scraping workflow:
        - Loading URLs from input
        - Processing URLs via PipelineOrchestrator
        - Saving results to CSV, JSON, and error logs
        - Calculating and displaying metrics

    Attributes:
        urls (Optional[URLs]): List of URLs loaded from input file.
        results (ScrapeResults): List of scrape results after processing.
    """

    def __init__(self):
        """
        Initialize the pipeline runner with empty URL and result containers.
        """
        self.urls: Optional[URLs] = None
        self.results: ScrapeResults = []

    async def run(self) -> None:
        """
        Execute the entire scraping pipeline.

        This method orchestrates the complete workflow:
            1. Loads URLs from input file
            2. Processes URLs using the pipeline orchestrator
            3. Saves results to output files
            4. Calculates and displays metrics

        Returns:
            None
        """
        self.urls = self._load_urls()
        if not self.urls:
            logger.warning("No URLs found. Pipeline terminated.")
            return

        self.results = await self._process(self.urls)
        self._save(self.results)
        self._report_metrics(self.results)

    # ===== PIPELINE STEPS =====

    def _load_urls(self) -> Optional[URLs]:
        """
        Load URLs from the input file using URLInputLoader.

        Returns:
            Optional[URLs]: List of URLs if loading is successful,
                            None otherwise.

        Notes:
            - Uses `URLInputLoader` to handle the loading process.
        """
        loader = URLInputLoader(settings.urls_file)
        return loader.get_urls()

    async def _process(self, urls: URLs) -> ScrapeResults:
        """
        Process the list of URLs using the pipeline orchestrator.

        Args:
            urls (URLs): List of URLs to process.

        Returns:
            ScrapeResults: Results from the scraping process.

        Notes:
            - Uses `PipelineOrchestrator` to handle the scraping workflow.
        """
        orchestrator = PipelineOrchestrator()
        return await orchestrator.process_pipeline(urls)

    def _save(self, results: ScrapeResults) -> None:
        """
        Save scrape results to CSV, JSON, and error log files.

        Args:
            results (ScrapeResults): List of scrape results to save.

        Notes:
            - Uses `ResultManager` to handle multiple save formats.
        """
        logger.separator()
        saver = ResultManager(
            settings.output_csv_file,
            settings.output_json_file,
            settings.output_error_file,
        )
        saver.save_all(results, only_csv=True)

    def _report_metrics(self, results: ScrapeResults) -> None:
        """
        Report metrics for the scrape results.

        Args:
            results (ScrapeResults): List of scrape results to analyze.

        Notes:
            - Uses `MetricsReporter` to handle the metrics reporting process.
        """
        logger.separator()
        reporter = MetricsReporter()
        reporter.report(results)
