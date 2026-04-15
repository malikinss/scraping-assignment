# ./src/models/__init__.py

"""
Scraping Models Package

This package provides the data models and type definitions used throughout
the scraping application. These models represent the core entities and
types involved in the scraping process, enabling type safety and
structured data representation.

Key Components:
    - Enums: Enumerations for defining scrape methods and statuses
    - ScrapeResult: Represents a single scraping result with detailed
      information about the scrape operation
    - ScrapeResults: A collection class for managing multiple scrape results
    - Common Types: Utility types for URLs, counts, and other common data

Usage:
    >>> from src.models import ScrapeResult, ScrapeResults, ScrapeStatus
    >>> result = ScrapeResult(
    ...     id=1, url="https://example.com", status=ScrapeStatus.SUCCESS
    ... )
    >>> results = ScrapeResults([result])
    >>> print(results)
    ScrapeResults(total=1)

See Also:
    - :mod:`~src.models.enums` for enumeration definitions
    - :mod:`~src.models.scrape_result` for individual result representation
    - :mod:`~src.models.scrape_results` for result collection management
    - :mod:`~src.models.common` for common type definitions

Module Structure:
    - Imports: Core dependencies and domain enums
    - Type Aliases: Type hints for common patterns
    - Class Definitions: `ScrapeResult` and `ScrapeResults` classes
    - Export: Public API for the models package

This package serves as the foundation for data representation in the
scraping application, ensuring type safety and structured data
handling.
"""

from .enums import ScrapeMethod, ScrapeStatus
from .scrape_result import ScrapeResult
from .scrape_results import ScrapeResults, Grouped
from .common import URL, URLs, Counts

__all__ = [
    "ScrapeMethod",
    "ScrapeStatus",
    "ScrapeResult",
    "ScrapeResults",
    "Counts",
    "Grouped",
    "URL",
    "URLs",
]
