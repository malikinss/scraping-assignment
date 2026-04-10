# ./src/services/result_manager/deps.py

"""
Shared dependencies for the result manager service.

This module centralizes commonly used imports for the result manager
layer to reduce duplication and simplify dependency management across
the service.

It exposes typing utilities, logging, and core domain models required
for processing and aggregating scrape results.
"""

from typing import Dict
from src.utils import Logger
from src.models import ScrapeResults

__all__ = ["Dict", "Logger", "ScrapeResults"]
