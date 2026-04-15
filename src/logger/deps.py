# ./src/logger/deps.py

"""
Shared dependencies and type exports for the logging subsystem.

This module centralizes commonly used standard library imports,
project-level utilities, and shared type definitions for all logger
components. It is used to reduce duplication and ensure consistency
across the logging package.

Exports:
    logging: Standard Python logging module.
    re: Regular expression module.
    os: Operating system interface module.
    Optional: Optional type from typing module.
    URLUtils: Utility class for URL formatting and normalization.
    Counts: Typed structure representing aggregated pipeline metrics.
"""

import logging
import re
import os
from typing import Optional
from src.utils.url_utils import URLUtils
from src.models import Counts

__all__ = [
    "logging",
    "re",
    "os",
    "Optional",
    "URLUtils",
    "Counts"
]
