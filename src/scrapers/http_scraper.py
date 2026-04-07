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
)

from .result_builder import ResultBuilder

Response = httpx.Response
Client = httpx.AsyncClient

logger = Logger("HTTPScraper")


class HTTPScraper:
    """
    Asynchronous HTTP scraper with retry, backoff, and PDF detection.

    Uses `httpx.AsyncClient` to fetch URLs with configurable timeout,
    retries, and proxy support. Integrates with `ResultBuilder` to produce
    standardized `ScrapeResult` objects, including SUCCESS, FAILURE,
    TIMEOUT, and PDF responses.
    """

    def __init__(self):
        """
        Initialize the HTTPScraper with timeout, retries, and proxy settings.

        Attributes:
            timeout (float): HTTP request timeout in seconds.
            retries (int): Maximum number of retry attempts.
            proxy (Optional[str]): Proxy URL for HTTP requests.
            client (Client): Async HTTP client instance.
        """
        self.timeout: float = settings.http_timeout
        self.retries: int = settings.retries
        self.proxy: Optional[str] = proxy_manager.get_httpx_proxy().get(
            settings.protocol
        )
        self.client: Client = self._build_client()

    def _build_client(self) -> Client:
        """
        Build an `httpx.AsyncClient` with headers, timeout, proxy,
        and redirects.

        Returns:
            Client: Configured asynchronous HTTP client.
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

    async def _request_with_retry(
        self, id: int, url: str
    ) -> Optional[Response]:
        """
        Perform an HTTP GET request with retry and exponential backoff.

        Args:
            id (int): The scrape ID for logging purposes.
            url (str): The URL to fetch.

        Returns:
            Optional[Response]: The HTTP response if successful; `None`
            otherwise.
        """
        short_url = URLUtils.short_url(url)

        for attempt in range(1, self.retries + 1):
            try:
                log = (
                    f"[ID: {id}] "
                    f"url={short_url} "
                    f"attempt={attempt}/{self.retries}"
                )

                if attempt > 1:
                    logger.debug(f"{log} timeout={self.timeout}")

                response: Response = await self.client.get(url)

                if response.status_code == 200:
                    return response

                logger.warning(f"{log} Non-200 status: {response.status_code}")

            except httpx.TimeoutException:
                logger.warning(f"{log} HTTP timeout")

            except httpx.RequestError as e:
                msg = (
                    f"{log} "
                    f"HTTP request error: "
                    f"error={e if e else "Unknown error"}"
                )
                if attempt == self.retries:
                    logger.warning(msg)
                else:
                    logger.debug(msg)

            if attempt < self.retries:
                await self._backoff(id, attempt)

        logger.error(f"{log}: All retries failed")
        return None

    async def _backoff(self, id: int, attempt: int) -> None:
        """
        Apply exponential backoff delay between retries.

        Args:
            id (int): The scrape ID for logging.
            attempt (int): Current retry attempt number.
        """
        delay: float = min(2 ** attempt, 10)
        if self.retries > 1:
            msg = (
                f"[ID: {id}] "
                f"Backoff: "
                f"attempt={attempt}/{self.retries} "
                f"sleep={delay:.2f}s"
            )
            logger.debug(msg)
        await asyncio.sleep(delay)

    async def close(self) -> None:
        """
        Close the underlying HTTP client and release resources.
        """
        await self.client.aclose()

    def _is_pdf(self, response: Response) -> bool:
        """
        Check if the HTTP response is a PDF document.

        Detection is based on content-type header, URL path, and utility
        function `URLUtils.is_pdf`.

        Args:
            response (Response): The HTTP response object.

        Returns:
            bool: `True` if the response is a PDF, `False` otherwise.
        """
        content_type: str = response.headers.get("Content-Type", "").lower()
        is_pdf = (
            "application/pdf" in content_type
            or response.url.path.endswith(".pdf")
        )
        is_pdf = is_pdf and URLUtils.is_pdf(response.url)
        return is_pdf

    async def fetch(self, id: int, url: str) -> ScrapeResult:
        """
        Fetch a URL and return a standardized `ScrapeResult`.

        Applies retry logic, PDF detection, and response content analysis
        via `ResultBuilder`. Handles exceptions and timeouts gracefully.

        Args:
            id (int): The scrape ID.
            url (str): The URL to fetch.

        Returns:
            ScrapeResult: The result object representing the scrape outcome.
        """
        builder: ResultBuilder = ResultBuilder(ScrapeMethod.HTTPX)

        response: Optional[Response] = None

        try:
            response = await self._request_with_retry(id, url)

            if response is None:
                return builder.build_failure(id, url, "No response")

            if self._is_pdf(response):
                return builder.build_pdf(id, url)

            return builder.process(id, url, response.text)

        except httpx.TimeoutException:
            return builder.build_timeout(id, url)

        except Exception as e:
            return builder.build_failure(id, url, str(e))
