# ./src/services/metrics/models.py

from .deps import Dict, Any, dataclass


@dataclass
class MetricsSummary:
    """
    Summary statistics for scraping metrics.

    Attributes:
        total_requests (int): Total number of requests made.
        success_rate (float): Ratio of successful requests (0-1).
        blocked_rate (float): Ratio of blocked requests (0-1).
        empty_rate (float): Ratio of empty responses (0-1).
        captcha_rate (float): Ratio of CAPTCHA responses (0-1).
        timeout_rate (float): Ratio of timed-out requests (0-1).
        pdf_rate (float): Ratio of PDF responses (0-1).
        image_rate (float): Ratio of image responses (0-1).
        video_rate (float): Ratio of video responses (0-1).
        audio_rate (float): Ratio of audio responses (0-1).
        error_rate (float): Ratio of error responses (0-1).
        avg_latency (float): Average response latency in seconds.
        p95_latency (float): 95th percentile of response latency in seconds.
        avg_content_length (float): Average response content length in bytes.
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
    error_rate: float = 0.0

    avg_latency: float = 0.0
    p95_latency: float = 0.0

    avg_content_length: float = 0.0

    def __str__(self) -> str:
        """
        Returns a string representation of the metrics summary.

        Returns:
            str: String representation of the metrics summary.
        """
        return (
            f"Total requests: {self.total_requests}\n"
            f"Success rate: {self.success_rate:.2%}\n"
            f"Error rate: {self.error_rate:.2%}\n"
            f"Blocked rate: {self.blocked_rate:.2%}\n"
            f"Empty rate: {self.empty_rate:.2%}\n"
            f"Captcha rate: {self.captcha_rate:.2%}\n"
            f"Timeout rate: {self.timeout_rate:.2%}\n"
            f"PDF rate: {self.pdf_rate:.2%}\n"
            f"Image rate: {self.image_rate:.2%}\n"
            f"Video rate: {self.video_rate:.2%}\n"
            f"Audio rate: {self.audio_rate:.2%}\n"
            f"Avg latency: {self.avg_latency:.2f}s\n"
            f"P95 latency: {self.p95_latency:.2f}s\n"
            f"Avg content length: {self.avg_content_length:.2f}"
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the metrics summary to a dictionary.

        Returns:
            Dict[str, Any]: Dictionary containing the metrics summary.
        """
        return {
            "total_requests": self.total_requests,
            "success_rate": self.success_rate,
            "error_rate": self.error_rate,
            "blocked_rate": self.blocked_rate,
            "empty_rate": self.empty_rate,
            "captcha_rate": self.captcha_rate,
            "timeout_rate": self.timeout_rate,
            "pdf_rate": self.pdf_rate,
            "image_rate": self.image_rate,
            "video_rate": self.video_rate,
            "audio_rate": self.audio_rate,
            "avg_latency": self.avg_latency,
            "p95_latency": self.p95_latency,
            "avg_content_length": self.avg_content_length,
        }
