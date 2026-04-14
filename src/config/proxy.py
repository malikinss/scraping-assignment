# ./src/config/proxy.py

"""
Proxy configuration and management module.

This module provides:
    - Data model for proxy credentials
    - Proxy configuration loader from file
    - Format converters for different clients (httpx, playwright)

It supports parsing proxy settings from JSON files and exposing them
in formats compatible with different HTTP clients.
"""

from .deps import json, Path, dataclass, AppLogger

logger: AppLogger = AppLogger("Proxy")


@dataclass
class ProxyCredentials:
    """
    Data structure representing proxy authentication credentials.

    Attributes:
        username (str): Proxy username.
        password (str): Proxy password.
        hostname (str): Proxy host address (without port).
        http_port (int): HTTP proxy port.
        https_port (int): HTTPS proxy port.
        socks5_port (int): SOCKS5 proxy port.
    """
    username: str
    password: str
    hostname: str
    http_port: int
    https_port: int
    socks5_port: int


class ProxyManager:
    """
    Manages proxy configuration and provides client-specific formats.

    Responsible for:
        - Loading proxy configuration from JSON file
        - Parsing and validating proxy credentials
        - Providing proxy configs for HTTPX and Playwright

    Attributes:
        credentials (ProxyCredentials): Proxy authentication credentials.
    """

    def __init__(self, credentials: ProxyCredentials):
        """
        Initialize ProxyManager with proxy credentials.

        Args:
            credentials (ProxyCredentials): Proxy authentication credentials.
        """
        self.credentials = credentials

    # ===== FACTORY =====

    @classmethod
    def from_file(cls, path: Path) -> "ProxyManager":
        """
        Create ProxyManager instance from JSON configuration file.

        The file must contain a "proxy" key with required credentials.

        Args:
            path (Path): Path to the JSON configuration file.

        Returns:
            ProxyManager: Initialized ProxyManager instance.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            ValueError: If the configuration file is invalid or missing
                        required fields.
            Exception: For other unexpected errors during loading.
        """
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
        """
        Parse raw proxy dictionary into ProxyCredentials.

        Args:
            proxy (dict): Raw proxy configuration.

        Returns:
            ProxyCredentials: Structured proxy credentials.

        Raises:
            ValueError: If required keys are missing.
        """
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
        """
        Build base proxy URL from credentials.

        Returns:
            str: Base proxy URL in format: http://username:password@hostname
        """
        c = self.credentials
        return f"http://{c.username}:{c.password}@{c.hostname}"

    # ===== PUBLIC API =====

    def get_httpx_proxy(self) -> dict:
        """
        Return proxy configuration compatible with HTTPX.

        Returns:
            dict: HTTPX proxy configuration in format:
                {
                    "http://": "http://username:password@hostname:http_port",
                    "https://": "http://username:password@hostname:https_port"
                }
        """
        c = self.credentials
        base = self._build_base_url()
        return {
            "http://": f"{base}:{c.http_port}",
            "https://": f"{base}:{c.https_port}",
        }

    def get_playwright_proxy(self) -> dict:
        """
        Return proxy configuration compatible with Playwright.

        Returns:
            dict: Playwright proxy configuration in format:
                {
                    "server": "http://username:password@hostname:http_port",
                    "username": "username",
                    "password": "password"
                }
        """
        c = self.credentials
        return {
            "server": f"http://{c.hostname}:{c.http_port}",
            "username": c.username,
            "password": c.password,
        }
