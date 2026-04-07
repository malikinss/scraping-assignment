# ./src/services/metrics/calculator.py

from .deps import (
    np,
    List,
    Dict,
    Tuple,
    Logger,
    ScrapeStatus,
    ScrapeResult,
)
from .models import MetricsSummary
from .aggregator import MetricsAggregator

logger = Logger("MetricsCalculator")


class MetricsCalculator:
    """
    Utility class for computing aggregated metrics from scraping results.

    This class provides methods to calculate:
        - Request success/error rates
        - Latency statistics (average and percentile)
        - Content length statistics

    All calculations are based on a collection of `ScrapeResult` objects.
    """

    @classmethod
    def calculate(cls, results: List[ScrapeResult]) -> MetricsSummary:
        """
        Compute a full metrics summary from scrape results.

        This method aggregates multiple metrics including:
            - Total number of requests
            - Success and error rates per status
            - Average latency
            - 95th percentile latency (P95)
            - Average content length

        Args:
            results (List[ScrapeResult]): List of scraping results to analyze.

        Returns:
            MetricsSummary: Object containing all calculated metrics.

        Raises:
            ValueError: If the input results list is empty.
        """
        if not results:
            raise ValueError("No results to calculate metrics")

        total = len(results)

        grouped_by_status = MetricsAggregator().group_by_status(results)

        rates = cls._calculate_rates(grouped_by_status, total)
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
    def _calculate_rates(
        grouped: Dict[ScrapeStatus, int],
        total: int
    ) -> Dict[str, float]:
        """
        Calculate normalized rates for each scrape status.

        Each rate is computed as:
            count(status) / total

        Args:
            grouped (Dict[ScrapeStatus, int]): Mapping of scrape statuses
                to their occurrence counts.
            total (int): Total number of results.

        Returns:
            Dict[str, float]: Dictionary where keys are in the format
                "<status>_rate" (e.g., "success_rate") and values are
                normalized rates in the range [0.0, 1.0].

        Notes:
            Missing statuses in the input dictionary are treated as zero.
        """
        def rate(status: ScrapeStatus) -> float:
            return grouped.get(status, 0) / total

        return {
            f"{status.name.lower()}_rate": rate(status)
            for status in ScrapeStatus
        }

    @staticmethod
    def _calculate_latency(results: List[ScrapeResult]) -> Tuple[float, float]:
        """
        Calculate latency statistics from scrape results.

        Extracts latency values and computes:
            - Mean (average) latency
            - 95th percentile latency (P95)

        Args:
            results (List[ScrapeResult]): List of scraping results.

        Returns:
            Tuple[float, float]: A tuple containing:
                - Average latency (float)
                - 95th percentile latency (float)

        Notes:
            Results with missing (`None`) latency values are ignored.
            Returns (0.0, 0.0) if no valid latency values are present.
        """

        latencies = [r.latency for r in results if r.latency is not None]

        if not latencies:
            return 0.0, 0.0

        return (
            float(np.mean(latencies)),
            float(np.percentile(latencies, 95))
        )

    @staticmethod
    def _calculate_content_length(results: List[ScrapeResult]):
        """
        Calculate the average content length from scrape results.

        Args:
            results (List[ScrapeResult]): List of scraping results.

        Returns:
            float: Average content length. Returns 0.0 if no valid values
                   exist.

        Notes:
            Results with missing (`None`) content_length values are ignored.
        """

        values = [
            r.content_length
            for r in results
            if r.content_length is not None
        ]

        return sum(values) / len(values) if values else 0.0
