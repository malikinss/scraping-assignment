# ./src/services/result_manager/savers/deps.py

"""
Shared dependencies for result saver implementations.

This module centralizes commonly used imports for saver classes to:
    - Reduce import duplication across files
    - Simplify refactoring and dependency management
    - Provide a single source of truth for shared types and utilities

Exposes standard libraries, typing utilities, and project-specific
models required for implementing saver strategies.

Exports:
    csv: CSV handling module.
    json: JSON serialization module.
    Path: Filesystem path utility from pathlib.
    ABC: Base class for defining abstract classes.
    abstractmethod: Decorator for abstract methods.
    ScrapeResult: Model representing a single scrape result.
    ScrapeResults: Collection wrapper for scrape results.
    Logger: Project logging utility.
    List: Typing alias for list.
    Callable: Typing alias for callable objects.
    Any: Typing alias for any type.
"""

import csv
import json
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Callable, Any
from src.utils import Logger
from src.models import ScrapeResult, ScrapeResults


__all__ = [
    "csv",
    "json",
    "Path",
    "ABC",
    "abstractmethod",
    "ScrapeResult",
    "ScrapeResults",
    "Logger",
    "List",
    "Callable",
    "Any",
]
