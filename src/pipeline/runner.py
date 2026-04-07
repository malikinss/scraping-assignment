# ./src/pipeline/runner.py

from .deps import (
    Optional,
    settings,
    URLs,
    URLInputLoader,
    ResultManager,
    ScrapeResults,
    MetricsCalculator,
    MetricsAggregator,
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

        logger.separator()
        self._save(self.results)
        logger.separator()
        self._handle_metrics(self.results)

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
        saver = ResultManager(
            settings.output_csv_file,
            settings.output_json_file,
            settings.output_error_file,
        )
        saver.save_all(results)

    def _handle_metrics(self, results: ScrapeResults) -> None:
        """
        Calculate, display, and log metrics from scrape results.

        Args:
            results (ScrapeResults): List of scrape results to analyze.

        Steps:
            1. Display total metrics for all results.
            2. Group results by scraping method and display per-method metrics.
            3. Log status distribution across all results.

        Notes:
            - Uses `MetricsCalculator` to calculate metrics.
            - Uses `MetricsAggregator` to group results by method and status.
        """
        self._get_and_display_metrics("[TOTAL] METRICS", results)

        grouped = MetricsAggregator.group_by_method(results)
        for method, group in grouped.items():
            title = f"[{method.upper()}] METRICS"
            self._get_and_display_metrics(title, group)

        self._log_status_distribution(results)

    def _get_and_display_metrics(
        self,
        title: str,
        results: ScrapeResults
    ):
        """
        Compute and log metrics for a set of scrape results.

        Args:
            title (str): Title to display in logs.
            results (ScrapeResults): List of results to compute metrics for.

        Notes:
            - Uses `MetricsCalculator` to calculate metrics.
        """
        metrics = MetricsCalculator.calculate(results)
        logger.info(title)
        logger.info(f"\n{metrics}")

    def _log_status_distribution(self, results: ScrapeResults):
        """
        Log the distribution of scrape statuses.

        Args:
            results (ScrapeResults): List of scrape results to analyze.

        Notes:
            - Uses `MetricsAggregator` to group results by status.
        """
        status_counts = MetricsAggregator.group_by_status(results)
        logger.info(f"Status distribution: {status_counts}")
