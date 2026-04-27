# ./src/services/metrics/deps.py

from collections import defaultdict
from src.models import ScrapeMethod, Counts, Grouped
from typing import (
    List,
    Any,
    TypeVar,
    Tuple,
    ClassVar,
    TYPE_CHECKING
)
from src.services.deps import (
    dataclass, asdict,
    Optional, Callable, Dict, AppLogger,
    ScrapeResult, ScrapeResults, ScrapeStatus
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
