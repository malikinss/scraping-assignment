# ./src/services/content_detector/deps.py

"""
Dependencies for the ContentDetector service.

Imports:
    - Tuple: For type hinting.
    - dataclass: For creating dataclasses.
    - ScrapeStatus: For scrape status enum.
"""

from typing import Tuple
from dataclasses import dataclass
from src.models import ScrapeStatus

__all__ = ["ScrapeStatus", "Tuple", "dataclass"]
