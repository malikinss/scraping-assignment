# ./src/services/metrics/reporter.py
from .aggregator import MetricsAggregator
from .deps import ScrapeResults, logger
from .subtypes import GroupedMetrics, Distribution


class MetricsReporter:

    def report(self, results: ScrapeResults) -> None:
        if not results:
            logger.metrics.log_no_metrics("ALL")
            return
        logger.core.separator()
        self._report_total(results)
        self._report_by_method(results)
        self._report_status_distribution(results)

    # ===== REPORTERS =====

    def _report_total(self, results: ScrapeResults) -> None:
        self._report_group("TOTAL", results)

    def _report_by_method(self, results: ScrapeResults) -> None:
        metrics: GroupedMetrics = MetricsAggregator.per_method(results)
        for method, metric in metrics.items():
            logger.metrics.log_metrics(method, metric)

    def _report_status_distribution(self, results: ScrapeResults) -> None:
        distribution: Distribution = MetricsAggregator.status_distribution(
            results)
        logger.metrics.log_distribution("STATUS", distribution)

    # ===== CORE =====
    def _report_group(self, name: str, results: ScrapeResults) -> None:
        try:
            metrics = MetricsAggregator.metrics(results)
            logger.metrics.log_metrics(name, metrics)
        except Exception as e:
            logger.metrics.log_metrics_exception(name, e)
