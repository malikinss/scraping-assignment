# ./src/scrapers/result_builder.py

from .deps import (
    time,
    detector,
    Logger,
    URLUtils,
    ScrapeMethod,
    ScrapeResult,
    ScrapeStatus,
    Callable,
    URL,
    Optional
)

logger = Logger("ResultBuilder")
Builder = Callable[[int, URL], ScrapeResult]


class ResultBuilder:
    """
    Helper class to construct structured ScrapeResult objects for a scraper.

    Tracks latency, computes content length, logs results, and provides
    convenient builders for various statuses (success, failure, timeout, 
    CAPTCHA, blocked, empty, PDF, etc.).

    Attributes:
        method (ScrapeMethod): Scraping method used (HTTPX, PLAYWRIGHT, etc.)
        _start (float): Timestamp when scraping started, used for latency calculation.
    """

    def __init__(self, method: ScrapeMethod):
        """
        Initialize the ResultBuilder with a scraping method.

        Args:
            method (ScrapeMethod): Enum indicating the scraping method used.
        """
        self.method: ScrapeMethod = method
        self._start: float = time.perf_counter()

    # ===== TIME =====

    def start_timer(self) -> None:
        """
        Reset the internal timer to the current time.

        Call this before starting a scrape operation to measure its duration.

        Returns:
            None
        """
        self._start = time.perf_counter()

    def calc_latency(self) -> float:
        """
        Calculate the elapsed time since the timer was started.

        Returns:
            float: Latency in seconds (non-negative).
        """
        return max(time.perf_counter() - self._start, 0.0)

    # ===== BUILDERS =====

    def build_success(self, id: int, url: URL, text: str) -> ScrapeResult:
        """
        Build a successful ScrapeResult.

        Calculates latency and content length, logs the result, and returns
        a ScrapeResult with status SUCCESS.

        Args:
            id (int): Request identifier.
            url (URL): Target URL.
            text (str): Scraped text content.

        Returns:
            ScrapeResult: Success result with content and metadata.
        """
        latency: float = self.calc_latency()
        content_length: int = len(text)

        status = ScrapeStatus.SUCCESS
        self._log(status, id, url, latency, content_length)
        result = ScrapeResult(
            id=id,
            url=url,
            method=self.method,
            status=status,
            latency=latency,
            content=text,
            content_length=content_length,
            error=None,
        )

        return result

    def build_failure(
            self,
            id: int,
            url: URL,
            error: str,
            status: ScrapeStatus = ScrapeStatus.FAILED
    ) -> ScrapeResult:
        """
        Build a failed ScrapeResult.

        Calculates latency, logs the failure, and returns a ScrapeResult
        with the given status and error message.

        Args:
            id (int): Request identifier.
            url (URL): Target URL.
            error (str): Error message describing the failure.
            status (ScrapeStatus, optional): Failure status. Defaults to FAILED.

        Returns:
            ScrapeResult: Failure result with error and metadata.
        """
        latency: float = self.calc_latency()

        self._log(status, id, url, latency, 0, error)
        result = ScrapeResult(
            id=id,
            url=url,
            method=self.method,
            status=status,
            latency=latency,
            content_length=0,
            error=error,
        )

        return result

    # ===== LOGGING =====

    def _log(
        self,
        status: ScrapeStatus,
        id: int,
        url: URL,
        latency: float,
        content_length: int,
        error: Optional[str] = None
    ) -> str:
        """
        Format a log message for the given status.

        Args:
            status (ScrapeStatus): Current status.
            id (int): Request identifier.
            url (URL): Target URL.
            latency (float): Elapsed time in seconds.
            content_length (int): Length of content.
            error (Optional[str]): Error message, if any.

        Returns:
            str: Formatted log message.
        """
        msg: str = (
            f"[ID:{id}]"
            f"[{self.method.value.upper()}] "
            f"[{status.value.upper()}] "
            f"url={URLUtils.short_url(url)} "
            f"latency={latency:.3f}s "
            f"content_length={content_length} "
            f"error={error or "N/A"}"
        )

        if status == ScrapeStatus.SUCCESS:
            logger.info(msg)
        elif status in (ScrapeStatus.TIMEOUT, ScrapeStatus.CAPTCHA):
            logger.warning(msg)
        elif status == ScrapeStatus.FAILED:
            logger.error(msg)
        elif status == ScrapeStatus.BLOCKED:
            logger.info(msg)
        else:
            logger.debug(msg)

    # ===== SHORTCUTS =====

    def build_empty(self, id: int, url: URL) -> ScrapeResult:
        """
        Build an empty response ScrapeResult.

        Args:
            id (int): Request identifier.
            url (URL): Target URL.

        Returns:
            ScrapeResult: Empty result with status EMPTY.
        """
        return self.build_failure(
            id,
            url,
            "Empty response",
            ScrapeStatus.EMPTY
        )

    def build_blocked(self, id: int, url: URL) -> ScrapeResult:
        """
        Build a blocked response ScrapeResult.

        Args:
            id (int): Request identifier.
            url (URL): Target URL.

        Returns:
            ScrapeResult: Blocked result with status BLOCKED.
        """
        status = ScrapeStatus.BLOCKED
        return self.build_failure(id, url, "Blocked by site", status)

    def build_captcha(self, id: int, url: URL) -> ScrapeResult:
        """
        Build a CAPTCHA response ScrapeResult.

        Args:
            id (int): Request identifier.
            url (URL): Target URL.

        Returns:
            ScrapeResult: CAPTCHA result with status CAPTCHA.
        """
        status = ScrapeStatus.CAPTCHA
        return self.build_failure(id, url, "CAPTCHA found", status)

    def build_pdf(self, id: int, url: URL) -> ScrapeResult:
        """
        Build a PDF response ScrapeResult.

        Args:
            id (int): Request identifier.
            url (URL): Target URL.

        Returns:
            ScrapeResult: PDF result with status PDF.
        """
        status = ScrapeStatus.PDF
        return self.build_failure(id, url, "PDF found", status)

    def build_timeout(self, id: int, url: URL) -> ScrapeResult:
        """
        Build a timeout response ScrapeResult.

        Args:
            id (int): Request identifier.
            url (URL): Target URL.

        Returns:
            ScrapeResult: Timeout result with status TIMEOUT.
        """
        status = ScrapeStatus.TIMEOUT
        return self.build_failure(id, url, "Timeout", status)

    # ===== MAIN ENTRY =====

    def process(self, id: int, url: URL, text: str) -> ScrapeResult:
        """
        Process scraped text and return the appropriate ScrapeResult.

        Detects issues like empty content, CAPTCHA, blocks, or PDFs,
        and uses the appropriate builder method.

        Args:
            id (int): Request identifier.
            url (URL): Target URL.
            text (str): Scraped text content.

        Returns:
            ScrapeResult: Structured result with appropriate status.
        """
        if not text or not text.strip():
            return self.build_empty(id, url)

        status: ScrapeStatus = detector.detect(text)
        if status == ScrapeStatus.SUCCESS:
            return self.build_success(id, url, text)

        # fallback for detected issues
        status_map: dict[ScrapeStatus, Builder] = {
            ScrapeStatus.CAPTCHA: self.build_captcha,
            ScrapeStatus.BLOCKED: self.build_blocked,
            ScrapeStatus.EMPTY: self.build_empty,
        }

        builder: Builder = status_map.get(status)

        if builder:
            return builder(id, url)

        return self.build_success(id, url, text)
