# ./src/logger/scraper_logger.py

"""
Scraper Logger Module
=====================

This module provides a structured scraper logger that wraps the core Logger
class to handle scraper-level logging operations.

Key Features:
    - Structured logging for scraper lifecycle events
    - Helper methods for starting, retrying, succeeding, failing, and timeout
      events
    - Uses LogParts for consistent log formatting

Classes:
    ScraperLogger: Logger wrapper for scraper-level events

Dependencies:
    - src.logger.core.Logger
    - src.logger.deps.Optional
    - src.logger.deps.ScraperContext
    - src.logger.deps.URLUtils
    - src.logger.log_parts.LogParts

Usage:
    >>> from src.logger import Logger, ScraperLogger
    >>> logger = Logger()
    >>> scraper_logger = ScraperLogger(logger)
    >>> scraper_logger.start(context)
    >>> scraper_logger.retry(context)
    >>> scraper_logger.success(context)
    >>> scraper_logger.fail(context, "HTTP 404")
    >>> scraper_logger.timeout(context)
    >>> scraper_logger.request_error(context, "Connection timed out")
    >>> scraper_logger.no_proxy("GET")
    >>> scraper_logger.exception(context, "An unexpected error occurred")

Example:
    >>> logger = Logger()
    >>> scraper_logger = ScraperLogger(logger)
    >>> scraper_logger.start(
    ...     ScraperContext(
    ...         id=1, method="GET", url="http://example.com", timeout=10
    ...     )
    ... )
    DEBUG: [1 GET example.com] START [ATempt 1/3]
    >>> scraper_logger.success(
    ...     ScraperContext(
    ...         id=1, method="GET", url="http://example.com", timeout=10
    ...     )
    ... )
    INFO: [1 GET example.com] SUCCESS [ATempt 1/3]

"""

from .core import Logger
from .deps import Optional, ScraperContext, URLUtils
from .log_parts import LogParts as LP


class ScraperLogger:
    """
    A logger class for scraper events and status.

    This class provides methods for logging different events that occur during
    scraper execution, such as starting, retrying, succeeding, failing, and
    timeout.
    It also provides methods for logging status of the scraper.

    Attributes:
        log (Logger): The logger instance.
    """

    def __init__(self, logger: Logger) -> None:
        """
        Initialize ScraperLogger.

        Args:
            logger (Logger): The logger instance.
        """
        self.log: Logger = logger

    def event(
        self,
        ctx: ScraperContext,
        message: str,
        level: str = "debug"
    ) -> None:
        """
        Log an event with context.

        Args:
            ctx (ScraperContext): The scraper context.
            message (str): The message to log.
            level (str): The log level (default: "debug").
        """
        short_url: str = URLUtils.short_url(ctx.url)
        prefix: str = LP.prefix(ctx.id, ctx.method, short_url, ctx.timeout)
        attempt_str: str = LP.attempt(ctx.attempt, ctx.retries)

        getattr(self.log, level)(f"{prefix} {message} {attempt_str}")

    def status(
        self,
        status: str,
        ctx: ScraperContext,
        latency: float,
        content_length: int,
        error: Optional[str] = None
    ) -> None:
        """
        Log the status of the scraper.

        Args:
            status (str): The status of the scraper.
            ctx (ScraperContext): The scraper context.
            latency (float): The time taken to scrape.
            content_length (int): The length of the content.
            error (Optional[str]): The error message if any.
        """
        rows = [
            LP.id(ctx.id),
            LP.method(ctx.method),
            LP.status(status),
            LP.url(ctx.url),
            LP.latency(latency),
            LP.content_length(content_length),
            LP.error(error)
        ]

        msg = " ".join(rows)

        if status.value == "success":
            self.log.rows(rows)
        elif status.value in ("timeout", "captcha"):
            self.log.warning(msg)
        elif status.value == "failed":
            self.log.error(msg)
        else:
            self.log.debug(msg)

    def log_fallback(self, ctx: ScraperContext, status: str) -> None:
        """
        Log a fallback event.

        Args:
            ctx (ScraperContext): The scraper context.
            status (str): The status of the fallback.
        """
        rows = [
            LP.id(ctx.id),
            LP.name("fallback browser"),
            LP.url(ctx.url),
            LP.reason(status)
        ]
        self.log.rows(rows)

    def start(self, ctx: ScraperContext) -> None:
        """
        Log the start of the scraper.

        Args:
            ctx (ScraperContext): The scraper context.
        """
        self.event(ctx, "START", "debug")

    def retry(self, ctx: ScraperContext) -> None:
        """
        Log a retry event.

        Args:
            ctx (ScraperContext): The scraper context.
        """
        self.event(ctx, "RETRYING", "warning")

    def success(self, ctx: ScraperContext) -> None:
        """
        Log a success event.

        Args:
            ctx (ScraperContext): The scraper context.
        """
        self.event(ctx, "SUCCESS", "info")

    def fail(self, ctx: ScraperContext, status: str) -> None:
        """
        Log a failure event.

        Args:
            ctx (ScraperContext): The scraper context.
            status (str): The status of the failure.
        """
        self.event(ctx, f"STATUS CODE {status}", "error")

    def all_failed(self, ctx: ScraperContext) -> None:
        """
        Log that all retries have failed.

        Args:
            ctx (ScraperContext): The scraper context.
        """
        self.event(ctx, "ALL RETRIES FAILED", "error")

    def timeout(self, ctx: ScraperContext) -> None:
        """
        Log a timeout event.

        Args:
            ctx (ScraperContext): The scraper context.
        """
        self.event(ctx, "TIMEOUT", "error")

    def request_error(self, ctx: ScraperContext, error: str) -> None:
        """
        Log a request error event.

        Args:
            ctx (ScraperContext): The scraper context.
            error (str): The error message.
        """
        level = "error" if ctx.attempt == ctx.retries else "debug"
        self.event(ctx, f"REQUEST ERROR: {error}", level)

    def no_proxy(self, method: str) -> None:
        """
        Log that no proxy was configured.

        Args:
            method (str): The method used.
        """
        msg = LP.prefix(-1, method, "N/A", 0) + " NO PROXY CONFIGURED"
        self.log.warning(msg)

    def exception(self, ctx: ScraperContext, error: str) -> None:
        """
        Log an unexpected error event.

        Args:
            ctx (ScraperContext): The scraper context.
            error (str): The error message.
        """
        self.event(ctx, f"UNEXPECTED ERROR: {error}", "error")
