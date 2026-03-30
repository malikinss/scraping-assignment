# ./src/models/scrape_result.py

from typing import Optional
from dataclasses import dataclass
from .enums import ScrapeStatus, ScrapeMethod


@dataclass
class ScrapeResult:
    """
    Represents the result of a single scraping attempt.

    Attributes:
        url: The URL that was scraped.
        method: The method used for scraping.
        status: The status of the scraping attempt.
        latency: The time it took to scrape the URL.
        content_length: The length of the content that was scraped.
        error: The error message if the scraping attempt failed.
        content: The content that was scraped.
    """

    url: str
    method: ScrapeMethod
    status: ScrapeStatus

    latency: float
    content_length: int

    error: Optional[str] = None
    content: Optional[str] = None

    def to_dict(self) -> dict:
        """
        Converts the ScrapeResult to a dictionary.
        """
        return {
            "url": self.url,
            "method": self.method.value,
            "status": self.status.value,
            "latency": self.latency,
            "content_length": self.content_length,
            "error": self.error,
            "content": self.content,
        }

    def __str__(self) -> str:
        """
        Returns a string representation of the ScrapeResult.
        """
        return (
            f"ScrapeResult(\n"
            f"    url='{self.url}',\n"
            f"    method={self.method},\n"
            f"    status={self.status},\n"
            f"    latency={self.latency},\n"
            f"    content_length={self.content_length},\n"
            f"    error={self.error},\n"
            f"    content={'<omitted>' if self.content else None}\n"
            f")"
        )
