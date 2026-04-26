# ./src/scrapers/http/deps.py

# ===== STANDARD LIB =====
import random
import httpx
import asyncio
from typing import Optional

# ===== INTERNAL =====
from src.config import settings
from src.logger import AppLogger
from src.models import ScrapeMethod, ScrapeResult, ScraperContext, URL
from src.scrapers.result_builder import ResultBuilder

# ===== TYPE ALIASES =====
Client = Optional[httpx.AsyncClient]
Response = Optional[httpx.Response]
CTX = ScraperContext
METHOD = ScrapeMethod.HTTPX
TimeoutException = httpx.TimeoutException
RequestError = httpx.RequestError
logger = AppLogger(METHOD.value)


# ===== EXPLICIT EXPORTS =====
__all__ = [
    "random",
    "httpx",
    "settings",
    "Client",

    "asyncio",
    "ScrapeResult",
    "CTX",
    "URL",
    "Response",
    "METHOD",
    "logger",
    "ResultBuilder",
    "TimeoutException",
    "RequestError"
]
