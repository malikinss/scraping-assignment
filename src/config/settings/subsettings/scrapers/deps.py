# ./src/config/settings/subsettings/scrapers/deps.py
from src.config.settings.subsettings.deps import (
    dataclass, Optional, get_env, ProxyManager)
Proxy = Optional[dict | str]
__all__ = ["dataclass", "Optional", "get_env", "Proxy", "ProxyManager"]
