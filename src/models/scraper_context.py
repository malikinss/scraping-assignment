# ./src/models/scraper_context.py

"""
Scraper Context Module
======================

This module defines the `ScraperContext` class, a data structure for holding
all the context and state related to a single scraper execution.

Key Features:
    - Holds scraping parameters (url, method, timeout) and execution state
      (attempt, retries, error)
    - Immutable structure with efficient updates via `with_updates`
    - Frozen dataclass with slots for memory optimization
    - Supports optional fields for flexible state management

Usage:
    >>> from src.models import ScraperContext, ScrapeMethod
    >>> ctx = ScraperContext(
    ...     id=1,
    ...     url="https://example.com",
    ...     method=ScrapeMethod.GET,
    ...     timeout=10.0,
    ...     attempt=1,
    ...     retries=3,
    ... )
    >>> print(ctx.url)
    https://example.com
    >>> updated_ctx = ctx.with_updates(attempt=2, error="Timeout")
    >>> print(updated_ctx.attempt)
    2

Dependencies:
    - `.common.URL`: Type alias for URL strings
    - `.enums.ScrapeMethod`: HTTP method enum for scraping operations
    - `.deps`: Core dependencies including `dataclass`, `Optional`, `replace`

Classes:
    - ScraperContext: Immutable context for scraper execution

Key Methods:
    - `__init__`: Initialize the context
    - `with_updates`: Create a new context with updated fields

Typical Workflow:
    1. Create a context with initial parameters
    2. Update attempt number during retries
    3. Add error information on failure
    4. Use `with_updates` to create new immutable instances

"""

from .common import URL
from .enums import ScrapeMethod
from .deps import dataclass, Optional, replace


@dataclass(frozen=True, slots=True)
class ScraperContext:
    """
    Context for a single scraper execution.

    Attributes:
        id(int): The ID of the scraper.
        url(URL): The URL to scrape.
        method(ScrapeMethod): The HTTP method to use.
        timeout(float): The timeout for the request.
        attempt(Optional[int]): The current attempt number.
        retries(Optional[int]): The maximum number of retries.
        error(Optional[str]): The error message.
    """
    id: int
    url: URL
    method: ScrapeMethod
    timeout: float

    attempt: Optional[int] = None
    retries: Optional[int] = None
    error: Optional[str] = None

    def with_updates(self, **kwargs) -> "ScraperContext":
        """
        Return a new context with the specified fields updated.

        Args:
            **kwargs: Fields to update.

        Returns:
            ScraperContext: New context with updated fields.
        """
        return replace(self, **kwargs)
