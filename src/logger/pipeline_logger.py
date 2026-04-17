# ./src/logger/pipeline_logger.py

"""
Pipeline Logger Module
=====================

This module provides a structured pipeline logger that wraps the core Logger
class to handle pipeline-level logging operations.

Key Features:
    - Structured logging for pipeline lifecycle events
    - Helper methods for startup, summary, fallback, and configuration logging
    - Uses LogParts for consistent log formatting

Classes:
    PipelineLogger: Logger wrapper for pipeline-level events

Dependencies:
    - src.logger.core.Logger
    - src.logger.deps.Counts
    - src.logger.log_parts.LogParts

Usage:
    >>> from src.logger import Logger, PipelineLogger
    >>> logger = Logger()
    >>> pipeline_logger = PipelineLogger(logger)
    >>> pipeline_logger.start(100, 5)
    >>> pipeline_logger.summary(counts)
    >>> pipeline_logger.fallback(1, "http://example.com", "timeout")
    >>> pipeline_logger.settings(60, 30, 3, 5)
    >>> pipeline_logger.proxy_success("proxy.example.com")

Example:
    >>> logger = Logger()
    >>> pipeline_logger = PipelineLogger(logger)
    >>> pipeline_logger.start(100, 5)
    Pipeline started:
    Total: 100
    Concurrency: 5
    >>> pipeline_logger.summary(Counts(success=80, failed=10, timeout=10))
    Pipeline completed:
    Success: 80
    Failed: 10
    Timeout: 10

"""

from .core import Logger
from .deps import Counts
from .log_parts import LogParts as LP


class PipelineLogger:
    """
    Logger wrapper for pipeline-level events and lifecycle tracking.

    This class provides structured logging methods for key stages of the
    scraping pipeline, including startup, completion summaries, fallback
    handling, configuration reporting, and error scenarios.

    It ensures consistent formatting across all pipeline-related logs by
    leveraging `LogParts`.

    Attributes:
        log (Logger): Underlying logger instance used for output.
    """

    def __init__(self, logger: Logger):
        """
        Initialize the PipelineLogger.

        Args:
            logger (Logger): Core logger instance used for emitting logs.
        """
        self.log = logger

    # ===== PIPELINE LIFECYCLE =====

    def start(self, total: int, concurrency: int):
        """
        Log the start of the pipeline execution.

        Args:
            total (int): Total number of URLs to process.
            concurrency (int): Number of concurrent workers.
        """
        self.log.separator()
        rows = [
            "Pipeline started:",
            LP.total(total),
            LP.concurrency(concurrency)
        ]
        self.log.rows(rows)

    def summary(self, stats: Counts) -> None:
        """
        Log the final summary of the pipeline execution.

        Args:
            stats (Counts): Dictionary containing aggregated counts
                of scraping results (e.g., success, failed, timeout).
        """
        self.log.separator()
        data = [LP.kv(key.value, value) for key, value in stats.items()]
        rows = [
            "Pipeline completed:",
            *data
        ]
        self.log.rows(rows)
        self.log.separator()

    # ===== CONTROL FLOW EVENTS =====

    def no_urls(self):
        """Log that the pipeline terminated because no URLs were provided."""
        self.log.warning(LP.pipeline_terminated("No URLs to process."))

    def no_results(self):
        """
        Log that the pipeline terminated because no results were produced.
        """
        self.log.warning(LP.pipeline_terminated("No results produced."))

    def interrupted(self):
        """Log that the pipeline was interrupted by user action."""
        self.log.warning(LP.pipeline_terminated("Interrupted by user."))

    def exception(self, e: Exception):
        """
        Log an exception that occurred during pipeline execution.

        Args:
            e (Exception): Exception that occurred.
        """
        self.log.exception(f"Pipeline exception: {e}")

    # ===== SCRAPING FALLBACKS =====

    def fallback(self, id: int, url: str, status: str) -> None:
        """
        Log a fallback event where browser-based scraping was used.

        Args:
            id (int): Item ID.
            url (str): URL that was scraped.
            status (str): Status or reason for using fallback.
        """
        rows = [
            LP.id(id),
            "[FALLBACK_BROWSER]",
            LP.url(url),
            LP.reason(status)
        ]
        self.log.rows(rows)

    # ===== CONFIGURATION =====

    def settings(
        self,
        http_timeout: float,
        browser_timeout: float,
        retries: int,
        concurrency: int
    ) -> None:
        """
        Log the loaded configuration settings.

        Args:
            http_timeout (float): HTTP request timeout.
            browser_timeout (float): Browser operation timeout.
            retries (int): Number of retry attempts.
            concurrency (int): Number of concurrent workers.
        """
        self.log.separator()
        rows = [
            "Settings loaded:",
            LP.source(".env"),
            LP.http_timeout(http_timeout),
            LP.browser_timeout(browser_timeout),
            LP.retries(retries),
            LP.concurrency(concurrency)
        ]
        self.log.rows(rows)

    # ===== PROXY EVENTS =====

    def proxy_fail(self, e: Exception):
        """
        Log an error during proxy manager initialization.

        Args:
            e (Exception): Exception that occurred.
        """
        self.log.error(f"Failed to initialize proxy manager: {e}")

    def proxy_success(self, hostname: str):
        """
        Log successful proxy initialization.

        Args:
            hostname (str): Hostname of the loaded proxy.
        """
        rows = [
            "Loaded proxy for",
            LP.hostname(hostname)
        ]
        self.log.rows(rows)
