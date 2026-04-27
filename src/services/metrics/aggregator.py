# ./src/services/metrics/aggregator.py
from .models import MetricsSummary
from .calculator import MetricsCalculator
from .deps import Grouped, Optional, ScrapeResults
from .subtypes import (
    Distribution,
    KeyFn,
    FormatterFn,
    GroupedMetrics,
    NonZeroMetrics
)


class MetricsAggregator:
    @staticmethod
    def metrics(results: ScrapeResults) -> MetricsSummary:
        MetricsAggregator._ensure_results(results)
        return MetricsCalculator.calculate(results)

    @staticmethod
    def per_method(
        results: ScrapeResults,
        exclude_zero: bool = False
    ) -> GroupedMetrics:
        MetricsAggregator._ensure_results(results)
        grouped: Grouped = results.group_by_method()
        return {
            method: MetricsAggregator.to_dict(
                MetricsAggregator.metrics(group),
                exclude_zero
            )
            for method, group in grouped.items()
        }

    @staticmethod
    def status_distribution(
        results: ScrapeResults,
        exclude_zero: bool = False
    ) -> Distribution:
        return MetricsAggregator.distribution(
            results,
            lambda r: r.status,
            lambda s: s.value.upper(),
            exclude_zero
        )

    @staticmethod
    def _ensure_results(results: ScrapeResults) -> None:
        if not results:
            raise ValueError("Results cannot be empty")

    @staticmethod
    def distribution(
        results: ScrapeResults,
        key_fn: KeyFn,
        formatter: Optional[FormatterFn] = None,
        exclude_zero: bool = False
    ) -> Distribution:
        res = results.count(key_fn)

        if exclude_zero:
            res = {k: v for k, v in res.items() if v > 0}

        if formatter:
            return {formatter(k): v for k, v in res.items()}

        return res

    @staticmethod
    def to_dict(
        metrics: MetricsSummary,
        exclude_zero: bool = False
    ) -> NonZeroMetrics:
        return metrics.to_dict(exclude_zero=exclude_zero)
