# src/config/proxy.py

from .settings import settings
from .deps import json, Path, dataclass, Logger

logger: Logger = Logger("Proxy")


@dataclass
class ProxyCredentials:
    """
    Data class representing proxy authentication and connection details.

    Attributes:
        username (str): Username for proxy authentication.
        password (str): Password for proxy authentication.
        hostname (str): Proxy server hostname or IP address.
        http_port (int): Port for HTTP connections.
        https_port (int): Port for HTTPS connections.
        socks5_port (int): Port for SOCKS5 connections.
    """
    username: str
    password: str
    hostname: str
    http_port: int
    https_port: int
    socks5_port: int


class ProxyManager:
    """
    Manager for loading and providing proxy configurations.

    This class is responsible for:
        - Loading proxy credentials from a JSON file.
        - Validating proxy configuration structure.
        - Providing formatted proxy settings for different clients
          (e.g., httpx, Playwright).

    Raises:
        FileNotFoundError: If the proxy file does not exist.
        ValueError: If the proxy file format is invalid.
        Exception: For any unexpected loading/parsing errors.
    """

    def __init__(self):
        """
        Initialize the ProxyManager and load proxy credentials.

        Raises:
            Exception: If proxy credentials cannot be loaded.
        Example:
            >>> proxy_manager = ProxyManager()
            >>> proxy_manager.get_httpx_proxy()
            {
                "http://": "http://username:password@hostname:http_port",
                "https://": "http://username:password@hostname:https_port",
            }
        """
        try:
            self.credentials: ProxyCredentials = self._load()
        except Exception as e:
            logger.error(f"Failed to initialize proxy manager: {e}")
            raise

    def _load(self) -> ProxyCredentials:
        """
        Load proxy credentials from a JSON file.

        Returns:
            ProxyCredentials: Parsed and validated proxy credentials.

        Raises:
            FileNotFoundError: If the proxy file does not exist.
            ValueError: If required keys are missing or format is invalid.
            KeyError: If expected fields are missing in the JSON.
        Example:
            >>> proxy_manager = ProxyManager()
            >>> proxy_manager._load()
            ProxyCredentials(
                username='username',
                password='password',
                hostname='hostname',
                http_port=http_port,
                https_port=https_port,
                socks5_port=socks5_port,
            )
        """
        path: Path = Path(settings.proxy_file)

        if not path.exists():
            raise FileNotFoundError(f"Proxy file not found: {path}")
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)

            proxy = data.get("proxy")
            if not proxy:
                raise ValueError("Missing 'proxy' key in config")

            return self._parse_proxy(proxy)

        except KeyError as e:
            raise ValueError(f"Missing required proxy field: {e}") from e
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in proxy file: {e}") from e

    def _parse_proxy(self, proxy: dict) -> ProxyCredentials:
        """
        Parse and validate proxy credentials.

        Args:
            proxy (dict): Proxy configuration dictionary.

        Returns:
            ProxyCredentials: Parsed and validated proxy credentials.

        Raises:
            ValueError: If required keys are missing or format is invalid.
            KeyError: If expected fields are missing in the JSON.
        Example:
            >>> proxy_manager = ProxyManager()
            >>> proxy_manager._parse_proxy(proxy_manager._load())
            ProxyCredentials(
                username='username',
                password='password',
                hostname='hostname',
                http_port=http_port,
                https_port=https_port,
                socks5_port=socks5_port,
            )
        """
        hostname: str = proxy["hostname"].split(":")[0]
        logger.info(f"Loaded proxy for hostname={hostname}")
        return ProxyCredentials(
            username=proxy["username"],
            password=proxy["password"],
            hostname=hostname,
            http_port=proxy["port"]["http"],
            https_port=proxy["port"]["https"],
            socks5_port=proxy["port"]["socks5"],
        )

    def _build_base_url(self) -> str:
        """
        Build the base proxy URL with authentication credentials.

        Returns:
            str: Proxy URL in the format:
                "http://username:password@hostname"
        Example:
            >>> proxy_manager = ProxyManager()
            >>> proxy_manager._build_base_url()
        """
        c = self.credentials
        return f"http://{c.username}:{c.password}@{c.hostname}"

    def get_httpx_proxy(self) -> dict:
        """
        Get HTTPX proxy configuration.

        Returns:
            dict: HTTPX proxy configuration in the format:
                {
                    "http://": "http://username:password@hostname:http_port",
                    "https://": "http://username:password@hostname:https_port",
                }
        Example:
            >>> proxy_manager = ProxyManager()
            >>> proxy_manager.get_httpx_proxy()
        """
        base = self._build_base_url()
        c = self.credentials
        return {
            "http://": f"{base}:{c.http_port}",
            "https://": f"{base}:{c.https_port}",
        }

    def get_playwright_proxy(self) -> dict:
        """
        Get Playwright proxy configuration.

        Returns:
            dict: Playwright proxy configuration in the format:
                {
                    "server": "http://hostname:http_port",
                    "username": "...",
                    "password": "...",
                }
        Example:
            >>> proxy_manager = ProxyManager()
            >>> proxy_manager.get_playwright_proxy()
        """
        c = self.credentials
        return {
            "server": f"http://{c.hostname}:{c.http_port}",
            "username": c.username,
            "password": c.password,
        }


proxy_manager = ProxyManager()
