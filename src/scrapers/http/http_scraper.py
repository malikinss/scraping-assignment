# ./src/scrapers/http/http_scraper.py

from .deps import (
    random,
    asyncio,
    settings,
    ScrapeResult,
    CTX,
    URL,
    Response,
    METHOD,
    logger,
    RFactory,
    TimeoutException,
    RequestError
)
from .http_client import HTTPXClient


class HTTPScraper:

    def __init__(self):
        self._http = HTTPXClient()

    async def __aenter__(self):
        await self._http.start()
        return self

    async def __aexit__(self, *args) -> bool:
        await self._http.close()
        return False

    # ===== CORE REQUEST =====
    async def _make_request(self, url: URL) -> Response:
        return await self._http.client.get(url)

    async def _request_attempt(self, base_ctx: CTX, attempt: int) -> Response:
        ctx: CTX = base_ctx.with_updates(attempt=attempt)
        logger.scraper.start_or_retry(ctx)

        try:
            return await self._make_request(ctx.url)
        except Exception as e:
            self._handle_exception(e, ctx)
            if attempt < base_ctx.retries:
                await self._backoff(attempt)
        return None

    async def _request_with_retry(self, base_ctx: CTX) -> Response:
        for attempt in range(1, base_ctx.retries + 1):
            response = await self._request_attempt(base_ctx, attempt)
            if response:
                if not self._should_retry(response):
                    return response
        logger.scraper.all_failed(base_ctx)
        return None

    def _should_retry(self, response: Response) -> bool:
        return response.status_code in {429, 500, 502, 503, 504}

    # ===== EXCEPTION HANDLING =====

    def _handle_exception(self, error: Exception, ctx: CTX) -> None:
        ctx_error = ctx.with_updates(error=str(error))
        if isinstance(error, TimeoutException):
            logger.scraper.timeout(ctx_error)
        elif isinstance(error, RequestError):
            logger.scraper.request_error(ctx_error, str(error))
        else:
            logger.scraper.exception(ctx_error, str(error))

    # ===== HELPERS =====

    async def _backoff(self, attempt: int) -> None:
        base = min(2 ** attempt, 10)
        delay = random.uniform(0, base)
        await asyncio.sleep(delay)

    def _is_pdf(self, response: Response) -> bool:
        content_type = response.headers.get("Content-Type", "").lower()
        return "application/pdf" in content_type

    # ===== PUBLIC API =====

    async def fetch(self, id: int, url: URL) -> ScrapeResult:
        factory: RFactory = RFactory()
        base_ctx: CTX = CTX(
            id=id,
            method=METHOD,
            url=url,
            timeout=settings.httpx.timeout,
            retries=settings.httpx.retries,
        )

        try:
            response = await self._request_with_retry(base_ctx)

            if response is None:
                return factory.failure(base_ctx, "No response")

            if self._is_pdf(response):
                return factory.pdf(base_ctx)

            return factory.process(base_ctx, response.text)

        except TimeoutException:
            return factory.timeout(base_ctx)

        except Exception as e:
            return factory.failure(base_ctx, str(e))
