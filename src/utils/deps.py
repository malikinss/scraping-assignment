# ./src/utils/deps.py

"""
Dependencies for the utils module.

This module is used to import dependencies for the utils module.
"""

from urllib.parse import urlparse
from typing import NamedTuple
from src.models import URL, URLs

__all__ = ["urlparse", "URL", "URLs", "NamedTuple"]
