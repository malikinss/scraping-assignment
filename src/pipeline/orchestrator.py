# src/pipeline/orchestrator.py


from .deps import (
    asyncio,
    List,
    URLUtils,
    ScrapeResult,
    ScrapeStatus,
    HTTPScraper,
    BrowserScraper,
    settings,
    Logger,
    MetricsAggregator
)

logger = Logger("PipelineOrchestrator")


class PipelineOrchestrator:
    """
    Orchestrates the execution of scraping pipelines using HTTP and browser
    scrapers.

    This class manages concurrent scraping of URLs, fallback logic from HTTPX
    to browser-based scraping, and aggregation of results.

    It uses `HTTPScraper` for fast requests and `BrowserScraper` for pages
    requiring JS rendering or additional handling.

    Attributes:
        http_scraper (HTTPScraper): Instance for HTTPX-based scraping.
        browser_scraper (BrowserScraper): Instance for Playwright-based
                                          scraping.
    """

    def __init__(self):
        """
        Initializes the PipelineOrchestrator with HTTP and browser scrapers.
        """
        self.http_scraper = HTTPScraper()
        self.browser_scraper = BrowserScraper()

    async def launch(self):
        """
        Launch necessary resources for the browser scraper.

        This must be called before fetching any URLs that may require browser
        rendering.
        """
        await self.browser_scraper.launch()

    async def close(self):
        """
        Closes the browser and cleans up resources.

        This should be called after all scraping tasks are completed to free
        memory and resources.
        """
        await self.browser_scraper.close_browser()

    async def process_pipeline(self, urls: List[str]):
        """
        Process a list of URLs through the scraping pipeline.

        Executes scraping with concurrency limits, applies fallback logic,
        and aggregates statistics.

        Args:
            urls (List[str]): List of URLs to scrape.

        Returns:
            List[ScrapeResult]: List of standardized scrape results.
        """
        total_urls = len(urls)
        await self.launch()

        logger.separator()
        logger.info(
            f"Pipeline started: total={total_urls} "
            f"concurrency={settings.max_concurrency}"
        )

        try:
            results = await self.run(urls)
            stats = MetricsAggregator.group_by_status(results)

            logger.info(
                "Pipeline completed: "
                f"total={total_urls} "
                f"success={stats.get(ScrapeStatus.SUCCESS, 0)} "
                f"failed={stats.get(ScrapeStatus.FAILED, 0)} "
                f"timeout={stats.get(ScrapeStatus.TIMEOUT, 0)} "
                f"blocked={stats.get(ScrapeStatus.BLOCKED, 0)} "
                f"empty={stats.get(ScrapeStatus.EMPTY, 0)} "
                f"captcha={stats.get(ScrapeStatus.CAPTCHA, 0)}"
            )
            return results
        finally:
            await self.close()

    def _should_use_browser(self, result: ScrapeResult) -> bool:
        """
        Determine whether a failed HTTPX result should fallback to browser
        scraping.

        Args:
            result (ScrapeResult): Result from an HTTPX scrape.

        Returns:
            bool: `True` if the status indicates a fallback is needed,
                  else `False`.
        """
        return result.status in {
            ScrapeStatus.FAILED,
            ScrapeStatus.TIMEOUT,
            ScrapeStatus.BLOCKED,
            ScrapeStatus.EMPTY,
        }

    async def process_url(self, id: int, url: str) -> ScrapeResult:
        """
        Process a single URL through the scraping pipeline.

        Attempts HTTPX scraping first, then falls back to browser scraping if
        the initial attempt fails or returns an empty result.

        Args:
            id (int): Unique identifier for the request.
            url (str): URL to scrape.

        Returns:
            ScrapeResult: Result of the scraping operation.
        """
        short_url = URLUtils.short_url(url)

        # 1. HTTPX attempt
        result = await self.http_scraper.fetch(id, url)

        # 2. fallback decision
        if self._should_use_browser(result):
            logger.info(
                f"[ID: {id}][FALLBACK_BROWSER] "
                f"url={short_url} "
                f"reason={result.status}"
            )

            result = await self.browser_scraper.fetch(id, url)
        return result

    async def run(self, urls: List[str]) -> List[ScrapeResult]:
        """
        Run the scraping tasks concurrently with a semaphore for throttling.

        Args:
            urls (List[str]): List of URLs to scrape.

        Returns:
            List[ScrapeResult]: List of results, with exceptions normalized
                                as failed results.
        """
        concurrency = min(settings.max_concurrency, len(urls))
        semaphore = asyncio.Semaphore(concurrency)

        async def worker(id: int, url: str) -> ScrapeResult:
            async with semaphore:
                return await self.process_url(id, url)

        tasks: List[asyncio.Task[ScrapeResult]] = [
            worker(id, url)
            for id, url in enumerate(urls, start=1)
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        return await self._normalize_exceptions(results)

    async def _normalize_exceptions(
        self, results: List[ScrapeResult]
    ) -> List[ScrapeResult]:
        """
        Convert exceptions raised during scraping into standardized failed
        results.

        Args:
            results (List[ScrapeResult]): List containing either ScrapeResult
                                          or Exception objects.

        Returns:
            List[ScrapeResult]: List with all exceptions replaced
                                by ScrapeResult objects with status FAILED.
        """

        final_results = []

        for r in results:
            if isinstance(r, Exception):
                logger.exception(f"Unhandled exception in result: {r}")
                final_results.append(
                    ScrapeResult(
                        id=getattr(r, "id", 0),
                        url=getattr(r, "url", "unknown"),
                        method=getattr(r, "method", None),
                        status=ScrapeStatus.FAILED,
                        latency=0,
                        content_length=0,
                        error=str(r),
                    )
                )
            else:
                final_results.append(r)
        return final_results
