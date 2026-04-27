# ./src/services/deps.py
from src.logger import AppLogger
from dataclasses import dataclass, asdict
from typing import Optional, Callable, Dict
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
