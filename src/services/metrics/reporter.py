# ./src/services/metrics/reporter.py

from .aggregator import MetricsAggregator
from .calculator import MetricsCalculator
from .deps import Logger, ScrapeResults

logger = Logger("MetricsReporter")


class MetricsReporter:
    """
    Service class responsible for calculating and displaying metrics.

    Provides aggregated metrics for:
        - All results
        - Results grouped by scraping method
        - Status distribution
    """

    def report(self, results: ScrapeResults) -> None:
        """
        Entry point for metrics reporting.

        Args:
            results (ScrapeResults): List of scraping results
        """
        if not results:
            logger.warning("No results provided for metrics reporting.")
            return

        self._report_total(results)
        self._report_by_method(results)
        self._report_status_distribution(results)

    # ===== INTERNAL METHODS =====

    def _report_total(self, results: ScrapeResults) -> None:
        """Log total aggregated metrics."""
        self._log_metrics("[TOTAL] METRICS", results)

    def _report_by_method(self, results: ScrapeResults) -> None:
        """Log metrics grouped by scraping method."""
        grouped = MetricsAggregator.group_by_method(results)

        for method, group in grouped.items():
            title = f"[{method.upper()}] METRICS"
            self._log_metrics(title, group)

    def _report_status_distribution(self, results: ScrapeResults) -> None:
        """Log distribution of scraping statuses."""
        status_counts = MetricsAggregator.group_by_status(results)
        logger.info(f"Status distribution: {status_counts}")

    def _log_metrics(self, title: str, results: ScrapeResults) -> None:
        """
        Calculate and log metrics for a given subset of results.

        Args:
            title (str): Section title for logging
            results (ScrapeResults): Results subset
        """
        metrics = MetricsCalculator.calculate(results)
        logger.info(title)
        logger.info(str(metrics))
