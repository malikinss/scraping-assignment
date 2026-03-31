# ./src/config/__init__.py

"""
Configuration package for the scraping assignment.

This package provides:
    - settings: Global application settings.
    - proxy: Proxy configuration and management.

Exports:
    - settings: Global settings instance.
    - ProxyManager: For managing proxy configurations.
    - ProxyCredentials: For holding proxy credentials.

Usage:
    from src.config import settings, ProxyManager, ProxyCredentials

    settings.load()
    proxy_manager = ProxyManager()
    proxy_creds = ProxyCredentials(...)
"""

from .settings import settings
from .proxy import ProxyManager, ProxyCredentials

__all__ = [
    "settings",
    "ProxyManager",
    "ProxyCredentials",
]
