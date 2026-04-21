# ./src/services/metrics/deps.py

"""
Metrics Service Dependencies
============================

This module contains the dependencies for the metrics service.
It is used to group all the necessary imports for the metrics service.

Key Features:
    - Pipeline-based metrics calculation
    - Rate calculation
    - Latency calculation
    - Content length calculation

Usage:
    >>> from src.services.metrics import MetricsCalculator
    >>> calculator = MetricsCalculator()
    >>> metrics = calculator.calculate(results)
    >>> print(metrics)

Example:
    >>> from src.services.metrics import MetricsCalculator
    >>> calculator = MetricsCalculator()
    >>> metrics = calculator.calculate(results)
    >>> print(metrics)
"""

from dataclasses import dataclass, asdict
from collections import defaultdict
from typing import (
    List,
    Dict,
    Any,
    Callable,
    TypeVar,
    Tuple,
    ClassVar,
    Optional,
)
from src.logger import AppLogger
from src.models import (
    ScrapeResult,
    ScrapeMethod,
    ScrapeStatus,
    ScrapeResults,
    Counts,
    Grouped,
)

__all__ = [
    "asdict",
    "dataclass",
    "List",
    "Dict",
    "Tuple",
    "Any",
    "Callable",
    "TypeVar",
    "ClassVar",
    "defaultdict",
    "Optional",
    "AppLogger",
    "ScrapeResult",
    "ScrapeMethod",
    "ScrapeStatus",
    "ScrapeResults",
    "Counts",
    "Grouped",
]
