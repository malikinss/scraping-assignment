# ./src/services/result_manager/deps.py

"""
Dependencies
============

This module contains the dependencies for the result_manager package.
It is used by all the other modules in the result_manager package.
"""

from typing import Dict
from src.logger import AppLogger
from src.models import ScrapeResults

__all__ = ["Dict", "AppLogger", "ScrapeResults"]
