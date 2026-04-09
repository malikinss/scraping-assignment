# ./src/services/metrics/reporter.py

from .calculator import MetricsCalculator
from .deps import Logger, ScrapeResults

logger = Logger("MetricsReporter")


class MetricsReporter:
    """
    Reports metrics for a collection of scrape results.

    Uses MetricsCalculator to compute metrics and logs them
    in a structured format.
    """

    def report(self, results: ScrapeResults) -> None:
        """
        Entry point for metrics reporting.

        Args:
            results (ScrapeResults): Collection of scrape results.
        """
        if not results or len(results) == 0:
            logger.warning("No results provided for metrics reporting.")
            return

        self._report_total(results)
        self._report_by_method(results)
        self._report_status_distribution(results)

    # ===== INTERNAL METHODS =====

    def _report_total(self, results: ScrapeResults) -> None:
        """Log overall metrics for all results."""
        self._log_metrics("[TOTAL] METRICS", results)

    def _report_by_method(self, results: ScrapeResults) -> None:
        """
        Log metrics grouped by scraping method.
        """
        grouped = results.group_by_method()
        if not grouped:
            logger.info("No methods found for metrics reporting.")
            return

        for method, group in grouped.items():
            title = f"[{method.upper()}] METRICS"
            self._log_metrics(title, group)

    def _report_status_distribution(self, results: ScrapeResults) -> None:
        """
        Log the count of results per ScrapeStatus.
        """
        status_counts = results.count_by_status()
        logger.info(f"Status distribution: {status_counts}")

    def _log_metrics(self, title: str, results: ScrapeResults) -> None:
        """
        Compute metrics and log them under a given title.

        Args:
            title (str): Header for log output.
            results (ScrapeResults): Collection of results to compute metrics
                                     on.
        """
        try:
            metrics = MetricsCalculator.calculate(results)
            logger.info(title)
            logger.info(str(metrics))
        except Exception as e:
            logger.exception(f"Failed to calculate metrics for {title}: {e}")
