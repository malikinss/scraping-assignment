# ./src/scrapers/deps.py

"""
Dependencies for the scrapers module.
"""

import time
import httpx
import asyncio
from typing import Optional, Callable
from playwright.async_api import (
    Playwright,
    async_playwright,
    Browser,
    Page,
    BrowserContext,
    TimeoutError,
)
from src.utils import Logger, URLUtils
from src.services import detector
from src.config.settings import settings
from src.config.proxy import proxy_manager
from src.models import ScrapeMethod, ScrapeResult, ScrapeStatus

__all__ = [
    "time",
    "httpx",
    "asyncio",
    "Optional",
    "Callable",
    "Playwright",
    "async_playwright",
    "Browser",
    "Page",
    "BrowserContext",
    "TimeoutError",
    "Logger",
    "URLUtils",
    "detector",
    "settings",
    "proxy_manager",
    "ScrapeMethod",
    "ScrapeResult",
    "ScrapeStatus",
]
