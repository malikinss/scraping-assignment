# ./src/config/__init__.py

"""
Application configuration module.

This module initializes and exposes global configuration objects used
across the application, including runtime settings and proxy management.

It acts as a central entry point for configuration loading:
    - Loads environment-based settings
    - Initializes proxy manager from configuration file
    - Provides ready-to-use singleton-like objects
"""

from .deps import Path
from .settings import Settings
from .proxy import ProxyManager

settings = Settings.from_env()
"""Global application settings loaded from environment variables."""

proxy_manager = ProxyManager.from_file(Path(settings.proxy_file))
"""Global proxy manager initialized from configured proxy file."""

__all__ = ["settings", "proxy_manager"]
