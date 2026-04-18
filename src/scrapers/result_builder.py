# ./src/scrapers/result_builder.py

"""
Result Builder Module
=====================

This module provides a structured builder for creating ScrapeResult objects.
It uses the Logger class to log the status of each scrape operation.

Key Features:
    - Structured logging for scrape operations
    - Helper methods for different scrape statuses
    - Uses ScrapeResult for consistent result representation

Classes:
    ResultBuilder: Builder class for creating ScrapeResult objects

Dependencies:
    - src.scrapers.deps: Contains necessary imports for the module
    - src.logger: Contains Logger class for logging
    - src.scrapers.detector: Contains detector for detecting scrape status

Usage:
    >>> from src.scrapers import ResultBuilder
    >>> builder = ResultBuilder()
    >>> result = builder.success(ctx, "Some content")
    >>> print(result)

    ScrapeResult(
        id='some-id',
        url='https://example.com',
        method='GET',
        status=ScrapeStatus.SUCCESS,
        latency=0.5,
        content='Some content',
        content_length=12,
        error=None
    )

Example:
    >>> logger = Logger()
    >>> builder = ResultBuilder(logger)
    >>> builder.success(ctx, "Some content")
    Some content scraped:
        [id=some-id] [url=https://example.com] [method=GET] [latency=0.0005s]
        [size=12B]
    ScrapeResult(
        id='some-id',
        url='https://example.com',
        method='GET',
        status=ScrapeStatus.SUCCESS,
        latency=0.0005,
        content='Some content',
        content_length=12,
        error=None
    )
"""

from .deps import (
    time,
    detector,
    AppLogger,
    ScrapeResult,
    ScrapeStatus,
    ScraperContext,
    Callable,
    Optional,
)
Builder = Callable[[ScraperContext], ScrapeResult]

logger = AppLogger("ResultBuilder")


