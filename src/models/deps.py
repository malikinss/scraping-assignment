# ./src/models/deps.py

"""
Shared dependencies and type exports for the models subsystem.

This module centralizes commonly used standard library imports,
third-party libraries, and typing primitives used across domain models.

It provides a single re-export layer to reduce repetitive imports
and ensure consistency across the models package.

Warning:
    This module is intended for convenience only and should not contain
    business logic or domain behavior.
"""

import pandas as pd
from enum import Enum
from collections import defaultdict
from dataclasses import dataclass, asdict
from typing import (
    Optional,
    List,
    Dict,
    Callable,
    TypeVar,
    Iterable,
    Iterator,
    NewType,
    TypedDict
)

__all__ = [
    "pd",
    "Enum",
    "defaultdict",
    "dataclass",
    "asdict",
    "Optional",
    "List",
    "Dict",
    "Callable",
    "TypeVar",
    "Iterable",
    "Iterator",
    "NewType",
    "TypedDict"
]
