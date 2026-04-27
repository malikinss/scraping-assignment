# ./src/services/metrics/deps.py

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
    TYPE_CHECKING
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

logger: AppLogger = AppLogger("Metrics")

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
    "logger",
    "ScrapeResult",
    "ScrapeMethod",
    "ScrapeStatus",
    "ScrapeResults",
    "Counts",
    "Grouped",
    "TYPE_CHECKING"
]
