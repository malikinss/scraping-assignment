# ./src/pipeline/deps.py

"""
Dependency aggregation module for the pipeline layer.

This module serves as a centralized import hub for all dependencies
used within the pipeline package. It simplifies imports across pipeline
modules by re-exporting commonly used classes, types, and utilities.

The goal is to:
    - Reduce import verbosity in pipeline modules
    - Provide a consistent dependency interface
    - Decouple internal module structure from usage

Exposed components include:
    - Core utilities: asyncio, settings, AppLogger
    - Typing helpers: Optional, List, Callable, Awaitable
    - Domain models: ScrapeResult, ScrapeResults, ScrapeStatus, ScrapeMethod
    - URL types: URL, URLs
    - Scrapers: HTTPScraper, BrowserScraper
    - Services: URLInputLoader, ResultManager, MetricsCalculator,
      MetricsSummary, MetricsReporter
    - Aggregation types: Counts

Example:
    from .deps import ScrapeResult, HTTPScraper, settings

    scraper = HTTPScraper()
"""

import asyncio
from src.config import settings
from src.logger import AppLogger
from typing import Optional, List, Callable, Awaitable
from src.models import (
    ScrapeResult, ScrapeStatus, ScrapeResults, URL, URLs, Counts, ScrapeMethod
)
from src.scrapers import HTTPScraper, BrowserScraper
from src.services import (
    URLInputLoader,
    ResultManager,
    MetricsCalculator,
    MetricsSummary,
    MetricsReporter
)

__all__ = [
    "asyncio",
    "settings",
    "AppLogger",
    "Optional",
    "List",
    "ScrapeResult",
    "ScrapeResults",
    "ScrapeStatus",
    "ScrapeMethod",
    "HTTPScraper",
    "BrowserScraper",
    "URL",
    "URLs",
    "URLInputLoader",
    "ResultManager",
    "MetricsCalculator",
    "MetricsSummary",
    "MetricsReporter",
    "Counts",
    "Callable",
    "Awaitable"
]
