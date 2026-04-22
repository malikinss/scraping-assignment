# ./src/services/metrics/aggregator.py

"""
Scraping Metrics Aggregator Module

This module provides functionality for aggregating and formatting
scrape metrics. It handles grouping, counting, and formatting of
metrics for analysis and reporting.

Usage:
    >>> from src.services.metrics import MetricsAggregator
    >>> aggregator = MetricsAggregator()
    >>> metrics = aggregator.metrics(results)
    >>> print(metrics)
"""

from .deps import (
    ScrapeResults,
    Grouped,
    Callable,
    ScrapeResult,
    TypeVar,
    Optional,
)
from .models import MetricsSummary
from .calculator import MetricsCalculator

K = TypeVar("K")
Distribution = dict[K, int]
KeyFn = Callable[[ScrapeResult], K]
FormatterFn = Callable[[K], str]

GroupedMetrics = dict[str, MetricsSummary]
NonZeroMetrics = dict[str, int]


class MetricsAggregator:
    """
    Aggregates and formats scrape metrics for analysis and reporting.

    Example:
        >>> from src.services.metrics import MetricsAggregator
        >>> aggregator = MetricsAggregator()
        >>> metrics = aggregator.metrics(results)
        >>> print(metrics)
    """

    @staticmethod
    def metrics(results: ScrapeResults) -> MetricsSummary:
        """
        Calculate metrics for all results.

        Args:
            results: Scrape results

        Returns:
            Metrics summary
        """
        MetricsAggregator._ensure_results(results)
        return MetricsCalculator.calculate(results)

    @staticmethod
    def per_method(
        results: ScrapeResults,
        exclude_zero: bool = False
    ) -> GroupedMetrics:
        """
        Calculate metrics per method.

        Args:
            results: Scrape results
            exclude_zero: Whether to exclude zero metrics

        Returns:
            Metrics grouped by method
        """
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
        """
        Calculate status distribution.

        Args:
            results: Scrape results
            exclude_zero: Whether to exclude zero metrics

        Returns:
            Distribution
        """
        return MetricsAggregator.distribution(
            results,
            lambda r: r.status,
            lambda s: s.upper(),
            exclude_zero
        )

    @staticmethod
    def _ensure_results(results: ScrapeResults) -> None:
        """
        Ensure results are not empty.

        Args:
            results: Scrape results

        Raises:
            ValueError: If results are empty
        """
        if not results:
            raise ValueError("Results cannot be empty")

    @staticmethod
    def distribution(
        results: ScrapeResults,
        key_fn: KeyFn,
        formatter: Optional[FormatterFn] = None,
        exclude_zero: bool = False
    ) -> Distribution:
        """
        Calculate distribution.

        Args:
            results: Scrape results
            key_fn: Key function
            formatter: Formatter function
            exclude_zero: Whether to exclude zero counts

        Returns:
            Distribution
        """
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
        """
        Convert metrics to dictionary.

        Args:
            metrics: Metrics summary
            exclude_zero: Whether to exclude zero metrics

        Returns:
            Dictionary
        """
        return metrics.to_dict(exclude_zero=exclude_zero)
