# ./src/scrapers/__init__.py

"""
This module exports the scraper classes.
"""

from .browser_scraper import BrowserScraper
from .http_scraper import HTTPScraper

__all__ = [
    "BrowserScraper",
    "HTTPScraper",
]
