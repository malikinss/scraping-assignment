# ./src/scrapers/result_builder.py

from .deps import (
    time,
    detector,
    Logger,
    ScrapeMethod,
    ScrapeResult,
    ScrapeStatus,
)

logger = Logger(__name__)


class ResultBuilder:
    """
    Builder for constructing `ScrapeResult` objects.

    This class encapsulates the logic for measuring request latency and
    generating standardized `ScrapeResult` instances for different
    scraping outcomes (success, failure, blocked, captcha, etc.).

    It also provides a high-level `process` method that analyzes response
    content and determines the appropriate result type automatically.
    """

    def __init__(self, method: ScrapeMethod):
        """
        Initialize the result builder and start the timer.

        Args:
            method (ScrapeMethod): The scraping method used.
        """
        self.method: ScrapeMethod = method
        self.start: float = time.perf_counter()
        logger.debug(f"ResultBuilder initialized (method={self.method})")

    def start_timer(self) -> None:
        """
        Start the latency timer.

        Records the current high-resolution timestamp to be used later
        for latency calculation.
        """
        self.start = time.perf_counter()
        logger.debug("Timer started")

    def calc_latency(self) -> float:
        """
        Calculate the elapsed time since the timer was started.

        Returns:
            float: The latency in seconds. Returns 0.0 if the timer
                was not started.

        Logs:
            Warning if the timer was not started before calling this method.
        """
        if self.start == 0:
            logger.warning("Latency requested before timer start")
            return 0.0
        latency = time.perf_counter() - self.start
        logger.debug(f"Latency calculated: {latency:.3f}s")
        return latency

    # --- Core builders ---
    def build_success(self, url: str, text: str) -> ScrapeResult:
        """
        Build a successful scrape result.

        Args:
            url (str): The URL that was scraped.
            text (str): The retrieved content.

        Returns:
            ScrapeResult: A result object marked as SUCCESS with content
                and computed metadata.

        Logs:
            Info message with URL, method, latency, and content length.
        """
        latency = self.calc_latency()
        content_length = len(text)

        logger.info(
            f"SUCCESS url={url} method={self.method} "
            f"latency={latency:.3f}s length={content_length}"
        )

        return ScrapeResult(
            url=url,
            method=self.method,
            latency=latency,
            content=text,
            content_length=content_length,
            status=ScrapeStatus.SUCCESS,
            error=None,
        )

    def build_failure(
            self,
            url: str,
            error: str,
            status: ScrapeStatus = ScrapeStatus.FAILED
    ) -> ScrapeResult:
        """
        Build a failed scrape result.

        Args:
            url (str): The URL that failed to be scraped.
            error (str): A human-readable error message.
            status (ScrapeStatus, optional): Specific failure status.
                Defaults to `ScrapeStatus.FAILED`.

        Returns:
            ScrapeResult: A result object representing the failure.

        Logs:
            Warning message with URL, method, latency, and error.
        """
        latency = self.calc_latency()

        logger.warning(
            f"{status.value.upper()} url={url} method={self.method} "
            f"latency={latency:.3f}s error={error}"
        )

        return ScrapeResult(
            url=url,
            method=self.method,
            status=status,
            latency=latency,
            error=error,
            content_length=0,
        )

    # --- Shortcuts ---
    def build_empty(self, url: str) -> ScrapeResult:
        """
        Build an empty response result.

        Args:
            url (str): The URL that had an empty response.

        Returns:
            ScrapeResult: A result object marked as EMPTY.

        Logs:
            Debug message with URL.
        """
        logger.debug(f"Detected empty response: url={url}")
        return self.build_failure(url, "Empty response", ScrapeStatus.EMPTY)

    def build_blocked(self, url: str) -> ScrapeResult:
        """
        Build a blocked response result.

        Args:
            url (str): The URL that was blocked.

        Returns:
            ScrapeResult: A result object marked as BLOCKED.

        Logs:
            Debug message with URL.
        """
        logger.debug(f"Detected blocked page: url={url}")
        return self.build_failure(url, "Blocked by site", ScrapeStatus.BLOCKED)

    def build_captcha(self, url: str) -> ScrapeResult:
        """
        Build a CAPTCHA response result.

        Args:
            url (str): The URL that had a CAPTCHA.

        Returns:
            ScrapeResult: A result object marked as CAPTCHA.

        Logs:
            Debug message with URL.
        """
        logger.debug(f"Detected CAPTCHA: url={url}")
        return self.build_failure(url, "CAPTCHA found", ScrapeStatus.CAPTCHA)

    def build_pdf(self, url: str) -> ScrapeResult:
        """
        Build a PDF response result.

        Args:
            url (str): The URL that had a PDF.

        Returns:
            ScrapeResult: A result object marked as PDF.

        Logs:
            Debug message with URL.
        """
        logger.debug(f"Detected PDF content: url={url}")
        return self.build_failure(url, "PDF found", ScrapeStatus.PDF)

    def build_timeout(self, url: str) -> ScrapeResult:
        """
        Build a timeout response result.

        Args:
            url (str): The URL that timed out.

        Returns:
            ScrapeResult: A result object marked as TIMEOUT.

        Logs:
            Debug message with URL.
        """
        logger.debug(f"Timeout occurred: url={url}")
        return self.build_failure(url, "Timeout", ScrapeStatus.TIMEOUT)

    # --- Smart processor ---
    def process(self, url: str, text: str) -> ScrapeResult:
        """
        Process raw response content and build an appropriate result.

        This method applies validation and detection logic to determine
        the correct result type:
            - Empty content → EMPTY
            - CAPTCHA detected → CAPTCHA
            - Block detected → BLOCKED
            - Otherwise → SUCCESS

        Args:
            url (str): The URL that was scraped.
            text (str): The raw response content.

        Returns:
            ScrapeResult: The constructed result object based on detected
                          status.

        Logs:
            Debug message with URL and status.
        """
        logger.debug(f"Processing response: url={url}")

        if not text or not text.strip():
            return self.build_empty(url)

        status = detector.detect(text)
        logger.debug(f"Detection result: url={url} status={status}")

        if status == ScrapeStatus.CAPTCHA:
            return self.build_captcha(url)

        if status == ScrapeStatus.BLOCKED:
            return self.build_blocked(url)

        return self.build_success(url, text)
