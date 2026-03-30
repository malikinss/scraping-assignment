# ./src/services/metrics/calculator.py

import numpy as np
from typing import List, Dict
from .models import MetricsSummary
from src.utils.logger import Logger
from src.models.enums import ScrapeStatus
from .aggregator import MetricsAggregator
from src.models.scrape_result import ScrapeResult


logger = Logger(__name__)


class MetricsCalculator:
    """
    Calculates metrics summary from a list of ScrapeResult objects.
    """

    def calculate(self, results: List[ScrapeResult]) -> MetricsSummary:
        """
        Calculates success/error rates, latency and content length metrics.

        Args:
            results (List[ScrapeResult]): List of scrape results.

        Returns:
            MetricsSummary: Aggregated metrics.
        """
        if not results:
            logger.error("No results to calculate metrics")
            raise ValueError("No results to calculate metrics")

        logger.debug("Calculating metrics")
        total = len(results)
        logger.debug(f"Total requests: {total}")

        aggregator = MetricsAggregator()
        grouped_by_status = aggregator.group_by_status(results)

        rates = self._calculate_rates(grouped_by_status)
        avg_latency, p95_latency = self._calculate_latency(results)
        avg_content_length = self._calculate_content_length(results)

        logger.debug("Metrics calculated successfully")
        return MetricsSummary(
            total_requests=total,
            success_rate=rates["success_rate"],
            blocked_rate=rates["blocked_rate"],
            empty_rate=rates["empty_rate"],
            captcha_rate=rates["captcha_rate"],
            timeout_rate=rates["timeout_rate"],
            pdf_rate=rates["pdf_rate"],
            image_rate=rates["image_rate"],
            video_rate=rates["video_rate"],
            audio_rate=rates["audio_rate"],
            error_rate=rates["error_rate"],
            avg_latency=avg_latency,
            p95_latency=p95_latency,
            avg_content_length=avg_content_length,
        )

    def _calculate_rates(
        self, grouped_by_status: Dict[ScrapeStatus, int]
    ) -> Dict[str, float]:
        """
        Calculates success/error rates from grouped results.

        Args:
            grouped_by_status (Dict[ScrapeStatus, int]): Dictionary mapping
                                                         each ScrapeStatus to
                                                         the count of results.

        Returns:
            Dict[str, float]: Dictionary mapping each rate name to its value.
        """
        logger.debug("Calculating rates")
        total = sum(grouped_by_status.values())
        logger.debug(f"Total requests: {total}")

        success_count = grouped_by_status.get(ScrapeStatus.SUCCESS, 0)
        blocked_count = grouped_by_status.get(ScrapeStatus.BLOCKED, 0)
        empty_count = grouped_by_status.get(ScrapeStatus.EMPTY, 0)
        captcha_count = grouped_by_status.get(ScrapeStatus.CAPTCHA, 0)
        timeout_count = grouped_by_status.get(ScrapeStatus.TIMEOUT, 0)
        pdf_count = grouped_by_status.get(ScrapeStatus.PDF, 0)
        image_count = grouped_by_status.get(ScrapeStatus.IMAGE, 0)
        video_count = grouped_by_status.get(ScrapeStatus.VIDEO, 0)
        audio_count = grouped_by_status.get(ScrapeStatus.AUDIO, 0)
        error_count = grouped_by_status.get(ScrapeStatus.ERROR, 0)

        logger.debug("Rates calculated successfully")
        return {
            "success_rate": success_count / total,
            "blocked_rate": blocked_count / total,
            "empty_rate": empty_count / total,
            "captcha_rate": captcha_count / total,
            "timeout_rate": timeout_count / total,
            "pdf_rate": pdf_count / total,
            "image_rate": image_count / total,
            "video_rate": video_count / total,
            "audio_rate": audio_count / total,
            "error_rate": error_count / total,
        }

    def _calculate_latency(self, results: List[ScrapeResult]):
        """
        Calculates average and 95th percentile latency from scrape results.

        Args:
            results (List[ScrapeResult]): List of scrape results.

        Returns:
            Tuple[float, float]: Tuple containing average latency and 95th
                                 percentile latency.
        """
        logger.debug("Calculating latency")

        latencies = [r.latency for r in results if r.latency is not None]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        p95_latency = np.percentile(latencies, 95) if latencies else 0

        logger.debug("Latency calculated successfully")
        return avg_latency, p95_latency

    def _calculate_content_length(self, results: List[ScrapeResult]):
        """
        Calculates average content length from scrape results.

        Args:
            results (List[ScrapeResult]): List of scrape results.

        Returns:
            float: Average content length.
        """
        logger.debug("Calculating content length")

        content_lengths = [
            r.content_length
            for r in results
            if r.content_length is not None
        ]

        avg_content_length = sum(content_lengths) / \
            len(content_lengths) if content_lengths else 0

        logger.debug("Content length calculated successfully")
        return avg_content_length
