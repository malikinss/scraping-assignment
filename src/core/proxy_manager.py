import json
from typing import Dict


class ProxyManager:
    """
    Class to manage proxy configurations and provide proxy
    dictionaries for httpx and Playwright.

    Attributes:
        config_path (str): Path to the proxy JSON config.
        config (dict | None): Loaded proxy configuration.
        httpx_proxy (Dict | None): Proxy dict for httpx.
        playwright_proxy (Dict | None): Proxy dict for Playwright.
    """

    def __init__(self, config_path: str):
        """
        Initialize ProxyManager.

        Args:
            config_path (str): Path to the proxy JSON config.
        """
        self.config_path = config_path
        self.config: dict | None = None
        self.httpx_proxy: Dict | None = None
        self.playwright_proxy: Dict | None = None

    def load_config(self) -> None:
        """
        Load the proxy configuration from the JSON file.

        Raises:
            ValueError: If loading fails.
        """
        try:
            with open(self.config_path, "r") as f:
                self.config = json.load(f)
        except Exception as e:
            raise ValueError(f"Failed to load proxy config: {e}")

    def get_hostname(self) -> str:
        """
        Get the proxy hostname.

        Returns:
            str: Proxy hostname.
        """
        return self.config["proxy"]["hostname"].split(":")[0]

    def get_username(self) -> str:
        """
        Get the proxy username.

        Returns:
            str: Proxy username.
        """
        return self.config["proxy"]["username"]

    def get_password(self) -> str:
        """
        Get the proxy password.

        Returns:
            str: Proxy password.
        """
        return self.config["proxy"]["password"]

    def get_port(self, protocol: str) -> int:
        """
        Get the proxy port for a given protocol.

        Args:
            protocol (str): Protocol ("http" or "https").

        Returns:
            int: Port number.
        """
        return self.config["proxy"]["port"][protocol]

    def build_proxy_url(self, port: int) -> str:
        """
        Build a full proxy URL with authentication.

        Args:
            port (int): Port to use.

        Returns:
            str: Proxy URL.
        """
        return f"http://{self.get_username()}:{self.get_password()}" \
            f"@{self.get_hostname()}:{port}"

    def build_httpx_proxy(self) -> None:
        """
        Build the httpx proxy dictionary and store in self.httpx_proxy.
        """
        self.httpx_proxy = {
            "http://": self.build_proxy_url(self.get_port("http")),
            "https://": self.build_proxy_url(self.get_port("https")),
        }

    def build_playwright_proxy(self) -> None:
        """
        Build the Playwright proxy dictionary and store in
        self.playwright_proxy.
        """
        self.playwright_proxy = {
            "server": f"http://{self.get_hostname()}:{self.get_port('https')}",
            "username": self.get_username(),
            "password": self.get_password(),
        }

    def get_httpx_proxy(self) -> Dict:
        """
        Get the httpx proxy dictionary. Loads config if needed.

        Returns:
            Dict: httpx proxy dictionary.
        """
        if self.httpx_proxy is None:
            if self.config is None:
                self.load_config()
            self.build_httpx_proxy()
        return self.httpx_proxy

    def get_playwright_proxy(self) -> Dict:
        """
        Get the Playwright proxy dictionary. Loads config if needed.

        Returns:
            Dict: Playwright proxy dictionary.
        """
        if self.playwright_proxy is None:
            if self.config is None:
                self.load_config()
            self.build_playwright_proxy()
        return self.playwright_proxy
