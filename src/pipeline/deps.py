# ./src/pipeline/deps.py

"""
This module is a dependency injection container for the scraping pipeline.
It is used to inject dependencies into the pipeline.
"""


import asyncio
from src.config import settings
from typing import Optional, List
from src.utils import URLUtils, Logger
from src.models import ScrapeResult, ScrapeStatus, ScrapeResults
from src.scrapers import HTTPScraper, BrowserScraper
from src.services import (
    URL,
    URLs,
    URLInputLoader,
    ResultManager,
    MetricsCalculator,
    MetricsAggregator,
    MetricsReporter
)

__all__ = [
    "asyncio",
    "settings",
    "Optional",
    "List",
    "URLUtils",
    "Logger",
    "ScrapeResult",
    "ScrapeResults",
    "ScrapeStatus",
    "HTTPScraper",
    "BrowserScraper",
    "URL",
    "URLs",
    "URLInputLoader",
    "ResultManager",
    "MetricsCalculator",
    "MetricsAggregator",
    "MetricsReporter"
]
