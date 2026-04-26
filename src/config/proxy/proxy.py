# ./src/config/proxy/proxy.py
from .deps import json, Path, logger, Optional
from .credentials import ProxyCredentials


class ProxyManager:
    def __init__(self, credentials: ProxyCredentials):
        self.credentials = credentials

    # ===== FACTORY ====
    @classmethod
    def from_file(cls, path: Path) -> "ProxyManager":
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)

            proxy = data.get("proxy")
            if not proxy:
                raise ValueError("Missing 'proxy' key in config")

            credentials = cls._parse_proxy(proxy)
            logger.pipeline.proxy_success(credentials.hostname)
            return cls(credentials)

        except Exception as e:
            logger.pipeline.proxy_fail(e)
            raise

    # ===== INTERNAL =====
    @staticmethod
    def _parse_proxy(proxy: dict) -> ProxyCredentials:
        try:
            hostname = proxy["hostname"].split(":")[0]

            return ProxyCredentials(
                username=proxy["username"],
                password=proxy["password"],
                hostname=hostname,
                http_port=proxy["port"]["http"],
                https_port=proxy["port"]["https"],
                socks5_port=proxy["port"]["socks5"],
            )
        except KeyError as e:
            raise ValueError(f"Invalid proxy config: missing {e}") from e

    def _build_base_url(self) -> str:
        c = self.credentials
        return f"http://{c.username}:{c.password}@{c.hostname}"

    # ===== PUBLIC API =====
    def get_httpx_proxy(self) -> dict:
        c = self.credentials
        base = self._build_base_url()
        return {
            "http://": f"{base}:{c.http_port}",
            "https://": f"{base}:{c.https_port}",
        }

    def get_playwright_proxy(self) -> dict:
        c = self.credentials
        return {
            "server": f"http://{c.hostname}:{c.http_port}",
            "username": c.username,
            "password": c.password,
        }

    def get_proxy(
        self, method: str, protocol="https://"
    ) -> Optional[dict | str]:
        method = method.lower()
        proxy_map = {
            "http": self.get_httpx_proxy().get(protocol),
            "browser": self.get_playwright_proxy(),
        }
        proxy = proxy_map.get(method)
        if proxy is None:
            logger.scraper.no_proxy(method)
        return proxy
