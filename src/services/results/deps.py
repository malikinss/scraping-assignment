# ./src/services/results/deps.py

# ===== STANDARD LIB =====
from typing import Optional, Callable, Dict

# ===== INTERNAL =====
from src.logger import AppLogger
from src.models import (
    ScrapeResult,
    ScrapeResults,
    ScrapeStatus,
    ScraperContext
)

__all__ = [
    "Optional",
    "Callable",
    "Dict",
    "AppLogger",
    "ScrapeResult",
    "ScrapeResults",
    "ScrapeStatus",
    "ScraperContext",
]
