# ./src/services/metrics/calculator.py
from .subtypes import Rates
from .models import MetricsSummary
from .deps import Tuple, ScrapeStatus, ScrapeResults, Counts


class MetricsCalculator:

    @classmethod
    def calculate(cls, results: ScrapeResults) -> MetricsSummary:
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

        def rate(status: ScrapeStatus) -> float:
            return counted.get(status, 0) / total

        return {
            f"{status.name.lower()}_rate": rate(status)
            for status in ScrapeStatus
        }

    # ===== LATENCY =====

    @staticmethod
    def _calculate_latency(results: ScrapeResults) -> Tuple[float, float]:
        latencies = results.values(lambda r: r.latency)
        if not latencies:
            return 0.0, 0.0

        latencies_sorted = sorted(latencies)
        n = len(latencies_sorted)

        avg = sum(latencies_sorted) / n
        p95_idx = max(0, int(n * 0.95) - 1)
        p95 = latencies_sorted[p95_idx]

        return float(avg), float(p95)

    # ===== CONTENT LENGTH =====

    @staticmethod
    def _calculate_content_length(results: ScrapeResults) -> float:
        values = results.values(lambda r: r.content_length)
        return sum(values) / len(values) if values else 0.0
