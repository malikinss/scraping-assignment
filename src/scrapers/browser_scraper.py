# ./src/scrapers/browser_scraper.py

import time
from playwright.sync_api import sync_playwright
from src.models.scrape_result import ScrapeResult
from src.models.enums import ScrapeMethod
from src.config.proxy import ProxyConfig
from src.services.content_detector import ContentDetector


class BrowserScraper:
    def __init__(
        self,
        proxy: ProxyConfig = None,
        headless: bool = True,
        timeout: int = 30000
    ):
        self.proxy = proxy.to_playwright() if proxy else None
        self.headless = headless
        self.timeout = timeout

        self.playwright = None
        self.browser = None

    def _create_browser(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            proxy=self.proxy,
            headless=self.headless
        )

    def fetch(self, url: str) -> ScrapeResult:
        start = time.time()

        try:
            if not self.browser:
                self._create_browser()

            context = self.browser.new_context()
            page = context.new_page()

            page.goto(url, timeout=self.timeout)

            content = self._get_content(page)

            return ScrapeResult(
                url=url,
                method=ScrapeMethod.PLAYWRIGHT,
                status=ContentDetector().detect(content),
                latency=time.time() - start,
                content_length=len(content),
            )

        except Exception as e:
            return ScrapeResult.failure(
                url=url,
                method=ScrapeMethod.PLAYWRIGHT,
                latency=time.time() - start,
                error=str(e),
            )

        finally:
            self.close()

    def _get_content(self, page):
        page.wait_for_load_state("networkidle")
        return page.content()

    def close(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
