# ./src/services/results/factory/deps.py

# ===== STANDARD LIB =====
import time

# ===== INTERNAL =====
from src.services.detector import detector
from src.services.results.deps import (
    Optional,
    Callable,
    AppLogger,
    ScrapeResult,
    ScrapeStatus,
    ScraperContext
)

# ===== LOGGER =====
logger = AppLogger("ResFactory")

# ===== EXPLICIT EXPORTS =====
__all__ = [
    "time",
    "Optional",
    "Callable",
    "logger",
    "detector",
    "ScrapeResult",
    "ScrapeStatus",
    "ScraperContext",
]
