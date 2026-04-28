# ./src/services/deps.py
from dataclasses import asdict
from src.logger import AppLogger
from typing import Callable, Dict
from src.deps import Optional, dataclass
from src.models import ScrapeResult, ScrapeStatus, ScrapeResults

__all__ = [
    "AppLogger",
    "dataclass",
    "asdict",
    "Optional",
    "Callable",
    "Dict",
    "ScrapeResult",
    "ScrapeStatus",
    "ScrapeResults"
]
