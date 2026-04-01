# src/config/proxy.py

from .deps import (
    json,
    Path,
    dataclass,
    Logger,
)
from .settings import settings

logger: Logger = Logger(__name__)


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
        Logs:
            - INFO: ProxyManager initialization started.
            - INFO: Proxy credentials loaded successfully.
            - ERROR: Failed to load proxy.
        Example:
            >>> proxy_manager = ProxyManager()
            >>> proxy_manager.get_httpx_proxy()
            {
                "http://": "http://username:password@hostname:http_port",
                "https://": "http://username:password@hostname:https_port",
            }
        """
        logger.debug(
            f"Initializing ProxyManager with file: {settings.proxy_file}"
        )
        try:
            self.credentials: ProxyCredentials = self._load()
            logger.debug(
                f"Proxy credentials loaded for "
                f"hostname={self.credentials.hostname}"
            )
        except Exception as e:
            logger.error(f"Failed to load proxy: {e}")
            raise

    def _load(self) -> ProxyCredentials:
        """
        Load proxy credentials from a JSON file.

        The expected JSON structure:
        {
            "proxy": {
                "username": "...",
                "password": "...",
                "hostname": "...",
                "port": {
                    "http": int,
                    "https": int,
                    "socks5": int
                }
            }
        }

        Returns:
            ProxyCredentials: Parsed and validated proxy credentials.

        Raises:
            FileNotFoundError: If the proxy file does not exist.
            ValueError: If required keys are missing or format is invalid.
            KeyError: If expected fields are missing in the JSON.
        Logs:
            - INFO: Proxy credentials loaded successfully.
            - ERROR: Failed to load proxy.
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
        msg: str = ""

        if not path.exists():
            msg = f"Proxy file not found: {path}"
            logger.error(msg)
            raise FileNotFoundError(msg)

        with path.open("r", encoding="utf-8") as f:
            data: dict = json.load(f)

        if "proxy" not in data:
            msg = "Invalid proxy format: missing 'proxy' key"
            logger.error(msg)
            raise ValueError(msg)

        proxy: dict = data["proxy"]

        username: str = proxy["username"]
        password: str = proxy["password"]
        hostname: str = proxy["hostname"].split(":")[0]
        http_port: int = proxy["port"]["http"]
        https_port: int = proxy["port"]["https"]
        socks5_port: int = proxy["port"]["socks5"]

        logger.info(
            f"Loaded proxy for "
            f"hostname={hostname}, ports: http={http_port}, "
            f"https={https_port}, socks5={socks5_port}"
        )
        return ProxyCredentials(
            username=username,
            password=password,
            hostname=hostname,
            http_port=http_port,
            https_port=https_port,
            socks5_port=socks5_port,
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
            "http://username:password@hostname"
        """
        creds = self.credentials
        return f"http://{creds.username}:{creds.password}@{creds.hostname}"

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
            {
                "http://": "http://username:password@hostname:http_port",
                "https://": "http://username:password@hostname:https_port",
            }
        """
        base_url = self._build_base_url()
        proxies = {
            "http://": f"{base_url}:{self.credentials.http_port}",
            "https://": f"{base_url}:{self.credentials.https_port}",
        }
        logger.debug(f"HTTPX proxies generated: {proxies}")
        return proxies

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
            {
                "server": "http://hostname:http_port",
                "username": "...",
                "password": "...",
            }
        """
        creds = self.credentials
        proxy_dict = {
            "server": f"http://{creds.hostname}:{creds.http_port}",
            "username": creds.username,
            "password": creds.password,
        }
        logger.debug(f"Playwright proxy generated: {proxy_dict}")
        return proxy_dict


proxy_manager = ProxyManager()
