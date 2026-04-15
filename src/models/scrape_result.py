# ./src/models/scrape_result.py

"""
Represents the result of a single scraping operation.

This module defines the `ScrapeResult` dataclass, which serves as the
fundamental unit of data in the scraping system. Each instance of
`ScrapeResult` captures all relevant information about a single
scraping attempt, enabling comprehensive analysis and reporting.

Key Concepts:
    - ScrapeResult: A dataclass that encapsulates all metadata about
      a scraping operation, including request identifiers, execution
      metrics, response content, and error information.
    - Domain Model: This class is a core component of the domain model,
      providing a type-safe and expressive way to represent scraping
      outcomes.
    - Serialization: Includes built-in support for converting results
      to dictionaries and DataFrames for easy analysis and storage.

Usage:
    >>> result = ScrapeResult(
    ...     id=1,
    ...     url="https://example.com",
    ...     method=ScrapeMethod.HTTPX,
    ...     status=ScrapeStatus.SUCCESS,
    ...     latency=0.5,
    ...     content_length=1024,
    ...     content="<html>...</html>"
    ... )
    >>> print(result)
    ScrapeResult(
        id=1,
        url='https://example.com',
        method=httpx,
        status=success,
        latency=0.500s,
        content_length=1024,
        error=None,
        content='<omitted>'
    )
    >>> result.to_dict()
    {
        'id': 1,
        'url': 'https://example.com',
        'method': 'httpx',
        'status': 'success',
        'latency': 0.5,
        'content_length': 1024,
        'error': None,
        'content': '<html>...</html>'
    }

See Also:
    - :class:`~src.models.enums.ScrapeStatus` for status definitions
    - :class:`~src.models.enums.ScrapeMethod` for method definitions
    - :class:`~src.models.scrape_results.ScrapeResults` for collection
                                                        management

Module Structure:
    - Imports: Core dependencies and domain enums
    - Dataclass Definition: `ScrapeResult` with comprehensive attributes
    - Serialization: Methods for converting to dict and DataFrame
    - Representation: String and developer-friendly representations
    - Domain Properties: Helper properties for status checking

This module provides the foundation for all scraping operations, enabling
consistent data capture and analysis throughout the system.
"""

from .deps import Optional, dataclass, asdict
from .enums import ScrapeStatus, ScrapeMethod


@dataclass(slots=True)
class ScrapeResult:
    """
    Represents the result of a single scraping operation.

    This dataclass stores all relevant metadata about a scraping attempt,
    including request identifiers, execution metrics, response content,
    and error information.

    Attributes:
        id (int): Unique identifier of the scraping task.
        url (str): Target URL that was scraped.
        method (ScrapeMethod): Scraping method used (HTTPX, PLAYWRIGHT, etc.).
        status (ScrapeStatus): Final status of the scraping operation.
        latency (float): Request duration in seconds.
        content_length (int): Size of the retrieved content.
        error (Optional[str]): Error message if the request failed.
        content (Optional[str]): Raw response content if available.
    """

    id: int
    url: str
    method: ScrapeMethod
    status: ScrapeStatus
    latency: float
    content_length: int
    error: Optional[str] = None
    content: Optional[str] = None

    # ===== SERIALIZATION =====

    def to_dict(self, include_content: bool = True) -> dict:
        """
        Convert the scraping result into a dictionary representation.

        Args:
            include_content (bool): Whether to include full response content.
                If False, the content field will be set to None.

        Returns:
            dict: Dictionary representation of the scraping result.
        """
        result = asdict(self)
        if not include_content:
            result["content"] = None
        return result

    # ===== REPRESENTATION =====

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the result.

        Returns:
            str: Pretty formatted multi-line string describing the result.
        """
        return (
            f"{self.__class__.__name__}(\n"
            f"    id={self.id},\n"
            f"    url='{self.url}',\n"
            f"    method={self.method.value},\n"
            f"    status={self.status.value},\n"
            f"    latency={self.latency:.3f}s,\n"
            f"    content_length={self.content_length},\n"
            f"    error={self.error},\n"
            f"    content={'<omitted>' if self.content else None}\n"
            f")"
        )

    def __repr__(self) -> str:
        """
        Return developer-friendly representation of the object.

        Returns:
            str: Same as __str__ for consistent debugging output.
        """
        return self.__str__()

    # ===== DOMAIN PROPERTIES =====

    @property
    def is_success(self) -> bool:
        """
        Check if the scraping result represents a successful request.

        Returns:
            bool: True if status is SUCCESS, otherwise False.
        """
        return self.status.is_success

    @property
    def is_failure(self) -> bool:
        """
        Check if the scraping result represents a failed request.

        Returns:
            bool: True if status indicates failure, otherwise False.
        """
        return self.status.is_failure

    @property
    def is_content(self) -> bool:
        """
        Check if the result contains usable content.

        Returns:
            bool: True if content is available and valid.
        """
        return self.status.is_content
