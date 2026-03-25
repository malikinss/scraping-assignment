import time
from typing import Dict, Optional
import httpx


class LightweightScraper:
    """
    Lightweight HTTP scraper using httpx with optional proxy support.

    Attributes:
        proxy (Optional[str]): HTTP proxy URL.
        timeout (int): Request timeout in seconds.
        headers (Dict): Default HTTP headers.
    """

    def __init__(self, proxy: Optional[Dict] = None, timeout: int = 10):
        """
        Initialize the scraper.

        Args:
            proxy (Optional[Dict]): Dictionary with "http://" proxy URL.
            timeout (int): Request timeout in seconds.
        """
        self.proxy = proxy.get("http://") if proxy else None
        self.timeout = timeout
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

    def _build_client(self) -> httpx.Client:
        """
        Build and return an httpx client with proxy and headers.

        Returns:
            httpx.Client: Configured HTTP client.
        """
        return httpx.Client(
            proxy=self.proxy,
            timeout=self.timeout,
            headers=self.headers,
            follow_redirects=True,
        )

    def fetch(self, url: str) -> Dict:
        """
        Fetch a URL and return response metadata and HTML content.

        Args:
            url (str): URL to fetch.

        Returns:
            Dict: Dictionary with status, HTML, latency, and more.
        """
        start_time = time.time()
        try:
            with self._build_client() as client:
                response = client.get(url)

            latency = time.time() - start_time
            return self._handle_response(response, latency)

        except Exception as e:
            latency = time.time() - start_time
            return self._handle_error(e, latency)

    def _handle_response(
        self, response: httpx.Response, latency: float
    ) -> Dict:
        """
        Format successful response.

        Args:
            response (httpx.Response): Response object.
            latency (float): Time taken for the request.

        Returns:
            Dict: Structured response data.
        """
        return {
            "status": "success" if response.status_code == 200 else "error",
            "status_code": response.status_code,
            "html": response.text,
            "latency": latency,
            "content_length": len(response.text),
            "method": "httpx",
        }

    def _handle_error(self, error: Exception, latency: float) -> Dict:
        """
        Format error response.

        Args:
            error (Exception): Raised exception.
            latency (float): Time elapsed until error.

        Returns:
            Dict: Structured error data.
        """
        return {
            "status": "error",
            "error": str(error),
            "html": None,
            "latency": latency,
            "content_length": 0,
            "method": "httpx",
        }
