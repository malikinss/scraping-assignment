# ./src/services/metrics/deps.py

"""
This module contains the dependencies for the metrics service.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Any
from collections import defaultdict
from src.utils.logger import Logger
from src.models import ScrapeResult, ScrapeMethod, ScrapeStatus

__all__ = [
    "np",
    "dataclass",
    "List",
    "Dict",
    "Any",
    "defaultdict",
    "Logger",
    "ScrapeResult",
    "ScrapeMethod",
    "ScrapeStatus",
]
