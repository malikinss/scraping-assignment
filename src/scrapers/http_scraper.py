# ./src/scrapers/http_scraper.py

from .deps import (
    httpx,
    asyncio,
    Optional,
    Logger,
    URLUtils,
    settings,
    proxy_manager,
    ScrapeMethod,
    ScrapeResult,
    URL,
)
from .result_builder import ResultBuilder

Response = httpx.Response
Client = httpx.AsyncClient

logger = Logger("HTTPScraper")


class HTTPScraper:
    """
    Asynchronous HTTP scraper using httpx.AsyncClient.

    Handles retries, timeouts, backoff, PDF detection, and structured
    result building via ResultBuilder.

    Attributes:
        timeout (float): Max time to wait for HTTP requests.
        retries (int): Number of retry attempts for failed requests.
        proxy (Optional[str]): Proxy URL for HTTP requests.
    """

    def __init__(self):
        """
        Initialize the HTTPScraper with configuration settings.

        Sets up timeout, retry count, and proxy settings from the
        global settings object.

        Returns:
            None
        """
        self.timeout: float = settings.http_timeout
        self.retries: int = settings.retries
        self.proxy: Optional[str] = proxy_manager.get_httpx_proxy().get(
            settings.protocol
        )

    # ===== CLIENT =====

    def _build_client(self) -> Client:
        """
        Build a new httpx.AsyncClient instance.

        Configures timeout, user-agent, proxy, and redirects.

        Returns:
            Client: Configured AsyncClient instance.
        """
        return Client(
            timeout=self.timeout,
            headers={
                "User-Agent": settings.user_agent,
                "Accept-Language": "en-US,en;q=0.9",
            },
            proxy=self.proxy,
            follow_redirects=True,
        )

    # ===== CORE REQUEST LOGIC =====

    async def _request_with_retry(
        self, client: Client, id: int, url: URL
    ) -> Optional[Response]:
        """
        Make HTTP request with automatic retry logic.

        Handles:
        - Success (200 OK)
        - Retries on failure
        - Exponential backoff
        - Exception handling (timeout, request errors)
        - Logging for each attempt

        Args:
            client (Client): httpx.AsyncClient instance.
            id (int): Unique request identifier.
            url (URL): URL to request.

        Returns:
            Optional[Response]: Response object if successful, None otherwise.
        """
        for attempt in range(1, self.retries + 1):
            if attempt > 1:
                self._log(id, attempt, url, "RETRYING")
            else:
                self._log(id, attempt, url, "START")

            try:
                response = await self._make_request(client, url)

                if self._is_success(response):
                    return response

                self._log_status_failure(id, attempt, url, response)

            except Exception as e:
                self._handle_exception(id, attempt, url, e)

            if attempt < self.retries+1:
                await self._backoff(attempt)

        self._log(id, attempt, url, "ALL RETRIES FAILED", level="error")
        return None

    async def _make_request(self, client: Client, url: URL) -> Response:
        """
        Execute a single HTTP GET request.

        Args:
            client (Client): httpx.AsyncClient instance.
            url (URL): URL to request.

        Returns:
            Response: Response object.
        """
        return await client.get(url)

    def _log_status_failure(
        self, id: int, attempt: int, url: URL, response: Response
    ) -> None:
        """
        Log non-successful HTTP response status codes.

        Args:
            id (int): Unique request identifier.
            attempt (int): Retry attempt number.
            url (URL): Target URL.
            response (Response): Response object with status code.

        Returns:
            None
        """
        self._log(
            id, attempt, url,
            f"STATUS CODE:{response.status_code}", level="warning"
        )

    def _handle_exception(
        self, id: int, attempt: int, url: URL, error: Exception
    ) -> None:
        """
        Handle and log exceptions that occur during HTTP requests.

        Args:
            id (int): Unique request identifier.
            attempt (int): Retry attempt number.
            url (URL): Target URL.
            error (Exception): Exception that occurred.

        Returns:
            None
        """
        if isinstance(error, httpx.TimeoutException):
            self._log(
                id, attempt, url,
                "TIMEOUT", level="warning"
            )
        elif isinstance(error, httpx.RequestError):
            level = "warning" if attempt == self.retries else "debug"
            self._log(
                id, attempt, url,
                f"REQUEST ERROR: {error}", level=level
            )
        else:
            self._log(
                id, attempt, url,
                f"UNEXPECTED ERROR: {error}", level="error"
            )
    # ===== HELPERS =====

    def _log(
        self,
        id: int,
        attempt: int,
        url: URL,
        message: str,
        level: str = "debug",
    ) -> None:
        """
        Centralized logging helper for HTTP scraping.

        Formats log messages consistently with ID, type, URL, attempt,
        and timeout information.

        Args:
            id (int): Unique request identifier.
            attempt (int): Retry attempt number.
            url (URL): Target URL.
            message (str): Message to log.
            level (str, optional): Logging level.

        Returns:
            None
        """
        short_url = URLUtils.short_url(url)
        msg = (
            f"[ID:{id}][HTTP] {message} "
            f"(attempt {attempt}/{self.retries}) "
            f"url={short_url} timeout={self.timeout}s"
        )

        getattr(logger, level)(msg)

    def _is_success(self, response: Response) -> bool:
        """
        Check if HTTP response indicates success.

        Args:
            response (Response): Response object to check.

        Returns:
            bool: True if status code is 200, False otherwise.
        """
        return response.status_code == 200

    async def _backoff(self, attempt: int) -> None:
        """
        Calculate and apply exponential backoff delay.

        Args:
            attempt (int): Current retry attempt number.

        Returns:
            None
        """
        delay = min(2 ** attempt, 10)
        await asyncio.sleep(delay)

    def _is_pdf(self, response: Response) -> bool:
        """
        Check if response is a PDF.

        Args:
            response (Response): Response object to check.

        Returns:
            bool: True if response is a PDF, False otherwise.
        """
        content_type = response.headers.get("Content-Type", "").lower()
        ends_with_pdf = response.url.path.endswith(".pdf")
        is_pdf_content = "application/pdf" in content_type or ends_with_pdf
        return is_pdf_content and URLUtils.is_pdf(response.url)

    # ===== PUBLIC API =====

    async def fetch(self, id: int, url: URL) -> ScrapeResult:
        """
        Fetch a URL and return a structured ScrapeResult.

        Performs retries, handles PDF detection, and builds result via
        ResultBuilder.

        Args:
            id (int): Unique request ID.
            url (URL): URL to scrape.

        Returns:
            ScrapeResult: Structured result with content or error status.
        """
        builder = ResultBuilder(ScrapeMethod.HTTPX)

        try:
            async with self._build_client() as client:
                response = await self._request_with_retry(client, id, url)

            if response is None:
                return builder.build_failure(id, url, "No response")

            if self._is_pdf(response):
                return builder.build_pdf(id, url)

            return builder.process(id, url, response.text)

        except httpx.TimeoutException:
            return builder.build_timeout(id, url)

        except Exception as e:
            return builder.build_failure(id, url, str(e))
