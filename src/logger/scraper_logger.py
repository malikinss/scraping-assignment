# ./src/logger/scraper_logger.py

"""
Scraper Logger Module
=====================

This module provides a structured scraper logger that wraps the core Logger
class to handle scraper-level logging operations.

Key Features:
    - Structured logging for scraper lifecycle events
    - Helper methods for request attempts, status reporting, and fallbacks
    - Uses LogParts for consistent log formatting

Classes:
    ScraperLogger: Logger wrapper for scraper-level events

Dependencies:
    - src.logger.core.Logger
    - src.logger.deps.Optional
    - src.logger.log_parts.LogParts

Usage:
    >>> from src.logger import Logger, ScraperLogger
    >>> logger = Logger()
    >>> scraper_logger = ScraperLogger(logger)
    >>> scraper_logger.scraper_log(
            1, "HTTPX", "http://example.com", 10, "Requesting..."
        )
    >>> scraper_logger.status(
            "HTTPX", "success", 1, "http://example.com", 0.5, 1024
        )
    >>> scraper_logger.log_fallback(1, "http://example.com", "timeout")

Example:
    >>> logger = Logger()
    >>> scraper_logger = ScraperLogger(logger)
    >>> scraper_logger.scraper_log(
            1, "HTTPX", "http://example.com", 10, "Requesting..."
        )
    Requesting... [id=1 method=HTTPX url=http://example.com timeout=10.0]
    >>> scraper_logger.status(
            "HTTPX", "success", 1, "http://example.com", 0.5, 1024
        )
    [
        id=1 method=HTTPX status=success url=http://example.com latency=0.50s
        content_length=1024
    ]

"""

from .core import Logger
from .deps import Optional
from .log_parts import LogParts as LP


class ScraperLogger:
    """
    Logger wrapper for scraper-level events.

    This class provides structured logging utilities for individual scraping
    operations, including request attempts, status reporting, and fallback
    handling. It standardizes log formatting using `LogParts` helpers and
    delegates actual logging to the underlying `Logger`.

    Attributes:
        log (Logger): Core logger instance used for emitting logs.
    """

    def __init__(self, logger: Logger):
        """
        Initialize the ScraperLogger.

        Args:
            logger (Logger): Core logger instance used for emitting logs.
        """
        self.log: Logger = logger

    def scraper_log(
        self,
        id: int,
        method: str,
        url,
        timeout: float,
        message: str,
        level: str = "debug",
        attempt: Optional[int] = None,
        retries: Optional[int] = None
    ):
        """
        Log a generic scraper event with optional retry metadata.

        This method is typically used for low-level request lifecycle logging
        such as attempts, retries, and intermediate states.

        Args:
            id (int): Unique identifier of the scraping task.
            method (str): Scraping method (e.g., HTTPX, PLAYWRIGHT).
            url: Target URL.
            timeout (float): Timeout value associated with the request.
            message (str): Custom log message.
            level (str, optional): Log level to use (e.g., "debug",
                "info", "warning"). Defaults to "debug".
            attempt (Optional[int], optional): Current retry attempt number.
            retries (Optional[int], optional): Total number of retries.
        """
        prefix = LP.prefix(id, method, url, timeout)
        attempt_str = LP.attempt(attempt, retries)

        getattr(self.log, level)(f"{prefix}{message}{attempt_str}")

    def status(
        self,
        method: str,
        status: str,
        id: int,
        url,
        latency: float,
        content_length: int,
        error: Optional[str] = None
    ) -> None:
        """
        Log the final status of a scraping operation.

        The log level is determined dynamically based on the provided status:
            - success → info (structured rows)
            - timeout/captcha → warning
            - failed → error
            - other → debug

        Args:
            method (str): Scraping method used.
            status: Scraping status (expected to have a `.value` attribute).
            id (int): Unique identifier of the scraping task.
            url: Target URL.
            latency (float): Request latency in seconds.
            content_length (int): Length of the response content.
            error (Optional[str], optional): Error message if any.
        """
        rows = [
            LP.id(id),
            LP.method(method),
            LP.status(status),
            LP.url(url),
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

    def log_fallback(self, id: int, url, status):
        """
        Log a fallback browser event.

        This method is typically used when a fallback scraping method
        (e.g., Playwright) is used instead of the primary method.

        Args:
            id (int): Unique identifier of the scraping task.
            url: Target URL.
            status: Status indicating why fallback was used.
        """
        rows = [
            LP.id(id),
            LP.name("fallback browser"),
            LP.url(url),
            LP.reason(status)
        ]
        self.log.rows(rows)
