# ./src/scrapers/http/deps.py

# ===== STANDARD LIB =====
import random
import httpx
import asyncio

# ===== COMMON SCRAPER DEPS =====
from src.scrapers.deps import (
    Optional,
    settings,
    AppLogger,
    ScrapeMethod,
    ScrapeResult,
    CTX,
    URL,
    RFactory
)

# ===== TYPE ALIASES =====
Client = Optional[httpx.AsyncClient]
Response = Optional[httpx.Response]
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
    "TimeoutException",
    "RequestError",
    "RFactory",
]
