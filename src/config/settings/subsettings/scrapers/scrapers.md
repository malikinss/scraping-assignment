###### ./src/config/settings/subsettings/scrapers/

- Structure:

```text
./src/config/settings/subsettings/scraper
|
├── __init__.py # imports scrapers settings
├── deps.py     # common imports dataclass and proxy_manager
├── browser.py  # browser settings
└─── httpx.py   # httpx settings
```

- Implementation:

```py
# ./src/config/settings/subsettings/scrapers/__init__.py
from .browser import BrowserSettings
from .httpx import HTTPXSettings
__all__ = ["BrowserSettings", "HTTPXSettings"]
```

```py
# ./src/config/settings/subsettings/scrapers/browser.py
from .deps import dataclass, Optional, proxy_manager

@dataclass
class BrowserSettings:
    timeout: float = 10000.0
    locale: str = "en-US"
    state: str = "networkidle"
    headless: bool = True
    proxy: Optional[str] = proxy_manager.get_proxy("browser")
```

```py
# ./src/config/settings/subsettings/scrapers/deps.py
from src.config.settings.subsettings import FilesSettings
from src.config.settings.subsettings.deps import dataclass, Optional, ProxyManager, Path
proxy_manager = ProxyManager.from_file(Path(FilesSettings.proxy))
__all__ = ["dataclass", "Optional", "proxy_manager"]
```

```py
# ./src/config/settings/subsettings/scrapers/httpx.py
from .deps import dataclass, Optional, proxy_manager

@dataclass
class HTTPXSettings:
    timeout: float = 10.0
    retries: int = 2
    connections: int = 100
    keepalive: int = 20
    redirects: bool = True
    max_concurrency: int = 5
    protocol: str = "https://"
    proxy: Optional[str] = proxy_manager.get_proxy("http")
```
