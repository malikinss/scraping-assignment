# ./src/services/metrics/reporter.py

"""
Metrics Reporter Service
======================

This module is responsible for reporting metrics for the scraping process.
It uses a pipeline approach to report metrics for the scraping process.

Key Features:
    - Pipeline-based metrics reporting
    - Total metrics reporting
    - Metrics by method reporting
    - Status distribution reporting

Usage:
    >>> from src.services.metrics import MetricsReporter
    >>> reporter = MetricsReporter()
    >>> reporter.report(results)

Example:
    >>> from src.services.metrics import MetricsReporter
    >>> reporter = MetricsReporter()
    >>> reporter.report(results)
"""

from .calculator import MetricsCalculator
from .deps import ScrapeResults, AppLogger, Grouped

logger: AppLogger = AppLogger("MetricsReporter")


class MetricsReporter:
    """
    This class is responsible for reporting metrics for the scraping process.
    """

    def report(self, results: ScrapeResults) -> None:
        """
        Reports the metrics for the scraping process.

        Args:
            results (ScrapeResults): Results of the scraping process.
        """
        if not results:
            logger.metrics.log_no_metrics("ALL")
            return
        logger.core.separator()
        self._report_total(results)
        self._report_by_method(results)
        self._report_status_distribution(results)

    # ===== REPORTERS =====

    def _report_total(self, results: ScrapeResults) -> None:
        """
        Reports the total metrics for the scraping process.

        Args:
            results (ScrapeResults): Results of the scraping process.
        """
        self._report_group("TOTAL", results)

    def _report_by_method(self, results: ScrapeResults) -> None:
        """
        Reports the metrics by method for the scraping process.

        Args:
            results (ScrapeResults): Results of the scraping process.
        """
        grouped: Grouped = results.group_by_method()
        if not grouped:
            logger.metrics.log_no_metrics("METHODS")
            return

        for method, group in grouped.items():
            self._report_group(method, group)

    def _report_status_distribution(self, results: ScrapeResults) -> None:
        """
        Reports the status distribution for the scraping process.

        Args:
            results (ScrapeResults): Results of the scraping process.
        """
        distribution = {
            status.value.upper(): count
            for status, count in results.count_by_status().items()
        }
        logger.metrics.log_distribution("STATUS", distribution)

    # ===== CORE =====

    def _report_group(self, name: str, results: ScrapeResults) -> None:
        """
        Reports the metrics for a group of results.

        Args:
            name (str): Name of the group.
            results (ScrapeResults): Results of the scraping process.
        """
        try:
            metrics = MetricsCalculator.calculate(results)
            logger.metrics.log_metrics(name, metrics)
        except Exception as e:
            logger.metrics.log_metrics_exception(name, e)
