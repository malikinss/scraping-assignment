# ./src/services/result_manager/savers/deps.py

"""
This module contains the dependencies for the result manager savers.
"""

import csv
import json
from pathlib import Path
from abc import ABC, abstractmethod
from src.models import ScrapeResult
from src.utils.logger import Logger
from typing import List, Callable, Any


__all__ = [
    "csv",
    "json",
    "Path",
    "ABC",
    "abstractmethod",
    "ScrapeResult",
    "Logger",
    "List",
    "Callable",
    "Any",
]
