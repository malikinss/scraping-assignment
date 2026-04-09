# ./src/services/metrics/calculator.py

from .deps import (
    np,
    Dict,
    Tuple,
    Logger,
    ScrapeStatus,
    ScrapeResults,
    Counts,
)
from .models import MetricsSummary

logger = Logger("MetricsCalculator")
Rates = Dict[str, float]


class MetricsCalculator:
    """
    Computes aggregated metrics from a collection of `ScrapeResult` objects.

    Metrics include:
        - Total requests
        - Success/failure rates by status
        - Average and 95th percentile latency
        - Average content length
    """

    @classmethod
    def calculate(cls, results: ScrapeResults) -> MetricsSummary:
        """
        Calculate summary metrics for a set of scrape results.

        Args:
            results (ScrapeResults): A collection of scrape results.

        Returns:
            MetricsSummary: Object containing calculated metrics.

        Raises:
            ValueError: If `results` is empty.
        """
        if not results:
            raise ValueError("No results to calculate metrics")

        total = len(results)
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

    @staticmethod
    def _calculate_rates(counted: Counts, total: int) -> Rates:
        """
        Calculate rate of each scrape status.

        Args:
            counted (Counts): Mapping of ScrapeStatus -> count.
            total (int): Total number of scrape results.

        Returns:
            Rates: Dictionary of status_rate -> float.
        """
        def rate(status: ScrapeStatus) -> float:
            return counted.get(status, 0) / total

        return {
            f"{status.name.lower()}_rate": rate(status)
            for status in ScrapeStatus
        }

    @staticmethod
    def _calculate_latency(results: ScrapeResults) -> Tuple[float, float]:
        """
        Calculate average and 95th percentile latency.

        Args:
            results (ScrapeResults): Collection of scrape results.

        Returns:
            Tuple[float, float]: Average latency, 95th percentile latency.
        """
        latencies = results.values(lambda r: r.latency)
        if not latencies:
            return 0.0, 0.0
        return float(np.mean(latencies)), float(np.percentile(latencies, 95))

    @staticmethod
    def _calculate_content_length(results: ScrapeResults) -> float:
        """
        Calculate average content length of all results.

        Args:
            results (ScrapeResults): Collection of scrape results.

        Returns:
            float: Average content length. Returns 0.0 if no results.
        """
        values = results.values(lambda r: r.content_length)
        return sum(values) / len(values) if values else 0.0