class ResultBuilder:
    """
    Builder class for creating ScrapeResult objects.

    Attributes:
        _STATUS_MAP (dict[ScrapeStatus, Builder]): Map of scrape statuses to
            builders.

    Methods:
        start_timer: Starts the timer for latency calculation.
        _latency: Calculates the latency.
        _build: Builds a ScrapeResult object.
        success: Builds a successful ScrapeResult.
        failure: Builds a failed ScrapeResult.
        empty: Builds an empty ScrapeResult.
        blocked: Builds a blocked ScrapeResult.
        captcha: Builds a captcha ScrapeResult.
        pdf: Builds a PDF ScrapeResult.
        timeout: Builds a timeout ScrapeResult.
        process: Processes a ScraperContext and builds a ScrapeResult.
    """
    _STATUS_MAP: dict[ScrapeStatus, Builder] = {}

    def __init__(self):
        """
        Initialize the ResultBuilder.

        Creates an instance of ResultBuilder.

        Attributes:
            _start (float): Timer for latency calculation.
        """
        self._start: float = 0.0

        # Initialize status map once
        if not self._STATUS_MAP:
            self._STATUS_MAP = {
                ScrapeStatus.CAPTCHA: self.captcha,
                ScrapeStatus.BLOCKED: self.blocked,
                ScrapeStatus.EMPTY: self.empty,
                ScrapeStatus.PDF: self.pdf,
                ScrapeStatus.TIMEOUT: self.timeout,
            }

        self.start_timer()

    # ===== TIME =====

    def start_timer(self) -> None:
        """
        Starts the timer for latency calculation.
        """
        self._start = time.perf_counter()

    def _latency(self) -> float:
        """
        Calculates the latency.

        Returns:
            float: The latency in seconds.
        """
        return max(time.perf_counter() - self._start, 0.0)

    # ===== BUILDERS =====

    def _build(
            self,
            ctx: ScraperContext,
            status: ScrapeStatus,
            content: Optional[str] = None,
            error: Optional[str] = None,
    ) -> ScrapeResult:
        """
        Builds a ScrapeResult object.

        Args:
            ctx (ScraperContext): The scraper context.
            status (ScrapeStatus): The status of the scrape.
            content (Optional[str]): The content of the scrape.
            error (Optional[str]): The error of the scrape.

        Returns:
            ScrapeResult: The ScrapeResult object.
        """
        latency: float = self._latency()
        content_length: int = len(content) if content is not None else 0

        logger.scraper.status(status, ctx, latency, content_length, error)

        result = ScrapeResult(
            id=ctx.id,
            url=ctx.url,
            method=ctx.method,
            status=status,
            latency=latency,
            content=content,
            content_length=content_length,
            error=error,
        )

        return result

    # ===== PUBLIC =====
    def success(self, ctx: ScraperContext, text: str) -> ScrapeResult:
        """
        Builds a successful ScrapeResult object.

        Args:
            ctx (ScraperContext): The scraper context.
            text (str): The content of the scrape.

        Returns:
            ScrapeResult: The successful ScrapeResult object.
        """
        return self._build(ctx, ScrapeStatus.SUCCESS, content=text)

    def failure(self, ctx: ScraperContext, error: str) -> ScrapeResult:
        """
        Builds a failed ScrapeResult object.

        Args:
            ctx (ScraperContext): The scraper context.
            error (str): The error message.

        Returns:
            ScrapeResult: The failed ScrapeResult object.
        """
        return self._build(ctx, ScrapeStatus.FAILED, error=error)

    # ===== SHORTCUTS =====

    def empty(self, ctx: ScraperContext) -> ScrapeResult:
        """
        Builds an empty ScrapeResult object.

        Args:
            ctx (ScraperContext): The scraper context.

        Returns:
            ScrapeResult: The empty ScrapeResult object.
        """
        return self._build(ctx, ScrapeStatus.EMPTY, error="Empty response")

    def blocked(self, ctx: ScraperContext) -> ScrapeResult:
        """
        Builds a blocked ScrapeResult object.

        Args:
            ctx (ScraperContext): The scraper context.

        Returns:
            ScrapeResult: The blocked ScrapeResult object.
        """
        return self._build(ctx, ScrapeStatus.BLOCKED, error="Blocked by site")

    def captcha(self, ctx: ScraperContext) -> ScrapeResult:
        """
        Builds a captcha ScrapeResult object.

        Args:
            ctx (ScraperContext): The scraper context.

        Returns:
            ScrapeResult: The captcha ScrapeResult object.
        """
        return self._build(ctx, ScrapeStatus.CAPTCHA, error="CAPTCHA found")

    def pdf(self, ctx: ScraperContext) -> ScrapeResult:
        """
        Builds a PDF ScrapeResult object.

        Args:
            ctx (ScraperContext): The scraper context.

        Returns:
            ScrapeResult: The PDF ScrapeResult object.
        """
        return self._build(ctx, ScrapeStatus.PDF, error="PDF found")

    def timeout(self, ctx: ScraperContext) -> ScrapeResult:
        """
        Builds a timeout ScrapeResult object.

        Args:
            ctx (ScraperContext): The scraper context.

        Returns:
            ScrapeResult: The timeout ScrapeResult object.
        """
        return self._build(ctx, ScrapeStatus.TIMEOUT, error="Timeout")

    # ===== MAIN ENTRY =====

    def process(self, ctx: ScraperContext, text: str) -> ScrapeResult:
        """
        Processes a ScraperContext and builds a ScrapeResult object.

        Args:
            ctx (ScraperContext): The scraper context.
            text (str): The content of the scrape.

        Returns:
            ScrapeResult: The ScrapeResult object.
        """
        if not text or not text.strip():
            return self.empty(ctx)

        status: ScrapeStatus = detector.detect(text)

        if status == ScrapeStatus.SUCCESS:
            return self.success(ctx, text)

        builder: Builder = self._STATUS_MAP.get(status)
        if builder:
            return builder(ctx)

        return self.failure(ctx, "Unknown error")
