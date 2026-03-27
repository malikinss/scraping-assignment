# ./src/models/scrape_result.py

from typing import Optional
from dataclasses import dataclass
from src.models.enums import ScrapeStatus, ScrapeMethod


@dataclass
class ScrapeResult:
    url: str
    method: ScrapeMethod
    status: ScrapeStatus

    latency: float
    content_length: int

    error: Optional[str] = None

    def is_success(self) -> bool:
        return self.status == ScrapeStatus.SUCCESS

    def is_captcha(self) -> bool:
        return self.status == ScrapeStatus.CAPTCHA

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
