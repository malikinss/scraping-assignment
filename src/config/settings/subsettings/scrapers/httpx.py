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
