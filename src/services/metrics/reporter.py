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

from .models import MetricsSummary
from .aggregator import (
    MetricsAggregator,
    GroupedMetrics,
    Distribution
)
from .deps import ScrapeResults, AppLogger

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
        metrics: MetricsSummary = MetricsAggregator.metrics(results)
        logger.metrics.log_metrics("TOTAL", metrics)

    def _report_by_method(self, results: ScrapeResults) -> None:
        """
        Reports the metrics by method for the scraping process.

        Args:
            results (ScrapeResults): Results of the scraping process.
        """
        metrics: GroupedMetrics = MetricsAggregator.per_method(results)
        for method, metric in metrics.items():
            logger.metrics.log_metrics(method, metric)

    def _report_status_distribution(self, results: ScrapeResults) -> None:
        """
        Reports the status distribution for the scraping process.

        Args:
            results (ScrapeResults): Results of the scraping process.
        """
        distribution: Distribution = MetricsAggregator.status_distribution(
            results)
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
            metrics = MetricsAggregator.metrics(results)
            logger.metrics.log_metrics(name, metrics)
        except Exception as e:
            logger.metrics.log_metrics_exception(name, e)
