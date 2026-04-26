# ./src/services/results/saver/savers/deps.py

# ===== STD LIB =====
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Callable, Any, IO

# ===== INTERNAL =====
from src.services.results.saver.deps import (
    AppLogger, ScrapeResult, ScrapeResults
)

__all__ = [
    "Path",
    "ABC",
    "abstractmethod",
    "List",
    "Callable",
    "Any",
    "IO",
    "AppLogger",
    "ScrapeResult",
    "ScrapeResults"
]
