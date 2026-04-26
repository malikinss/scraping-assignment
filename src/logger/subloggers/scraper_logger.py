# ./src/logger/subloggers/scraper_logger.py
from .lp import LLine
from .core import Logger
from .deps import Callable, Optional, ScraperContext, ScrapeStatus


class ScraperLogger:
    def __init__(self, logger: Logger) -> None:
        self.log: Logger = logger
        self._dispatch = {
            "debug": self.log.debug,
            "info": self.log.info,
            "warning": self.log.warning,
            "error": self.log.error,
            "critical": self.log.critical
        }

    def _log_fn(self, level: str) -> Callable[[str], None]:
        return self._dispatch.get(level, self.log.debug)

    def event(
        self,
        ctx: ScraperContext,
        message: str,
        level: str = "debug"
    ) -> None:
        msg = LLine().prefix(ctx.id, ctx.method, ctx.url, ctx.timeout)
        msg.text(message).attempt(ctx.attempt, ctx.retries)
        self._log_fn(level)(msg.build())

    def status(
        self,
        status: ScrapeStatus,
        ctx: ScraperContext,
        latency: float,
        content_length: int,
        error: Optional[str] = None
    ) -> None:
        msg = LLine().prefix(ctx.id, ctx.method, ctx.url, ctx.timeout)
        msg.status(status.value).seconds("latency", latency)
        msg.kv("content_length", content_length).error(error)
        if status == ScrapeStatus.SUCCESS:
            self.log.info(msg.build())
        elif status in (ScrapeStatus.TIMEOUT, ScrapeStatus.CAPTCHA):
            self.log.warning(msg.build())
        elif status == ScrapeStatus.FAILED:
            self.log.error(msg.build())
        else:
            self.log.debug(msg.build())

    def log_fallback(self, ctx: ScraperContext, status: str) -> None:
        msg = LLine().prefix(ctx.id, ctx.method, ctx.url, ctx.timeout)
        msg.kv("name", "fallback browser").kv("status", status)
        self.log.info(msg.build())

    def start(self, ctx: ScraperContext) -> None:
        self.event(ctx, "START", "debug")

    def retry(self, ctx: ScraperContext) -> None:
        self.event(ctx, "RETRYING", "warning")

    def start_or_retry(self, ctx: ScraperContext) -> None:
        if ctx.attempt == 1:
            self.start(ctx)
        else:
            self.retry(ctx)

    def success(self, ctx: ScraperContext) -> None:
        self.event(ctx, "SUCCESS", "info")

    def fail(self, ctx: ScraperContext, status: str) -> None:
        self.event(ctx, f"STATUS CODE {status}", "error")

    def all_failed(self, ctx: ScraperContext) -> None:
        self.event(ctx, "ALL RETRIES FAILED", "error")

    def timeout(self, ctx: ScraperContext) -> None:
        self.event(ctx, "TIMEOUT", "error")

    def request_error(self, ctx: ScraperContext, error: str) -> None:
        level = "error" if ctx.attempt == ctx.retries else "debug"
        self.event(ctx, f"REQUEST ERROR: {error}", level)

    def exception(self, ctx: ScraperContext, error: str) -> None:
        self.event(ctx, f"UNEXPECTED ERROR: {error}", "error")
