# ./src/scrapers/http_scraper.py

import time
import httpx
from typing import Optional

from src.config.settings import settings
from src.config.proxy import proxy_manager
from src.models.scrape_result import ScrapeResult
from src.models.enums import ScrapeMethod, ScrapeStatus
from src.services.content_detector import detector


class HTTPScraper:
    def __init__(self):
        self.timeout = settings.timeout
        self.retries = settings.retries
        self.proxy = proxy_manager.get_httpx_proxy()[settings.protocol]

        self.client = self._build_client()

    def _build_client(self) -> httpx.AsyncClient:
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
        for attempt in range(self.retries + 1):
            try:
                response = await self.client.get(url)

                if response.status_code == 200:
                    return response

            except httpx.TimeoutException:
                if attempt == self.retries:
                    raise

            except httpx.RequestError:
                if attempt == self.retries:
                    raise

        return None

    async def fetch(self, url: str) -> ScrapeResult:
        start = time.perf_counter()

        try:
            response = await self._request_with_retry(url)

            latency = time.perf_counter() - start

            if response is None:
                return ScrapeResult.failure(
                    url, ScrapeMethod.HTTPX, latency, "No response"
                )

            status = detector.detect(response.text)

            if status == ScrapeStatus.CAPTCHA:
                return ScrapeResult.captcha(url, ScrapeMethod.HTTPX, latency)

            if status == ScrapeStatus.BLOCKED:
                return ScrapeResult(
                    url=url,
                    method=ScrapeMethod.HTTPX,
                    status=ScrapeStatus.BLOCKED,
                    latency=latency,
                    content_length=0,
                    error="Blocked by site",
                )

            if not response.text.strip():
                return ScrapeResult(
                    url=url,
                    method=ScrapeMethod.HTTPX,
                    status=ScrapeStatus.EMPTY,
                    latency=latency,
                    content_length=0,
                )

            return ScrapeResult.success(
                url, ScrapeMethod.HTTPX, latency, response.text
            )

        except httpx.TimeoutException:
            latency = time.perf_counter() - start
            return ScrapeResult(
                url=url,
                method=ScrapeMethod.HTTPX,
                status=ScrapeStatus.TIMEOUT,
                latency=latency,
                content_length=0,
                error="Timeout",
            )

        except Exception as e:
            latency = time.perf_counter() - start
            return ScrapeResult(
                url=url,
                method=ScrapeMethod.HTTPX,
                status=ScrapeStatus.ERROR,
                latency=latency,
                content_length=0,
                error=str(e),
            )
