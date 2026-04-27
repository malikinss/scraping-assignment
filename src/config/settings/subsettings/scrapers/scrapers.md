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
from .deps import dataclass, Proxy, ProxyManager, get_env

@dataclass
class BrowserSettings:
    timeout: float = 10000.0
    locale: str = "en-US"
    state: str = "networkidle"
    headless: bool = True
    proxy: Proxy = None
    max_concurrency: int = 50

    def __post_init__(self) -> None:
        self._validate()

    @classmethod
    def from_env(cls, proxy_manager: ProxyManager) -> "BrowserSettings":
        return cls(
            timeout=get_env("BROWSER_TIMEOUT", cls.timeout, float),
            locale=get_env("BROWSER_LOCALE", cls.locale, str),
            state=get_env("BROWSER_STATE", cls.state, str),
            headless=get_env("BROWSER_HEADLESS", cls.headless, bool),
            max_concurrency=get_env(
                "BROWSER_MAX_CONCURRENCY", cls.max_concurrency, int),
            proxy=proxy_manager.get_playwright_proxy(),
        )

    # ===== INTERNAL =====
    def _validate(self) -> None:
        if self.timeout <= 0:
            raise ValueError("Browser timeout must be positive")
        if not self.locale:
            raise ValueError("Browser locale cannot be empty")
        if self.state not in ["load", "domcontentloaded", "networkidle"]:
            raise ValueError(
                "Browser state must be 'load', 'domcontentloaded', "
                "or 'networkidle'"
            )
        if self.max_concurrency <= 0:
            raise ValueError("Browser max concurrency must be positive")
```

```py
# ./src/config/settings/subsettings/scrapers/deps.py
from src.config.settings.subsettings.deps import (dataclass, Optional, get_env, ProxyManager)
Proxy = Optional[dict | str]
__all__ = ["dataclass", "Optional", "get_env", "Proxy", "ProxyManager"]
```

```py
# ./src/config/settings/subsettings/scrapers/httpx.py
from .deps import dataclass, Proxy, ProxyManager, get_env

@dataclass
class HTTPXSettings:
    timeout: float = 10.0
    retries: int = 2
    connections: int = 100
    keepalive: int = 20
    redirects: bool = True
    max_concurrency: int = 5
    protocol: str = "https://"
    proxy: Proxy = None

    def __post_init__(self) -> None:
        self._validate()

    @classmethod
    def from_env(cls, proxy_manager: ProxyManager) -> "HTTPXSettings":
        protocol = get_env("HTTPX_PROTOCOL", cls.protocol, str)
        return cls(
            timeout=get_env("HTTPX_TIMEOUT", cls.timeout, float),
            retries=get_env("HTTPX_RETRIES", cls.retries, int),
            connections=get_env("HTTPX_CONNECTIONS", cls.connections, int),
            keepalive=get_env("HTTPX_KEEPALIVE", cls.keepalive, int),
            redirects=get_env("HTTPX_REDIRECTS", cls.redirects, bool),
            max_concurrency=get_env(
                "HTTPX_MAX_CONCURRENCY", cls.max_concurrency, int),
            protocol=protocol,
            proxy=proxy_manager.get_httpx_proxy().get(protocol),
        )

    # ===== INTERNAL =====
    def _validate(self) -> None:
        if self.timeout <= 0:
            raise ValueError("HTTPX timeout must be positive")
        if self.retries < 0:
            raise ValueError("HTTPX retries must be non-negative")
        if self.connections <= 0:
            raise ValueError("HTTPX connections must be positive")
        if self.keepalive <= 0:
            raise ValueError("HTTPX keepalive must be positive")
        if not self.protocol:
            raise ValueError("HTTPX protocol cannot be empty")
        if self.max_concurrency <= 0:
            raise ValueError("HTTPX max concurrency must be positive")
        if self.protocol not in ["http://", "https://"]:
            raise ValueError("HTTPX protocol must be 'http://' or 'https://'")
```
