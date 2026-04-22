# ./src/scrapers/http_scraper.py

"""
HTTP Scraper Module
===================

This module provides an asynchronous HTTP scraper for fetching content
from URLs.
It uses `httpx` for making HTTP requests and supports features like:

- Automatic retry logic
- Proxy support
- Timeout handling
- PDF detection
- Logging for each request

Key Features:
    - Async request handling
    - Retry mechanism with exponential backoff
    - PDF content detection
    - Proxy support

Classes:
    HTTPScraper: Scrapes content from URLs.

Dependencies:
    - httpx: For making HTTP requests.
    - asyncio: For asynchronous programming.
    - src.scrapers.deps: Contains necessary imports for the module.

Example:
    >>> scraper = HTTPScraper()
    >>> result = await scraper.fetch(1, "https://example.com")
    >>> print(result)

    ScrapeResult(
        id='some-id',
        url='https://example.com',
        method='GET',
        status=ScrapeStatus.SUCCESS,
        latency=0.5,
        content='Some content',
        content_length=12,
        error=None
    )
"""

from .deps import (
    httpx,
    asyncio,
    Optional,
    AppLogger,
    URLUtils,
    settings,
    proxy_manager,
    ScrapeResult,
    ScraperContext,
    URL,
)
from .result_builder import ResultBuilder

METHOD = "HTTP"
Response = httpx.Response
Client = httpx.AsyncClient

logger = AppLogger("HTTPScraper")


class HTTPScraper:
    """
    HTTPScraper class for scraping HTTP content.
    """

    def __init__(self):
        """
        Initialize the HTTPScraper.

        Creates an instance of HTTPScraper.

        Attributes:
            timeout (float): The timeout for HTTP requests.
            retries (int): The number of retries for HTTP requests.
            proxy (Optional[str]): The proxy for HTTP requests.
            client (Optional[Client]): The HTTP client.
        """
        self.timeout: float = settings.http_timeout
        self.retries: int = settings.retries
        self.proxy: Optional[str] = self._init_proxy()
        self.client: Optional[Client] = None

    def _init_proxy(self) -> Optional[str]:
        """
        Initializes the proxy for HTTP requests.

        Creates an instance of proxy for HTTP requests.

        Returns:
            Optional[str]: The proxy for HTTP requests.
        """
        proxy = proxy_manager.get_httpx_proxy().get(settings.protocol)

        if proxy is None:
            logger.scraper.no_proxy(METHOD)

        return proxy

    # ===== CLIENT =====

    def _build_client(self):
        """
        Builds an HTTP client with retry logic
        """
        self.client = Client(
            timeout=self.timeout,
            headers={
                "User-Agent": settings.user_agent,
                "Accept-Language": "en-US,en;q=0.9",
            },
            proxy=self.proxy,
            follow_redirects=True,
        )

    # ===== CORE REQUEST =====

    async def _request_with_retry(
            self, base_ctx: ScraperContext) -> Optional[Response]:
        """
        Requests a URL with retry logic.

        Args:
            base_ctx (ScraperContext): The base scraper context.

        Returns:
            Optional[Response]: The response from the request.
        """
        self._build_client()

        for attempt in range(1, base_ctx.retries + 1):
            ctx: ScraperContext = base_ctx.with_updates(attempt=attempt)

            self._start_or_retry(ctx)

            try:
                response = await self.client.get(ctx.url)

                if self._is_success(response):
                    logger.scraper.success(ctx)
                    return response

                logger.scraper.fail(ctx, status=response.status_code)

            except Exception as e:
                self._handle_exception(e, ctx)

            if attempt < base_ctx.retries:
                await self._backoff(attempt)

        logger.scraper.all_failed(ctx)
        return None

    def _start_or_retry(self, ctx: ScraperContext) -> None:
        """
        Logs the start or retry of a request.

        Args:
            ctx (ScraperContext): The scraper context.
        """
        if ctx.attempt == 1:
            logger.scraper.start(ctx)
        else:
            logger.scraper.retry(ctx)

    # ===== EXCEPTION HANDLING =====

    def _handle_exception(self, error: Exception, ctx: ScraperContext) -> None:
        """
        Handles exceptions that occur during a request.

        Args:
            error (Exception): The exception to handle.
            ctx (ScraperContext): The scraper context.
        """
        ctx_error = ctx.with_updates(error=str(error))
        if isinstance(error, httpx.TimeoutException):
            logger.scraper.timeout(ctx_error)
        elif isinstance(error, httpx.RequestError):
            logger.scraper.request_error(ctx_error, str(error))
        else:
            logger.scraper.exception(ctx_error, str(error))

    # ===== HELPERS =====

    def _is_success(self, response: Response) -> bool:
        """
        Checks if the response is successful.

        Args:
            response (Response): The response to check.

        Returns:
            bool: True if the response is successful, False otherwise.
        """
        return response.status_code == 200

    async def _backoff(self, attempt: int) -> None:
        """
        Waits for a backoff period before the next retry.

        Args:
            attempt (int): The current attempt number.
        """
        delay = min(2 ** attempt, 10)
        await asyncio.sleep(delay)

    def _is_pdf(self, response: Response) -> bool:
        """
        Checks if the response is a PDF.

        Args:
            response (Response): The response to check.

        Returns:
            bool: True if the response is a PDF, False otherwise.
        """
        content_type = response.headers.get("Content-Type", "").lower()
        ends_with_pdf = response.url.path.endswith(".pdf")
        is_pdf_content = "application/pdf" in content_type or ends_with_pdf
        return is_pdf_content and URLUtils.is_pdf(response.url)

    # ===== PUBLIC API =====

    async def fetch(self, id: int, url: URL) -> ScrapeResult:
        """
        Fetches the content of a URL.

        Args:
            id (int): The ID of the scrape.
            url (URL): The URL to scrape.

        Returns:
            ScrapeResult: The result of the scrape.
        """
        builder: ResultBuilder = ResultBuilder()
        base_ctx: ScraperContext = ScraperContext(
            id=id,
            method=METHOD,
            url=url,
            timeout=self.timeout,
            retries=self.retries,
        )

        try:
            response = await self._request_with_retry(base_ctx)

            if response is None:
                return builder.failure(base_ctx, "No response")

            if self._is_pdf(response):
                return builder.pdf(base_ctx)

            return builder.process(base_ctx, response.text)

        except httpx.TimeoutException:
            return builder.timeout(base_ctx)

        except Exception as e:
            return builder.failure(base_ctx, str(e))
