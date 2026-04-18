# ./src/logger/deps.py

"""
Shared dependencies and type exports for the logging subsystem.

This module centralizes commonly used standard library imports,
project-level utilities, and shared type definitions for all logger
components. It is used to reduce duplication and ensure consistency
across the logging package.

Exports:
    os: Operating system interface module.
    re: Regular expression module.
    logging: Standard Python logging module.
    Optional: Optional type from typing module.
    URLUtils: Utility class for URL formatting and normalization.
    Counts: Typed structure representing aggregated pipeline metrics.
    ScraperContext: Context object for scraper execution.
"""

import os
import re
import logging
from typing import Optional
from src.utils.url_utils import URLUtils
from src.models import Counts, ScraperContext

__all__ = [
    "os",
    "re",
    "logging",
    "Optional",
    "URLUtils",
    "Counts",
    "ScraperContext"
]
