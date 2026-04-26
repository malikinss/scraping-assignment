# ./src/scrapers/browser/deps.py

# ===== STANDARD LIB =====
from typing import Optional, AsyncGenerator
from contextlib import asynccontextmanager

# ===== THIRD PARTY =====
from playwright.async_api import (
    async_playwright,
    Playwright,
    Browser,
    Page,
    BrowserContext,
    TimeoutError,
)

# ===== INTERNAL =====
from src.config import settings
from src.logger import AppLogger
from src.models import ScrapeMethod, ScrapeResult, ScraperContext, URL
from src.scrapers.result_builder import ResultBuilder

# ===== BROWSER SCRAPER =====
Content = Optional[str]
METHOD = ScrapeMethod.BROWSER
logger = AppLogger(METHOD.value)

# ===== TYPE ALIASES =====
CTX = ScraperContext

# ===== EXPLICIT EXPORTS =====
__all__ = [
    "Optional",
    "AsyncGenerator",
    "asynccontextmanager",
    "async_playwright",
    "Playwright",
    "Browser",
    "Page",
    "BrowserContext",
    "TimeoutError",
    "settings",
    "ScrapeResult",
    "CTX",
    "URL",
    "ResultBuilder",
    "Content",
    "METHOD",
    "logger",
]
