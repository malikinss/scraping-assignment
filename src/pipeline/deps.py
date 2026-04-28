# ./src/pipeline/deps.py
from typing import Optional
from src.config import settings
from src.logger import AppLogger
from src.models import ScrapeResults, URLs

__all__ = [
    "Optional",
    "ScrapeResults",
    "URLs",
    "AppLogger",
    "settings"
]
