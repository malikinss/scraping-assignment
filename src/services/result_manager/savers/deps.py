# ./src/services/result_manager/savers/deps.py

"""
Dependencies
============

This module contains the dependencies for the savers package.
It is used by all the other modules in the savers package.
"""

import csv
import json
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Callable, Any, IO

from src.logger import AppLogger
from src.models import ScrapeResult, ScrapeResults


__all__ = [
    "csv",
    "json",
    "Path",
    "ABC",
    "abstractmethod",
    "ScrapeResult",
    "ScrapeResults",
    "AppLogger",
    "List",
    "Callable",
    "Any",
    "IO"
]
