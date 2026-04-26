# ./src/scrapers/__init__.py
from .http import HTTPScraper
from .browser import BrowserScraper
__all__ = ["HTTPScraper", "BrowserScraper"]
