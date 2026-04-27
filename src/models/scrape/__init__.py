# ./src/models/scrape/__init__.py

from .method import ScrapeMethod
from .status import ScrapeStatus
from .result import ScrapeResult
from .context import ScraperContext
from .results import ScrapeResults, Grouped
from .deps import URL, URLs, Counts

__all__ = [
    "ScrapeMethod",
    "ScrapeStatus",
    "ScrapeResult",
    "ScrapeResults",
    "Counts",
    "Grouped",
    "URL",
    "URLs",
    "ScraperContext",
]
