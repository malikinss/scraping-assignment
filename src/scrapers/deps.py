# ./src/scrapers/deps.py

"""
Shared dependencies for the scrapers module.

This module centralizes commonly used imports to:
    - reduce import duplication
    - simplify refactoring
    - provide a single dependency surface
"""

# ===== STANDARD LIB =====
import asyncio
import time
from typing import Optional, Callable, AsyncGenerator
from contextlib import asynccontextmanager

# ===== THIRD-PARTY =====
import httpx
from playwright.async_api import (
    Playwright,
    async_playwright,
    Browser,
    Page,
    BrowserContext,
    TimeoutError,
)

# ===== INTERNAL =====
from src.logger import AppLogger
from src.utils import URLUtils
from src.services import detector
from src.config import settings, proxy_manager
from src.models import (
    ScrapeMethod,
    ScrapeResult,
    ScrapeStatus,
    ScrapeResults,
    ScraperContext,
    URL,
    URLs,
)

# ===== EXPLICIT EXPORTS =====
__all__ = [
    # stdlib
    "asyncio",
    "time",
    "Optional",
    "Callable",
    "AsyncGenerator",
    "asynccontextmanager",

    # third-party
    "httpx",
    "Playwright",
    "async_playwright",
    "Browser",
    "Page",
    "BrowserContext",
    "TimeoutError",

    # internal
    "AppLogger",
    "URLUtils",
    "detector",
    "settings",
    "proxy_manager",
    "ScrapeMethod",
    "ScrapeResult",
    "ScrapeStatus",
    "ScrapeResults",
    "ScraperContext",
    "URLs",
    "URL",
]
