# ./src/logger/deps.py
import re
import logging
from src.utils import URLUtils
from src.deps import os, Optional
from src.models import Counts, ScraperContext

__all__ = [
    "os",
    "re",
    "logging",
    "Optional",
    "URLUtils",
    "Counts",
    "ScraperContext"
]
