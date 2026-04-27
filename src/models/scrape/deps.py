# ./src/models/scrape/deps.py

import pandas as pd
from enum import Enum
from collections import defaultdict
from dataclasses import dataclass, asdict, replace
from typing import (
    Optional,
    List,
    Dict,
    Callable,
    TypeVar,
    Iterable,
    Iterator,
    NewType,
    TypedDict,
    TYPE_CHECKING
)
from src.models.common import URL, URLs

__all__ = [
    "pd",
    "Enum",
    "defaultdict",
    "dataclass", "asdict", "replace",
    "Optional", "List", "Dict", "Callable",
    "TypeVar", "Iterable", "Iterator", "NewType", "TypedDict", "TYPE_CHECKING",
    "URL", "URLs"
]
