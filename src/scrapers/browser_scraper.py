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
    URLUtils,
    settings,
    proxy_manager,
    ScrapeMethod,
    ScrapeResult,
)

from .result_builder import ResultBuilder

logger = Logger("BrowserScraper")


class BrowserScraper:
    """
    Asynchronous browser-based scraper using Playwright.

    Manages launching a headless Chromium browser, creating contexts
    and pages, navigating to URLs, and returning standardized
    `ScrapeResult` objects via `ResultBuilder`.

    Handles timeouts, errors, retries, and page/context cleanup.

    Attributes:
        timeout (int): Maximum timeout for browser operations in milliseconds.
        browser (Optional[Browser]): Playwright Browser instance.
        playwright (Optional[Playwright]): Playwright controller instance.
        proxy (Optional[dict]): Proxy configuration for browser context.
    """

    def __init__(self) -> None:
        """
        Initialize BrowserScraper with settings and optional proxy.

        Retrieves browser timeout and proxy configuration. Browser and
        Playwright instances are initialized as None.

        Examples:
            >>> scraper = BrowserScraper()
        """
        self.timeout: int = settings.browser_timeout
        self.browser: Optional[Browser] = None
        self.playwright: Optional[Playwright] = None
        self.proxy: Optional[dict] = proxy_manager.get_playwright_proxy()

    async def launch(self) -> None:
        """
        Launch Playwright and the headless Chromium browser.

        Must be called before fetching any pages. Initializes
        `self.playwright` and `self.browser`.

        Examples:
            >>> scraper = BrowserScraper()
            >>> await scraper.launch()
        """
        self.playwright: Playwright = await async_playwright().start()

        self.browser: Browser = await self.playwright.chromium.launch(
            headless=True,
            proxy=self.proxy,
        )

    async def close_browser(self) -> None:
        """
        Close the browser and stop the Playwright instance.

        Cleans up resources by closing the browser and stopping
        Playwright.

        Examples:
            >>> scraper = BrowserScraper()
            >>> await scraper.launch()
            >>> await scraper.close_browser()
        """
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None

    async def _create_context(self) -> BrowserContext:
        """
        Create a new browser context for page isolation.

        Returns:
            BrowserContext: A new Playwright browser context.

        Raises:
            RuntimeError: If the browser has not been launched.

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
        return context

    async def _create_page(self) -> tuple[BrowserContext, Page]:
        """
        Create a new page within a fresh browser context.

        Returns:
            tuple[BrowserContext, Page]: The context and the newly created
                                         page.

        Examples:
            >>> scraper = BrowserScraper()
            >>> await scraper.launch()
            >>> context, page = await scraper._create_page()
        """
        context: BrowserContext = await self._create_context()
        page: Page = await context.new_page()
        return context, page

    async def fetch(self, id: int, url: str) -> ScrapeResult:
        """
        Fetch a URL using a headless browser and return a scrape result.

        Uses `ResultBuilder` to standardize results. Waits for
        network idle state and handles timeouts, errors, and cleanup.

        Args:
            id (int): The scrape request ID.
            url (str): URL to navigate to and scrape.

        Returns:
            ScrapeResult: Standardized scrape result containing content,
                          status, latency, and error info.

        Examples:
            >>> scraper = BrowserScraper()
            >>> await scraper.launch()
            >>> result = await scraper.fetch(1, "https://example.com")
            >>> await scraper.close_browser()
        """
        builder: ResultBuilder = ResultBuilder(ScrapeMethod.PLAYWRIGHT)
        context: Optional[BrowserContext] = None
        page: Optional[Page] = None

        try:
            short_url = URLUtils.short_url(url)
            log = (
                f"url={short_url} "
                f"timeout={self.timeout}ms"
            )
            logger.debug(
                f"[ID: {id}] "
                f"[BROWSER] fetch started: {log}"
            )
            context, page = await self._create_page()
            await page.goto(url, timeout=self.timeout)
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(self.timeout)

            content: Optional[str] = await page.content()
            logger.debug(
                f"[ID: {id}] "
                f"[BROWSER] page content fetched: {log} "
                f"length={len(content) if content else 0}"
            )

            return builder.process(id, url, content)

        except TimeoutError:
            return builder.build_timeout(id, url)

        except Exception as e:
            return builder.build_failure(id, url, str(e))

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

        Examples:
            >>> scraper = BrowserScraper()
            >>> await scraper.launch()
            >>> context, page = await scraper._create_page()
            >>> await scraper.close_page_and_context(page, context)
        """
        if page:
            await page.close()
        if context:
            await context.close()
