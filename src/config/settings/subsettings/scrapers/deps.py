# ./src/config/settings/subsettings/scrapers/deps.py
from src.config.settings.subsettings import FilesSettings
from src.config.settings.subsettings.deps import (
    dataclass, Optional, ProxyManager, Path
)

proxy_manager = ProxyManager.from_file(Path(FilesSettings.proxy))
__all__ = ["dataclass", "Optional", "proxy_manager"]
