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
