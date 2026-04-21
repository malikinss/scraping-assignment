# ./src/__init__.py

"""
Scraping Package

This package provides a comprehensive set of tools for web scraping.

Key Features:
- Model-based data representation
- Metrics calculation and aggregation
- URL validation and normalization

Usage:
    >>> from src import ScrapeResult, MetricsCalculator, URLUtils

Modules:
    models: Data models for scrape results
    services: Metrics calculation and reporting
    utils: Utility functions
"""

from .models import (
    ScrapeResult,
    ScrapeResults,
    ScrapeMethod,
    ScrapeStatus,
    URL,
    URLs,
    Counts,
    Grouped,
)

from .services import (
    MetricsCalculator,
    MetricsSummary,
    MetricsReporter,
    MetricsAggregator
)

from .utils import URLUtils


__all__ = [
    # models
    "ScrapeResult",
    "ScrapeResults",
    "ScrapeMethod",
    "ScrapeStatus",
    "URL",
    "URLs",
    "Counts",
    "Grouped",
    # services
    "MetricsCalculator",
    "MetricsSummary",
    "MetricsReporter",
    "MetricsAggregator",
    # utils
    "URLUtils",

]
