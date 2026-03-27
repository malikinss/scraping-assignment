# ./src/scrapers/http_scraper.py

import os
import time
import httpx

from src.models.scrape_result import ScrapeResult
from src.models.enums import ScrapeMethod, ScrapeStatus
from src.config.settings import settings
from src.config.proxy import ProxyConfig
from src.services.content_detector import ContentDetector

PROTOCOL = os.getenv("PROTOCOL") or "http://"


class HttpScraper:
    def __init__(self, proxy: ProxyConfig | None = None):
        self.proxy = proxy.to_httpx()[PROTOCOL] if proxy else None

        self.headers = {
            "User-Agent": settings.user_agent
        }

    def _create_client(self) -> httpx.Client:
        return httpx.Client(
            proxy=self.proxy,
            timeout=settings.timeout,
            headers=self.headers,
        )

    def fetch(self, url: str) -> ScrapeResult:
        for attempt in range(settings.retries):
            result = self._fetch_once(url)

            if result.is_success():
                return result

        return result

    def _fetch_once(self, url: str) -> ScrapeResult:
        start_time = time.time()

        try:
            with self._create_client() as client:
                response = client.get(url)

            return ScrapeResult(
                url=url,
                method=ScrapeMethod.HTTPX,
                status=ContentDetector().detect(response.text),
                latency=time.time() - start_time,
                content_length=len(response.text),
            )

        except httpx.TimeoutException:
            return ScrapeResult(
                url=url,
                method=ScrapeMethod.HTTPX,
                status=ScrapeStatus.TIMEOUT,
                latency=time.time() - start_time,
                content_length=0,
                error="timeout",
            )

        except Exception as e:
            return ScrapeResult.failure(
                url=url,
                method=ScrapeMethod.HTTPX,
                latency=time.time() - start_time,
                error=str(e),
            )
