# ./src/config/settings/subsettings/scrapers/__init__.py

from .browser import BrowserSettings
from .httpx import HTTPXSettings

__all__ = ["BrowserSettings", "HTTPXSettings"]
