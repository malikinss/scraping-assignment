# ./src/models/scrape_result.py

from typing import Optional
from dataclasses import dataclass
from .enums import ScrapeStatus, ScrapeMethod


@dataclass
class ScrapeResult:
    url: str
    method: ScrapeMethod
    status: ScrapeStatus

    latency: float
    content_length: int

    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "method": self.method,
            "status": self.status,
            "latency": self.latency,
            "content_length": self.content_length,
            "error": self.error,
        }

    @classmethod
    def success(
        cls, url: str, method: ScrapeMethod, latency: float, content: str
    ):
        return cls(
            url=url,
            method=method,
            status=ScrapeStatus.SUCCESS,
            latency=latency,
            content_length=len(content),
        )

    @classmethod
    def failure(
        cls, url: str, method: ScrapeMethod, latency: float, error: str
    ):
        return cls(
            url=url,
            method=method,
            status=ScrapeStatus.FAILED,
            latency=latency,
            content_length=0,
            error=error,
        )

    @classmethod
    def captcha(
        cls, url: str, method: ScrapeMethod, latency: float
    ):
        return cls(
            url=url,
            method=method,
            status=ScrapeStatus.CAPTCHA,
            latency=latency,
            content_length=0,
            error="Captcha detected",
        )
