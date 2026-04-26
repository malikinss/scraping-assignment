# ./src/scrapers/browser/deps.py

# ===== STANDARD LIB =====
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

# ===== COMMON SCRAPER DEPS =====
from src.scrapers.deps import (
    Optional,
    AsyncGenerator,
    settings,
    AppLogger,
    ScrapeMethod,
    ScrapeResult,
    CTX,
    URL,
    RFactory
)

# ===== BROWSER SCRAPER =====
Content = Optional[str]
METHOD = ScrapeMethod.PLAYWRIGHT
logger = AppLogger(METHOD.value)

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
    "RFactory",
    "Content",
    "METHOD",
    "logger",
]
