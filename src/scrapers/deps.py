# ./src/scrapers/deps.py

from typing import Optional, AsyncGenerator

# ===== INTERNAL =====
from src.config import settings
from src.logger import AppLogger
from src.models import ScrapeMethod, ScrapeResult, ScraperContext, URL
from src.services import ResultFactory as RFactory

# ===== TYPE ALIASES =====
CTX = ScraperContext

# ===== EXPLICIT EXPORTS =====
__all__ = [
    "Optional",
    "AsyncGenerator",
    "settings",
    "AppLogger",
    "ScrapeMethod",
    "ScrapeResult",
    "CTX",
    "URL",
    "RFactory",
]
