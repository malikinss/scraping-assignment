# ./src/models/scrape_result.py

from .deps import Optional, dataclass, asdict
from .enums import ScrapeStatus, ScrapeMethod


@dataclass(slots=True)
class ScrapeResult:
    """
    Represents the result of a single scraping attempt.

    Attributes:
        id (int): Unique identifier for the scrape attempt.
        url (str): The URL that was scraped.
        method (ScrapeMethod): Method used for scraping.
        status (ScrapeStatus): Result status of the scrape.
        latency (float): Request latency in seconds.
        content_length (int): Length of content retrieved.
        error (Optional[str]): Error message if scraping failed.
        content (Optional[str]): Scraped content (may be None).
    """

    id: int
    url: str
    method: ScrapeMethod
    status: ScrapeStatus
    latency: float
    content_length: int
    error: Optional[str] = None
    content: Optional[str] = None

    def to_dict(self, include_content: bool = True) -> dict:
        """
        Converts the ScrapeResult to a dictionary.

        Args:
            include_content (bool): Whether to include the content field.
        Returns:
            dict: Dictionary representation of the result.
        """
        result = asdict(self)
        if not include_content:
            result["content"] = None
        return result

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the ScrapeResult.

        The content field is omitted for brevity if present.
        """
        return (
            f"ScrapeResult(\n"
            f"    id={self.id},\n"
            f"    url='{self.url}',\n"
            f"    method={self.method},\n"
            f"    status={self.status},\n"
            f"    latency={self.latency:.3f}s,\n"
            f"    content_length={self.content_length},\n"
            f"    error={self.error},\n"
            f"    content={'<omitted>' if self.content else None}\n"
            f")"
        )

    @property
    def is_success(self) -> bool:
        """Returns True if the scrape was successful."""
        return self.status.is_success

    @property
    def is_error(self) -> bool:
        """Returns True if the scrape failed."""
        return self.status.is_non_success
