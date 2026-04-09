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
from typing import Optional, Callable

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
from src.utils import Logger, URLUtils
from src.services import detector, URL, URLs
from src.config.settings import settings
from src.config.proxy import proxy_manager
from src.models import (
    ScrapeMethod,
    ScrapeResult,
    ScrapeStatus,
    ScrapeResults,
)

# ===== EXPLICIT EXPORTS =====
__all__ = [
    # stdlib
    "asyncio",
    "time",
    "Optional",
    "Callable",

    # third-party
    "httpx",
    "Playwright",
    "async_playwright",
    "Browser",
    "Page",
    "BrowserContext",
    "TimeoutError",

    # internal
    "Logger",
    "URLUtils",
    "detector",
    "settings",
    "proxy_manager",
    "ScrapeMethod",
    "ScrapeResult",
    "ScrapeStatus",
    "ScrapeResults",
    "URLs",
    "URL",
]
