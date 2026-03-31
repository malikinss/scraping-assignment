# ./src/scrapers/deps.py

"""
Dependencies for the scrapers module.
"""

import time
import httpx
import asyncio
from typing import Optional
from playwright.async_api import (
    Playwright,
    async_playwright,
    Browser,
    Page,
    BrowserContext,
    TimeoutError,
)
from src.utils import Logger
from src.services import detector
from src.config.settings import settings
from src.config.proxy import proxy_manager
from src.models import ScrapeMethod, ScrapeResult, ScrapeStatus

__all__ = [
    "time",
    "httpx",
    "asyncio",
    "Optional",
    "Playwright",
    "async_playwright",
    "Browser",
    "Page",
    "BrowserContext",
    "TimeoutError",
    "Logger",
    "detector",
    "settings",
    "proxy_manager",
    "ScrapeMethod",
    "ScrapeResult",
    "ScrapeStatus",
]
