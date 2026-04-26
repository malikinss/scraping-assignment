# ./src/services/results/factory/sr_factory.py

from .deps import (
    time,
    ScrapeResult,
    ScrapeStatus,
    ScraperContext,
    Callable,
    Optional,
    logger,
    detector,
)

Factory = Callable[[ScraperContext], ScrapeResult]


class ResultFactory:

    _status_map: dict[ScrapeStatus, str] = {
        ScrapeStatus.CAPTCHA: "captcha",
        ScrapeStatus.BLOCKED: "blocked",
        ScrapeStatus.EMPTY: "empty",
        ScrapeStatus.PDF: "pdf",
        ScrapeStatus.TIMEOUT: "timeout",
    }

    def __init__(self) -> None:
        self.start_timer()

    # ===== TIME =====

    def start_timer(self) -> None:
        self._start = time.perf_counter()

    def _latency(self) -> float:
        return max(time.perf_counter() - self._start, 0.0)

    # ===== BUILDERS =====

    def _build(
            self,
            ctx: ScraperContext,
            status: ScrapeStatus,
            content: Optional[str] = None,
            error: Optional[str] = None,
    ) -> ScrapeResult:
        latency: float = self._latency()
        content_length: int = self._content_len(content)
        logger.scraper.status(status, ctx, latency, content_length, error)
        return ScrapeResult(
            id=ctx.id,
            url=ctx.url,
            method=ctx.method,
            status=status,
            latency=latency,
            content=content,
            content_length=content_length,
            error=error,
        )

    # ===== HELPERS =====

    def _content_len(self, content: Optional[str]) -> int:
        return len(content) if content is not None else 0

    def _get_factory(self, status: ScrapeStatus) -> Optional[Factory]:
        method_name: str = self._status_map.get(status)
        if method_name:
            return getattr(self, method_name)
        return None

    # ===== PUBLIC =====
    def success(self, ctx: ScraperContext, text: str) -> ScrapeResult:
        return self._build(ctx, ScrapeStatus.SUCCESS, content=text)

    def failure(self, ctx: ScraperContext, error: str) -> ScrapeResult:
        return self._build(ctx, ScrapeStatus.FAILED, error=error)

    # ===== SHORTCUTS =====

    def empty(self, ctx: ScraperContext) -> ScrapeResult:
        return self._build(ctx, ScrapeStatus.EMPTY, error="Empty response")

    def blocked(self, ctx: ScraperContext) -> ScrapeResult:
        return self._build(ctx, ScrapeStatus.BLOCKED, error="Blocked by site")

    def captcha(self, ctx: ScraperContext) -> ScrapeResult:
        return self._build(ctx, ScrapeStatus.CAPTCHA, error="CAPTCHA found")

    def pdf(self, ctx: ScraperContext) -> ScrapeResult:
        return self._build(ctx, ScrapeStatus.PDF, error="PDF found")

    def timeout(self, ctx: ScraperContext) -> ScrapeResult:
        return self._build(ctx, ScrapeStatus.TIMEOUT, error="Timeout")

    # ===== MAIN ENTRY =====

    def process(self, ctx: ScraperContext, text: str) -> ScrapeResult:
        status: ScrapeStatus = detector.detect(text)

        if status == ScrapeStatus.SUCCESS:
            return self.success(ctx, text)

        factory: Optional[Factory] = self._get_factory(status)
        if factory:
            return factory(ctx)

        return self.failure(ctx, f"No factory for status {status}")
