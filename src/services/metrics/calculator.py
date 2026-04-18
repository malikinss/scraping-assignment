# ./src/services/metrics/calculator.py

"""
Metrics Calculator Service
==========================

This module is responsible for calculating metrics for the scraping process.
It uses a pipeline approach to calculate metrics for the scraping process.

Key Features:
    - Pipeline-based metrics calculation
    - Rate calculation
    - Latency calculation
    - Content length calculation

Usage:
    >>> from src.services.metrics import MetricsCalculator
    >>> calculator = MetricsCalculator()
    >>> metrics = calculator.calculate(results)
    >>> print(metrics)

Example:
    >>> from src.services.metrics import MetricsCalculator
    >>> calculator = MetricsCalculator()
    >>> metrics = calculator.calculate(results)
    >>> print(metrics)
"""

from .deps import (
    Dict,
    Tuple,
    ScrapeStatus,
    ScrapeResults,
    Counts,
)
from .models import MetricsSummary

Rates = Dict[str, float]


class MetricsCalculator:
    """
    This class is responsible for calculating metrics for the scraping process.
    """

    @classmethod
    def calculate(cls, results: ScrapeResults) -> MetricsSummary:
        """
        Calculates metrics for the scraping process.

        Args:
            results (ScrapeResults): Results of the scraping process.

        Returns:
            MetricsSummary: Summary of the scraping process.
        """
        total = len(results)
        if total == 0:
            raise ValueError("No results to calculate metrics")

        counted: Counts = results.count_by_status()

        rates = cls._calculate_rates(counted, total)
        avg_latency, p95_latency = cls._calculate_latency(results)
        avg_content_length = cls._calculate_content_length(results)

        return MetricsSummary(
            total_requests=total,
            avg_latency=avg_latency,
            p95_latency=p95_latency,
            avg_content_length=avg_content_length,
            **rates,
        )

    # ===== RATES =====

    @staticmethod
    def _calculate_rates(counted: Counts, total: int) -> Rates:
        """
        Calculates rates for each status.

        Args:
            counted (Counts): Count of each status.
            total (int): Total number of results.

        Returns:
            Rates: Dictionary of rates for each status.
        """

        def rate(status: ScrapeStatus) -> float:
            return counted.get(status, 0) / total

        return {
            f"{status.name.lower()}_rate": rate(status)
            for status in ScrapeStatus
        }

    # ===== LATENCY =====

    @staticmethod
    def _calculate_latency(results: ScrapeResults) -> Tuple[float, float]:
        """
        Calculates latency metrics.

        Args:
            results (ScrapeResults): Results of the scraping process.

        Returns:
            Tuple[float, float]: Tuple containing average and P95 latency.
        """
        latencies = results.values(lambda r: r.latency)
        if not latencies:
            return 0.0, 0.0

        latencies_sorted = sorted(latencies)
        n = len(latencies_sorted)

        avg = sum(latencies_sorted) / n
        p95 = latencies_sorted[int(n * 0.95) - 1]

        return float(avg), float(p95)

    # ===== CONTENT LENGTH =====

    @staticmethod
    def _calculate_content_length(results: ScrapeResults) -> float:
        """
        Calculates content length metrics.

        Args:
            results (ScrapeResults): Results of the scraping process.

        Returns:
            float: Average content length.
        """
        values = results.values(lambda r: r.content_length)
        return sum(values) / len(values) if values else 0.0
