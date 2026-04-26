# ./src/services/results/factory/deps.py

# ===== STANDARD LIB =====
import time
from typing import Optional, Callable

# ===== INTERNAL =====
from src.logger import AppLogger
from src.services import detector
from src.models import ScrapeResult, ScrapeStatus, ScraperContext

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
