# ./src/models/scrape/deps.py

import pandas as pd
from enum import Enum
from collections import defaultdict
from dataclasses import dataclass, asdict, replace
from typing import List, Dict
from typing import Optional, Callable, Iterable, Iterator
from typing import TypeVar, TYPE_CHECKING
from src.models.common import URL

__all__ = [
    "pd",
    "Enum",
    "defaultdict",
    "dataclass", "asdict", "replace",
    "Optional", "List", "Dict", "Callable",
    "TypeVar", "Iterable", "Iterator", "TYPE_CHECKING",
    "URL"
]
