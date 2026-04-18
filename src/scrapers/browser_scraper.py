# ./src/scrapers/browser_scraper.py

"""
Browser Scraper Module
======================

This module provides an asynchronous browser scraper for fetching content
from URLs. It uses `playwright` for making HTTP requests and supports features
like:

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
    BrowserScraper: Scrapes content from URLs.

Dependencies:
    - playwright: For making HTTP requests.
    - asyncio: For asynchronous programming.
    - src.scrapers.deps: Contains necessary imports for the module.

Example:
    >>> scraper = BrowserScraper()
    >>> result = await scraper.fetch(1, "https://example.com")
    >>> print(result)

    ScrapeResult(
        id='some-id',
        url='https://example.com',
        method='BROWSER',
        status=ScrapeStatus.SUCCESS,
        latency=0.5,
        content='Some content',
        content_length=12,
        error=None
    )
"""

from .deps import (
    Optional,
    Playwright,
    async_playwright,
    Browser,
    Page,
    BrowserContext,
    TimeoutError,
    AppLogger,
    settings,
    proxy_manager,
    ScrapeResult,
    ScraperContext,
    URL,
    AsyncGenerator,
    asynccontextmanager
)

from .result_builder import ResultBuilder

logger = AppLogger("BrowserScraper")
METHOD = "BROWSER"


class BrowserScraper:
    """
    BrowserScraper class for scraping content from URLs using Playwright.

    Attributes:
        timeout (int): The timeout for browser operations.
        browser (Optional[Browser]): The browser instance.
        playwright (Optional[Playwright]): The playwright instance.
        proxy (Optional[dict]): The proxy for browser operations.
    """

    def __init__(self) -> None:
        """
        Creates an instance of BrowserScraper.
        """
        self.timeout: int = settings.browser_timeout
        self.browser: Optional[Browser] = None
        self.playwright: Optional[Playwright] = None
        self.proxy: Optional[dict] = proxy_manager.get_playwright_proxy()

    # ===== LIFECYCLE =====

    async def launch(self) -> None:
        """
        Launches the browser for browser operations.
        """
        if self.browser:
            return

        self.playwright: Playwright = await async_playwright().start()
        self.browser: Browser = await self.playwright.chromium.launch(
            headless=True,
            proxy=self.proxy,
        )

    async def close_browser(self) -> None:
        """
        Closes the browser for browser operations.
        """
        if self.browser:
            await self.browser.close()
            self.browser = None

        if self.playwright:
            await self.playwright.stop()
            self.playwright = None

    async def _ensure_browser(self) -> None:
        """
        Ensures the browser is launched for browser operations.
        """
        if not self.browser:
            await self.launch()

    # ===== CONTEXT MANAGEMENT =====

    async def _create_context(self) -> BrowserContext:
        """
        Creates a new browser context for browser operations.

        Returns:
            BrowserContext: The new browser context.
        """
        await self._ensure_browser()

        context: BrowserContext = await self.browser.new_context(
            user_agent=settings.user_agent,
            locale="en-US",
        )
        return context

    @asynccontextmanager
    async def _page(self) -> AsyncGenerator[Page, None]:
        """
        Creates a new page for browser operations.

        Returns:
            AsyncGenerator[Page, None]: The new page and its context.
        """
        context: BrowserContext = await self._create_context()
        page: Page = await context.new_page()
        try:
            yield page
        finally:
            await self._cleanup(page, context)

    async def _cleanup(
        self, page: Optional[Page], context: Optional[BrowserContext]
    ) -> None:
        """
        Cleans up the browser context and page.

        Args:
            page (Optional[Page]): The page to clean up.
            context (Optional[BrowserContext]): The context to clean up.
        """
        if page:
            await page.close()
        if context:
            await context.close()

    # ===== CORE =====

    async def fetch(self, id: int, url: URL) -> ScrapeResult:
        """
        Fetches content from a URL using browser operations.

        Args:
            id (int): The ID of the scraper request.
            url (URL): The URL to fetch.

        Returns:
            ScrapeResult: The result of the browser operations.
        """
        ctx: ScraperContext = ScraperContext(
            id=id,
            method=METHOD,
            url=url,
            timeout=self.timeout
        )

        builder: ResultBuilder = ResultBuilder()
        logger.scraper.start(ctx)

        try:
            async with self._page() as page:
                content: Optional[str] = await self._get_content(ctx, page)

            if content is None:
                return builder.empty(ctx)

            return builder.process(ctx, content)

        except TimeoutError:
            return builder.timeout(ctx)

        except Exception as e:
            return builder.failure(ctx, str(e))

    # ===== PAGE PROCESSING =====

    async def _get_content(
        self,
        ctx: ScraperContext,
        page: Page
    ) -> Optional[str]:
        """
        Fetches content from a URL using browser operations.

        Args:
            ctx (ScraperContext): The scraper context.
            page (Page): The page to fetch content from.

        Returns:
            Optional[str]: The content from the page.
        """
        try:
            await page.goto(ctx.url, timeout=ctx.timeout)
            await page.wait_for_load_state("networkidle")
            await self._smart_wait(page)
            content: Optional[str] = await page.content()
            length: int = len(content) if content else 0
            msg: str = f"CONTENT_LOADED length={length}"
            logger.scraper.event(ctx, msg, "debug")
            return content

        except TimeoutError:
            logger.scraper.timeout(ctx)
            return None
        except Exception as e:
            logger.scraper.request_error(ctx, str(e))
            return None

    async def _smart_wait(self, page: Page) -> None:
        """
        Waits for the page to load using smart wait.

        Args:
            page (Page): The page to wait for.
        """
        delay: int = max(300, min(self.timeout // 2, 2000))
        await page.wait_for_timeout(delay)
