# ./src/scrapers/browser/browser_client.py

from .deps import async_playwright, Playwright, Browser, Optional, settings


class BrowserClient:
    def __init__(self) -> None:
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.initialized: bool = False

    async def start(self) -> None:
        if self.initialized:
            return
        self.playwright: Playwright = await async_playwright().start()
        self.browser: Browser = await self.playwright.chromium.launch(
            headless=settings.browser.headless,
            proxy=settings.browser.proxy,
        )
        self.initialized = True

    async def close(self) -> None:
        if self.initialized:
            await self.browser.close()
            await self.playwright.stop()
            self.browser = None
            self.playwright = None
            self.initialized = False

    async def ensure(self) -> None:
        if not self.initialized:
            await self.start()
