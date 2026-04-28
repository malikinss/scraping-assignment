# ./src/pipeline/orchestrator/orchestrator.py
from .deps import (
    replace,
    URLs,
    ScrapeResult,
    ScrapeResults,
    ScrapeMethod,
    ScrapeStatus,
    HTTPScraper,
    BrowserScraper,
    settings,
    Optional,
    Queue,
    HTTPQueue,
    BrowserQueue,
    ResultQueue,
    HttpTask,
    BrowserTask,
    Handler,
    UnNormalResult, UnNormalResults, logger, QueueEmpty
)

from .worker import WorkerGroup


class PipelineOrchestrator:
    def __init__(self):
        self.http_scraper = HTTPScraper()
        self.browser_scraper = BrowserScraper()

        # queues
        self.http_queue: HTTPQueue = Queue()
        self.browser_queue: BrowserQueue = Queue(maxsize=500)
        self.result_queue: ResultQueue = Queue()

        # config
        self.http_workers_count: int = settings.httpx.max_concurrency
        self.browser_workers_count: int = settings.browser.max_concurrency

    # ===== PUBLIC =====

    async def process_pipeline(self, urls: URLs) -> ScrapeResults:
        if not urls:
            return ScrapeResults()

        logger.pipeline.start(len(urls), settings.httpx.max_concurrency)

        try:
            results: ScrapeResults = await self._run(urls)
            logger.pipeline.summary(results.count_by_status())
            return results
        except Exception as e:
            logger.pipeline.exception(e)
            return ScrapeResults()

    # ===== CORE =====

    async def _fill_http_queue(self, urls: URLs):
        for i, url in enumerate(urls, start=1):
            task: HttpTask = (i, url)
            await self.http_queue.put(task)

    async def _run(self, urls: URLs) -> ScrapeResults:
        await self._fill_http_queue(urls)

        async with self.http_scraper:
            async with WorkerGroup(
                self.http_workers_count,
                self._http_handler,
                self.http_queue,
                self._worker
            ):
                await self.http_queue.join()

        async with self.browser_scraper:
            async with WorkerGroup(
                self.browser_workers_count,
                self._browser_handler,
                self.browser_queue,
                self._worker
            ):
                await self.browser_queue.join()

        return await self._drain_results()

    # ===== GENERIC WORKER (DRY CORE) =====

    async def _worker(self, handler: Handler, queue: Queue):
        while True:
            task = await queue.get()
            if task is None:
                queue.task_done()
                break
            try:
                await handler(task)
            except Exception as e:
                logger.pipeline.exception(e)
            finally:
                queue.task_done()

    # ===== HANDLERS =====
    def _should_fallback(self, result):
        return result.is_failure

    async def _http_handler(self, task: HttpTask):
        id, url = task
        result = await self.http_scraper.fetch(id, url)
        if self._should_fallback(result):
            browser_task: BrowserTask = (id, url, result)
            await self.browser_queue.put(browser_task)
        else:
            await self.result_queue.put(result)

    async def _browser_handler(self, task: BrowserTask):
        id, url, http_result = task
        logger.pipeline.fallback(id, url, http_result.status)
        browser_result = await self.browser_scraper.fetch(id, url)

        br_error = browser_result.error
        http_error = http_result.error

        if br_error:
            merged = self._merge_errors(http_error, br_error)
            browser_result = replace(browser_result, error=merged)

        await self.result_queue.put(browser_result)
    # ===== RESULTS =====

    async def _drain_results(self) -> ScrapeResults:
        results: UnNormalResults = []
        while True:
            try:
                item: UnNormalResult = self.result_queue.get_nowait()
                results.append(self._normalize_result(item))
            except QueueEmpty:
                break
            except Exception:
                break
        return ScrapeResults(results)

    def _normalize_result(self, result: UnNormalResult) -> ScrapeResult:
        normalized: ScrapeResult = result
        if isinstance(result, Exception):
            logger.pipeline.exception(result)
            normalized = ScrapeResult(
                id=getattr(result, "id", 0),
                url=getattr(result, "url", "UNKNOWN_URL"),
                method=getattr(result, "method", ScrapeMethod.HTTPX),
                status=ScrapeStatus.FAILED,
                latency=0,
                content_length=0,
                error=str(result),
            )
        return normalized

    def _merge_errors(self, *errors: Optional[str]) -> str:
        return " | ".join(e for e in errors if e)
