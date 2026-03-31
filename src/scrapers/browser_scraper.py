# ./src/scrapers/browser_scraper.py

from .deps import (
    Optional,
    Playwright,
    async_playwright,
    Browser,
    Page,
    BrowserContext,
    TimeoutError,
    Logger,
    settings,
    proxy_manager,
    ScrapeMethod,
    ScrapeResult,
)

from .result_builder import ResultBuilder

logger = Logger(__name__)


class BrowserScraper:
    """
    Asynchronous browser-based scraper using Playwright.

    This class manages launching a headless Chromium browser, creating contexts
    and pages, navigating to URLs, and returning standardized `ScrapeResult`
    objects using `ResultBuilder`. Handles timeouts, errors, and page cleanup.

    Attributes:
        timeout (int): Maximum timeout for browser operations in milliseconds.
        browser (Optional[Browser]): Playwright Browser instance.
        playwright (Optional[Playwright]): Playwright controller.
        proxy (Optional[dict]): Proxy configuration for browser context.
    """

    def __init__(self) -> None:
        """
        Initialize BrowserScraper with settings and optional proxy.

        Sets up timeout, initializes browser/playwright to None, and retrieves
        proxy configuration from `proxy_manager`.

        Returns:
            None

        Raises:
            RuntimeError: If browser is not initialized.

        Logs:
            - Debug: BrowserScraper initialized with timeout and proxy.

        Examples:
            >>> scraper = BrowserScraper()
            >>> await scraper.launch()
            >>> await scraper.close_browser()
        """
        print()
        self.timeout: int = settings.browser_timeout
        self.browser: Optional[Browser] = None
        self.playwright: Optional[Playwright] = None
        self.proxy: Optional[dict] = proxy_manager.get_playwright_proxy()

        logger.debug(
            f"BrowserScraper initialized (timeout={self.timeout}ms, "
            f"proxy={self.proxy})"
        )

    async def launch(self) -> None:
        """
        Launch Playwright and the headless Chromium browser.

        Notes:
            - Must be called before fetching any pages.
            - Initializes `self.playwright` and `self.browser`.

        Returns:
            None

        Logs:
            - Info: Launching BrowserScraper
            - Debug: Browser launched successfully

        Examples:
            >>> scraper = BrowserScraper()
            >>> await scraper.launch()
        """
        logger.info("Launching BrowserScraper")
        self.playwright: Playwright = await async_playwright().start()

        self.browser: Browser = await self.playwright.chromium.launch(
            headless=True,
            proxy=self.proxy,
        )
        logger.debug("Browser launched successfully")

    async def close_browser(self) -> None:
        """
        Close the browser and stop the Playwright instance.

        Returns:
            None

        Logs:
            - Debug: Closing BrowserScraper
            - Debug: Browser closed successfully
            - Debug: Playwright stopped successfully

        Examples:
            >>> scraper = BrowserScraper()
            >>> await scraper.launch()
            >>> await scraper.close_browser()
        """
        logger.debug("Closing BrowserScraper")
        if self.browser:
            await self.browser.close()
            logger.debug("Browser closed successfully")
        if self.playwright:
            await self.playwright.stop()
            logger.debug("Playwright stopped successfully")

    async def _create_context(self) -> BrowserContext:
        """Create a new browser context for a page.

        Returns:
            BrowserContext: A new Playwright browser context.

        Raises:
            RuntimeError: If the browser has not been launched.

        Logs:
            - Debug: Browser context created successfully

        Examples:
            >>> scraper = BrowserScraper()
            >>> await scraper.launch()
            >>> context = await scraper._create_context()
        """
        if not self.browser:
            raise RuntimeError(
                "Browser is not initialized. Call launch() first."
            )

        context: BrowserContext = await self.browser.new_context(
            user_agent=settings.user_agent,
            locale="en-US",
        )
        logger.debug("Browser context created successfully")
        return context

    async def _create_page(self) -> tuple[BrowserContext, Page]:
        """
        Create a new page within a fresh browser context.

        Returns:
            tuple[BrowserContext, Page]: The context and the new page.

        Logs:
            - Debug: New page created in browser context

        Examples:
            >>> scraper = BrowserScraper()
            >>> await scraper.launch()
            >>> context, page = await scraper._create_page()
        """
        context: BrowserContext = await self._create_context()
        page: Page = await context.new_page()
        logger.debug("New page created in browser context")
        return context, page

    async def fetch(self, url: str) -> ScrapeResult:
        """
        Fetch a URL using a headless browser and return a scrape result.

        Args:
            url (str): URL to navigate to and scrape.

        Returns:
            ScrapeResult: Standardized result containing content, status,
                          and latency.

        Notes:
            - Waits for full network idle state before capturing content.
            - Handles timeouts, errors, and page cleanup.
            - Uses `ResultBuilder.process` to determine SUCCESS, TIMEOUT,
              or FAILURE.

        Logs:
            - Info: Starting fetch
            - Debug: Page content fetched
            - Warning: Timeout while fetching
            - Exception: Unexpected error during fetch

        Examples:
            >>> scraper = BrowserScraper()
            >>> await scraper.launch()
            >>> result = await scraper.fetch("https://www.google.com")
            >>> await scraper.close_browser()
        """
        logger.info(f"Starting fetch: {url}")
        builder: ResultBuilder = ResultBuilder(ScrapeMethod.PLAYWRIGHT)
        context: Optional[BrowserContext] = None
        page: Optional[Page] = None

        try:
            context, page = await self._create_page()
            logger.debug(f"Navigating to URL: {url}")
            await page.goto(url, timeout=self.timeout)
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(self.timeout)

            content: Optional[str] = await page.content()
            logger.debug(
                f"Page content fetched: url={url} "
                f"length={len(content) if content else 0}"
            )

            return builder.process(url, content)

        except TimeoutError:
            logger.warning(f"Timeout while fetching: {url}")
            return builder.build_timeout(url)

        except Exception as e:
            logger.exception(f"Unexpected error during fetch: {url}")
            return builder.build_failure(url, str(e))

        finally:
            await self.close_page_and_context(page, context)

    async def close_page_and_context(
        self, page: Optional[Page], context: Optional[BrowserContext]
    ):
        """
        Close a page and its browser context to free resources.

        Args:
            page (Optional[Page]): The page to close.
            context (Optional[BrowserContext]): The context to close.

        Logs:
            - Debug: Page closed successfully
            - Debug: Browser context closed successfully

        Examples:
            >>> scraper = BrowserScraper()
            >>> await scraper.launch()
            >>> context, page = await scraper._create_page()
            >>> await scraper.close_page_and_context(page, context)
        """
        if page:
            await page.close()
            logger.debug("Page closed successfully")
        if context:
            await context.close()
            logger.debug("Browser context closed successfully")
