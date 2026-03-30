# ./src/models/__init__.py

"""
This package contains the models used by the application.
"""

from .enums import ScrapeMethod, ScrapeStatus
from .scrape_result import ScrapeResult

__all__ = [
    "ScrapeMethod",
    "ScrapeStatus",
    "ScrapeResult"
]
