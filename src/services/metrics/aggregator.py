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
    def per_method(results: ScrapeResults) -> GroupedMetrics:
        """
        Calculate metrics per method.

        Args:
            results: Scrape results

        Returns:
            Metrics grouped by method
        """
        MetricsAggregator._ensure_results(results)
        grouped: Grouped = results.group_by_method()
        return {
            method: MetricsAggregator.metrics(group)
            for method, group in grouped.items()
        }

    @staticmethod
    def status_distribution(results: ScrapeResults) -> Distribution:
        """
        Calculate status distribution.

        Args:
            results: Scrape results

        Returns:
            Distribution
        """
        return MetricsAggregator.distribution(
            results, lambda r: r.status, lambda s: s.value.upper()
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
        formatter: Optional[FormatterFn] = None
    ) -> Distribution:
        """
        Calculate distribution.

        Args:
            results: Scrape results
            key_fn: Key function
            formatter: Formatter function

        Returns:
            Distribution
        """
        res = results.count(key_fn)

        if formatter:
            res = {formatter(k): v for k, v in res.items()}

        return res
