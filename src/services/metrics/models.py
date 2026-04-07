# ./src/services/metrics/models.py

from .deps import Dict, Any, dataclass, asdict, ClassVar, Tuple

MetricFieldSpec = Tuple[Tuple[str, str, str], ...]


@dataclass
class MetricsSummary:
    """
    Summary statistics for scraping results.

    This class aggregates overall request metrics, including:
        - Total requests
        - Success, failure, and error rates
        - Latency statistics (average and 95th percentile)
        - Average content length
        - Optional rates for specific content types (PDF, image, video, etc.)

    Attributes:
        total_requests (int): Total number of requests processed.
        success_rate (float): Ratio of successful requests.
        blocked_rate (float): Ratio of blocked responses.
        empty_rate (float): Ratio of empty responses.
        captcha_rate (float): Ratio of CAPTCHA responses.
        timeout_rate (float): Ratio of timeout responses.
        pdf_rate (float): Ratio of PDF responses.
        image_rate (float): Ratio of image responses.
        video_rate (float): Ratio of video responses.
        audio_rate (float): Ratio of audio responses.
        failed_rate (float): Ratio of failed requests.
        avg_latency (float): Average latency of requests in seconds.
        p95_latency (float): 95th percentile latency in seconds.
        avg_content_length (float): Average content length in bytes.
    """

    total_requests: int = 0

    success_rate: float = 0.0
    blocked_rate: float = 0.0
    empty_rate: float = 0.0
    captcha_rate: float = 0.0
    timeout_rate: float = 0.0
    pdf_rate: float = 0.0
    image_rate: float = 0.0
    video_rate: float = 0.0
    audio_rate: float = 0.0
    failed_rate: float = 0.0

    avg_latency: float = 0.0
    p95_latency: float = 0.0

    avg_content_length: float = 0.0

    _FIELDS: ClassVar[MetricFieldSpec] = (
        ("total_requests", "Total requests", "{}"),
        ("success_rate", "Success rate", "{:.2%}"),
        ("failed_rate", "Failed rate", "{:.2%}"),
        ("blocked_rate", "Blocked rate", "{:.2%}"),
        ("empty_rate", "Empty rate", "{:.2%}"),
        ("captcha_rate", "Captcha rate", "{:.2%}"),
        ("timeout_rate", "Timeout rate", "{:.2%}"),
        ("pdf_rate", "PDF rate", "{:.2%}"),
        ("image_rate", "Image rate", "{:.2%}"),
        ("video_rate", "Video rate", "{:.2%}"),
        ("audio_rate", "Audio rate", "{:.2%}"),
        ("avg_latency", "Avg latency", "{:.2f}s"),
        ("p95_latency", "P95 latency", "{:.2f}s"),
        ("avg_content_length", "Avg content length", "{:.2f}")
    )

    def _should_include(self, field: str, value: Any) -> bool:
        """
        Determine whether a field should be included in the metrics summary.

        Args:
            field (str): The name of the field.
            value (Any): The value of the field.

        Returns:
            bool: True if the field should be included, False otherwise.
        """
        if field == "total_requests":
            return True
        return value not in (None, 0, 0.0)

    def _format(self, sep: str = "\n") -> str:
        """
        Format the metrics summary as a string.

        Args:
            sep (str): The separator to use between metrics.

        Returns:
            str: String representation of the metrics summary.
        """
        lines = []

        for field, label, fmt in self._FIELDS:
            value = getattr(self, field, None)

            if not self._should_include(field, value):
                continue

            try:
                formatted = fmt.format(value)
            except Exception:
                formatted = str(value)

            lines.append(f"{label}: {formatted}")

        return sep.join(lines)

    def __str__(self) -> str:
        """
        String representation of the metrics summary.

        Returns:
            str: String representation of the metrics summary.
        """
        return self._format()

    def to_log(self) -> str:
        """
        Returns a string representation of the metrics summary for logging.

        Returns:
            str: Metrics formatted in a single line with separators.
        """
        return self._format(sep=" | ")

    def to_dict(self, exclude_zero: bool = False) -> Dict[str, Any]:
        """
        Convert metrics summary to a dictionary.

        Args:
            exclude_zero (bool): Whether to exclude zero values.

        Returns:
            Dict[str, Any]: Dictionary representation of the metrics.
        """
        data = asdict(self)
        if exclude_zero:
            data = {
                k: v
                for k, v in data.items()
                if not (isinstance(v, (int, float)) and v == 0)
            }
        return data
