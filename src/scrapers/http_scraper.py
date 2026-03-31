# ./src/scrapers/http_scraper.py

from .deps import (
    httpx,
    asyncio,
    Optional,
    Logger,
    settings,
    proxy_manager,
    ScrapeMethod,
    ScrapeResult,
)

from .result_builder import ResultBuilder

logger = Logger(__name__)


class HTTPScraper:
    """
    Asynchronous HTTP scraper with retry, backoff, and response classification.

    This class uses `httpx.AsyncClient` to fetch URLs, handles retries with
    exponential backoff, detects PDFs, and constructs standardized
    `ScrapeResult` objects using `ResultBuilder`.

    Attributes:
        timeout (float): Request timeout in seconds.
        retries (int): Number of retry attempts on failure.
        proxy (Optional[str]): HTTP proxy URL if configured.
        client (httpx.AsyncClient): Async HTTP client instance.
    """

    def __init__(self):
        """
        Initialize the HTTP scraper with settings and proxy.

        Returns:
            None

        Logs:
            - Debug message with the following format:
                HTTPScraper initialized (timeout=..., retries=..., proxy=...)
        """
        self.timeout: float = settings.http_timeout
        self.retries: int = settings.retries
        self.proxy: Optional[str] = proxy_manager.get_httpx_proxy().get(
            settings.protocol
        )
        print()
        self.client: httpx.AsyncClient = self._build_client()
        logger.debug(
            f"HTTPScraper initialized (timeout={self.timeout}, "
            f"retries={self.retries}, proxy={self.proxy})"
        )

    def _build_client(self) -> httpx.AsyncClient:
        """
        Create and configure the asynchronous HTTP client.

        Returns:
            httpx.AsyncClient: Configured async client with headers,
                timeout, proxy, and redirect handling.

        Logs:
            - Debug message with the following format:
                Building HTTP client
        """
        logger.debug("Building HTTP client")
        return httpx.AsyncClient(
            timeout=self.timeout,
            headers={
                "User-Agent": settings.user_agent,
                "Accept-Language": "en-US,en;q=0.9",
            },
            proxy=self.proxy,
            follow_redirects=True,
        )

    async def _request_with_retry(self, url: str) -> Optional[httpx.Response]:
        """
        Perform an HTTP GET request with retries and backoff.

        Args:
            url (str): URL to fetch.

        Returns:
            Optional[httpx.Response]: HTTP response if successful,
                                      otherwise None.

        Notes:
            - Retries on non-200 responses, timeouts, and request errors.
            - Applies exponential backoff between attempts.

        Logs:
            - Debug message with the following format:
                Requesting {url} (attempt {attempt})
            - Debug message with the following format:
                Received 200 OK: {url} (attempt {attempt})
            - Warning message with the following format:
                Non-200 status: {status_code} url=... attempt=...
            - Warning message with the following format:
                Timeout on attempt {attempt} url=...
            - Warning message with the following format:
                Request error on attempt {attempt} url=...: {e}
            - Error message with the following format:
                All retries failed for {url}
        """
        for attempt in range(self.retries + 1):
            try:
                logger.debug(f"Requesting {url} (attempt {attempt})")
                response: httpx.Response = await self.client.get(url)

                if response.status_code == 200:
                    logger.debug(f"Received 200 OK: {url} (attempt {attempt})")
                    return response

                logger.warning(
                    f"Non-200 status: {response.status_code} url={url} "
                    f"attempt={attempt}"
                )

            except httpx.TimeoutException:
                logger.warning(
                    f"Timeout on attempt {attempt} url={url}"
                )

            except httpx.RequestError as e:
                logger.warning(
                    f"Request error on attempt {attempt} url={url}: {e}"
                )

            if attempt < self.retries:
                await self._backoff(attempt)

        logger.error(f"All retries failed for {url}")
        return None

    async def _backoff(self, attempt: int) -> None:
        """
        Apply exponential backoff before retrying a request.

        Args:
            attempt (int): Current retry attempt (0-based).

        Notes:
            - Delay is min(2 ** attempt, 10) seconds.

        Logs:
            - Debug message with the following format:
                Backoff: sleeping {delay:.2f}s before next attempt
        """
        delay: float = min(2 ** attempt, 10)
        logger.debug(f"Backoff: sleeping {delay:.2f}s before next attempt")
        await asyncio.sleep(delay)

    async def close(self) -> None:
        """
        Close the HTTP client and release resources.

        Logs:
            - Debug message with the following format:
                HTTP client closed
        """
        await self.client.close()
        logger.debug("HTTP client closed")

    def _is_pdf(self, response: httpx.Response) -> bool:
        """
        Check if the HTTP response contains a PDF.

        Args:
            response (httpx.Response): HTTP response to check.

        Returns:
            bool: True if the response is a PDF, False otherwise.

        Logs:
            - Debug message with the following format:
                PDF detected: {response.url}
        """
        content_type: str = response.headers.get("Content-Type", "").lower()
        is_pdf = (
            "application/pdf" in content_type
            or response.url.path.endswith(".pdf")
        )

        if is_pdf:
            logger.debug(f"PDF detected: {response.url}")

        return is_pdf

    async def fetch(self, url: str) -> ScrapeResult:
        """
        Fetch a URL asynchronously and return a standardized scrape result.

        Handles retries, PDF detection, timeouts, and unexpected errors.

        Args:
            url (str): URL to fetch.

        Returns:
            ScrapeResult: Result object describing the outcome of the request.

        Logs:
            - Info message with the following format:
                Starting fetch: {url}
            - Warning message with the following format:
                No response received: {url}
            - Exception message with the following format:
                Unexpected error during fetch: {url}: {e}
        """
        logger.info(f"Starting fetch: {url}")
        builder: ResultBuilder = ResultBuilder(ScrapeMethod.HTTPX)

        response: Optional[httpx.Response] = None

        try:
            response = await self._request_with_retry(url)

            if response is None:
                logger.warning(f"No response received: {url}")
                return builder.build_failure(url, "No response")

            if self._is_pdf(response):
                return builder.build_pdf(url)

            text = response.text

            return builder.process(url, text)

        except httpx.TimeoutException:
            logger.warning(f"Fetch timeout: {url}")
            return builder.build_timeout(url)

        except Exception as e:
            logger.exception(f"Unexpected error during fetch: {url}")
            return builder.build_failure(url, str(e))
