# ./src/config/settings/subsettings/scrapers/deps.py
from src.config.settings.subsettings import FilesSettings
from src.config.settings.subsettings.deps import (
    dataclass, Optional, ProxyManager, Path, get_env
)

Proxy = Optional[dict | str]
proxy_manager = ProxyManager.from_file(Path(FilesSettings.proxy))

__all__ = ["dataclass", "Optional", "proxy_manager", "get_env", "Proxy"]
