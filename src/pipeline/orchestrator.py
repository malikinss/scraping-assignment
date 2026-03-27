# src/pipeline/orchestrator.py

import asyncio
from typing import List

from src.scrapers.http_scraper import HTTPScraper
from src.scrapers.browser_scraper import BrowserScraper
from src.models.scrape_result import ScrapeResult
from src.models.enums import ScrapeStatus
from src.config.settings import settings


class PipelineOrchestrator:
    def __init__(self):
        self.http_scraper = HTTPScraper()
        self.browser_scraper = BrowserScraper()

    async def launch(self):
        await self.browser_scraper.launch()

    def _should_fallback(self, result: ScrapeResult) -> bool:
        return result.status in {
            ScrapeStatus.ERROR,
            ScrapeStatus.TIMEOUT,
            ScrapeStatus.BLOCKED,
            ScrapeStatus.EMPTY,
        }

    async def process_url(self, url: str) -> ScrapeResult:
        # 1. Try with httpx
        result = await self.http_scraper.fetch(url)

        # 2. Check fallback
        if self._should_fallback(result):

            # Don't bypass CAPTCHA
            if result.status == ScrapeStatus.CAPTCHA:
                return result

            # 3. Try with Playwright
            browser_result = await self.browser_scraper.fetch(url)

            return browser_result

        return result

    async def run(self, urls: List[str]) -> List[ScrapeResult]:
        semaphore = asyncio.Semaphore(settings.max_concurrency)

        async def worker(url: str):
            async with semaphore:
                return await self.process_url(url)

        tasks = [worker(url) for url in urls]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # normalize exceptions
        final_results = []
        for r in results:
            if isinstance(r, Exception):
                final_results.append(
                    ScrapeResult(
                        url=r.url,
                        method=r.method,
                        status=ScrapeStatus.ERROR,
                        latency=0,
                        content_length=0,
                        error=str(r),
                    )
                )
            else:
                final_results.append(r)

        return final_results
