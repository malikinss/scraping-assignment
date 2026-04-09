# ./src/services/metrics/deps.py

"""
This module contains the dependencies for the metrics service.
"""

import numpy as np
from dataclasses import dataclass, asdict
from collections import defaultdict
from typing import List, Dict, Any, Callable, TypeVar, Tuple, ClassVar
from src.utils import Logger
from src.models import (
    ScrapeResult,
    ScrapeMethod,
    ScrapeStatus,
    ScrapeResults,
    Counts,
    Grouped,
    K,
)

__all__ = [
    "np",
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
    "Logger",
    "ScrapeResult",
    "ScrapeMethod",
    "ScrapeStatus",
    "ScrapeResults",
    "Counts",
    "Grouped",
    "K",
]
