# ./src/services/results/deps.py

from src.models import ScraperContext
from src.services.deps import (
    AppLogger, Optional, Callable,
    Dict, ScrapeResult, ScrapeResults, ScrapeStatus
)

__all__ = [
    "ScraperContext",

    "Optional",
    "Callable",
    "Dict",
    "AppLogger",
    "ScrapeResult",
    "ScrapeResults",
    "ScrapeStatus"
]
