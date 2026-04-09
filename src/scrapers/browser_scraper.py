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
    URL
)

from .result_builder import ResultBuilder

logger = Logger("BrowserScraper")


class BrowserScraper:
    """
    Asynchronous browser scraper using Playwright.

    Handles dynamic web pages that require JavaScript execution. Manages
    browser lifecycle, page creation, content retrieval, and cleanup.

    Attributes:
        timeout (int): Max wait time (ms) for page loading and network idle.
        browser (Optional[Browser]): Active Playwright browser instance.
        playwright (Optional[Playwright]): Playwright engine instance.
        proxy (Optional[dict]): Proxy settings for browser requests.
    """

    def __init__(self) -> None:
        """
        Initialize the BrowserScraper.

        Sets the timeout, initializes browser and Playwright to None,
        and loads proxy settings from configuration.
        """
        self.timeout: int = settings.browser_timeout
        self.browser: Optional[Browser] = None
        self.playwright: Optional[Playwright] = None
        self.proxy: Optional[dict] = proxy_manager.get_playwright_proxy()

    # ===== LIFECYCLE =====

    async def launch(self) -> None:
        """
        Launch the Playwright engine and Chromium browser.

        If the browser is already launched, does nothing. Uses headless
        mode and applies proxy settings if configured.

        Returns:
            None
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
        Close the browser and stop Playwright.

        Safely handles cases when browser or Playwright are already None.
        Ensures proper cleanup to avoid memory leaks.

        Returns:
            None
        """
        if self.browser:
            await self.browser.close()
            self.browser = None

        if self.playwright:
            await self.playwright.stop()
            self.playwright = None

    # ===== INTERNAL HELPERS =====

    async def _create_context(self) -> BrowserContext:
        """
        Create a new browser context.

        Each context is isolated (cookies, cache, storage) from others.

        Raises:
            RuntimeError: If the browser has not been launched.

        Returns:
            BrowserContext: A new browser context instance.
        """
        if not self.browser:
            raise RuntimeError("Browser not initialized. Call launch()")

        context: BrowserContext = await self.browser.new_context(
            user_agent=settings.user_agent,
            locale="en-US",
        )
        return context

    async def _create_page(self) -> tuple[BrowserContext, Page]:
        """
        Create a new page within a fresh browser context.

        Returns:
            tuple[BrowserContext, Page]: The context and the new page.
        """
        context: BrowserContext = await self._create_context()
        page: Page = await context.new_page()
        return context, page

    async def _cleanup(
        self, page: Optional[Page], context: Optional[BrowserContext]
    ) -> None:
        """
        Close page and context to release resources.

        Args:
            page (Optional[Page]): Page to close.
            context (Optional[BrowserContext]): Context to close.

        Returns:
            None
        """
        if page:
            await page.close()
        if context:
            await context.close()

    # ===== CORE =====

    async def fetch(self, id: int, url: URL) -> ScrapeResult:
        """
        Fetch a page and return a structured ScrapeResult.

        1. Creates a page.
        2. Loads the URL.
        3. Waits for network idle and optional timeout.
        4. Extracts content.
        5. Builds ScrapeResult with ResultBuilder.

        Args:
            id (int): Unique request identifier.
            url (URL): URL to scrape.

        Returns:
            ScrapeResult: Result object including status, latency,
                          content, or error.
        """
        builder: ResultBuilder = ResultBuilder(ScrapeMethod.PLAYWRIGHT)
        context: Optional[BrowserContext] = None
        page: Optional[Page] = None

        self._log(id, url, "START")

        try:
            context, page = await self._create_page()
            content: Optional[str] = await self.get_content(id, url, page)
            return builder.process(id, url, content)

        except TimeoutError:
            return builder.build_timeout(id, url)

        except Exception as e:
            return builder.build_failure(id, url, str(e))

        finally:
            await self._cleanup(page, context)

    async def get_content(
        self,
        id: int,
        url: URL,
        page: Page
    ) -> Optional[str]:
        """
        Navigate to URL and extract page content.

        Waits for network idle and an additional small delay to ensure
        page stability.

        Args:
            id (int): Unique request ID.
            url (URL): URL to fetch.
            page (Page): Playwright page instance.

        Returns:
            Optional[str]: HTML content of the page, or None if failed.
        """
        try:
            await page.goto(url, timeout=self.timeout)
            await page.wait_for_load_state("networkidle")

            wait_time: int = max(500, min(self.timeout, 2000))
            await page.wait_for_timeout(wait_time)

            content: Optional[str] = await page.content()
            length: int = len(content) if content else 0
            self._log(id, url, f"CONTENT LOADED length={length}")
            return content

        except TimeoutError:
            self._log(id, url, "TIMEOUT", "error")
            return None
        except Exception as e:
            self._log(id, url, f"ERROR: {e}", "error")
            return None

    # ===== LOGGING =====

    def _log(
        self,
        id: int,
        url: URL,
        message: str,
        level: str = "debug",
    ) -> None:
        """
        Central logging helper for browser scraping.

        Formats log messages consistently with ID, type, URL, and timeout.

        Args:
            id (int): Unique request ID.
            url (URL): Target URL.
            message (str): Message to log.
            level (str, optional): Logging level.

        Returns:
            None
        """
        short_url = URLUtils.short_url(url)
        msg = (
            f"[ID:{id}][BROWSER] {message} "
            f"url={short_url} timeout={self.timeout}ms"
        )
        getattr(logger, level)(msg)
