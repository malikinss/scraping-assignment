# ./src/logger/deps.py

"""
Shared dependencies and type definitions for logging modules.

This module centralizes commonly used imports and type definitions
across the logging subsystem. It helps reduce duplication and ensures
consistent typing for logging-related components.

Includes:
    - Standard logging and utility modules
    - Type helpers (TypeVar, TypedDict)
    - URL utilities for formatting/logging
    - Common data structures for metrics (e.g., Counts)
"""

import logging
import re
import os
from typing import TypeVar, TypedDict, Optional
from src.utils.url_utils import URLUtils


K = TypeVar("K")


class Counts(TypedDict):
    """
    Type hint for counts dictionary.

    Attributes:
        total (int): Total count.
        success (int): Success count.
        failed (int): Failed count.
        timeout (int): Timeout count.
        blocked (int): Blocked count.
        empty (int): Empty count.
        captcha (int): Captcha count.
    """
    total: int
    success: int
    failed: int
    timeout: int
    blocked: int
    empty: int
    captcha: int


__all__ = [
    "logging",
    "re",
    "os",
    "TypeVar",
    "TypedDict",
    "Optional",
    "URLUtils",
    "K",
    "Counts"
]
