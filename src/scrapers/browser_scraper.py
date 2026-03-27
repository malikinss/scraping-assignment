# ./src/scrapers/browser_scraper.py

import time
from playwright.async_api import async_playwright, Browser, Page

from src.config.settings import settings
from src.config.proxy import proxy_manager
from src.models.scrape_result import ScrapeResult
from src.models.enums import ScrapeMethod, ScrapeStatus
from src.services.content_detector import detector


class BrowserScraper:
    def __init__(self):
        self.browser: Browser | None = None
        self.proxy = proxy_manager.get_playwright_proxy()

    async def launch(self):
        playwright = await async_playwright().start()

        self.browser = await playwright.chromium.launch(
            headless=True,
            proxy=self.proxy,
        )

    async def _create_page(self) -> Page:
        context = await self.browser.new_context(
            user_agent=settings.user_agent,
            locale="en-US",
        )
        page = await context.new_page()
        return page

    async def _wait_for_page_load(self, page: Page):
        await page.wait_for_load_state("domcontentloaded")

    async def _get_content(self, page: Page) -> str:
        return await page.content()

    async def fetch(self, url: str) -> ScrapeResult:
        start = time.perf_counter()

        try:
            page = await self._create_page()

            await page.goto(url, timeout=settings.timeout)

            await self._wait_for_page_load(page)

            content = await self._get_content(page)

            latency = time.perf_counter() - start
            status = detector.detect(content)

            if status == ScrapeStatus.CAPTCHA:
                return ScrapeResult.captcha(
                    url, ScrapeMethod.PLAYWRIGHT, latency
                )

            if status == ScrapeStatus.BLOCKED:
                return ScrapeResult(
                    url=url,
                    method=ScrapeMethod.PLAYWRIGHT,
                    status=ScrapeStatus.BLOCKED,
                    latency=latency,
                    content_length=0,
                    error="Blocked",
                )

            if not content.strip():
                return ScrapeResult(
                    url=url,
                    method=ScrapeMethod.PLAYWRIGHT,
                    status=ScrapeStatus.EMPTY,
                    latency=latency,
                    content_length=0,
                )

            return ScrapeResult.success(
                url, ScrapeMethod.PLAYWRIGHT, latency, content
            )

        except Exception as e:
            latency = time.perf_counter() - start
            return ScrapeResult(
                url=url,
                method=ScrapeMethod.PLAYWRIGHT,
                status=ScrapeStatus.ERROR,
                latency=latency,
                content_length=0,
                error=str(e),
            )

        finally:
            await page.close()
