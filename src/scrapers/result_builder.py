# ./src/scrapers/result_builder.py

from .deps import (
    time,
    detector,
    Logger,
    URLUtils,
    ScrapeMethod,
    ScrapeResult,
    ScrapeStatus,
    Callable
)

logger = Logger("ResultBuilder")


class ResultBuilder:
    """
    Builder for constructing `ScrapeResult` objects.

    Encapsulates logic for measuring request latency and generating
    standardized `ScrapeResult` instances for different outcomes:
    SUCCESS, FAILED, BLOCKED, CAPTCHA, EMPTY, TIMEOUT, PDF, etc.

    Provides both low-level builders and a high-level `process` method
    that automatically determines the result type based on response content.
    """

    def __init__(self, method: ScrapeMethod):
        """
        Initialize the result builder and start the latency timer.

        Args:
            method (ScrapeMethod): The scraping method used.
        """
        self.method: ScrapeMethod = method
        self.start: float = time.perf_counter()

    def start_timer(self) -> None:
        """
        Start the latency timer.

        Records the current high-resolution timestamp to be used later
        for latency calculation.
        """
        self.start = time.perf_counter()

    def calc_latency(self) -> float:
        """
        Calculate the elapsed time since the timer was started.

        Returns:
            float: The latency in seconds. Returns 0.0 if the timer
                   was not started.
        """
        if not hasattr(self, 'start') or self.start is None:
            logger.warning("Timer not started; returning 0 latency")
            return 0.0
        return max(time.perf_counter() - self.start, 0.0)

    # --- Core builders ---
    def build_success(self, id: int, url: str, text: str) -> ScrapeResult:
        """
        Build a successful scrape result.

        Args:
            id (int): The scrape ID.
            url (str): The URL that was scraped.
            text (str): The retrieved content.

        Returns:
            ScrapeResult: A result object with status SUCCESS and metadata.
        """
        latency = self.calc_latency()
        content_length = len(text)
        msg = self.build_log_message(
            ScrapeStatus.SUCCESS,
            id,
            url,
            latency,
            content_length
        )
        logger.info(msg)

        return ScrapeResult(
            id=id,
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
            id: int,
            url: str,
            error: str,
            status: ScrapeStatus = ScrapeStatus.FAILED
    ) -> ScrapeResult:
        """Build a failed scrape result.

        Args:
            id (int): The scrape ID.
            url (str): The URL that failed to be scraped.
            error (str): A human-readable error message.
            status (ScrapeStatus, optional): Specific failure status.
                                             Defaults to ScrapeStatus.FAILED.

        Returns:
            ScrapeResult: A result object representing the failure.
        """
        latency = self.calc_latency()
        msg = self.build_log_message(status, id, url, latency, 0, error)

        if status == ScrapeStatus.FAILED:
            logger.error(msg)
        elif status in (
            ScrapeStatus.CAPTCHA,
            ScrapeStatus.TIMEOUT,
        ):
            logger.warning(msg)
        elif status == ScrapeStatus.BLOCKED:
            logger.info(msg)
        else:
            logger.debug(msg)

        return ScrapeResult(
            id=id,
            url=url,
            method=self.method,
            status=status,
            latency=latency,
            error=error,
            content_length=0,
        )

    def build_log_message(
        self,
        status: ScrapeStatus,
        id: int,
        url: str,
        latency: float,
        content_length: int,
        error: str = None
    ) -> str:
        """
        Construct a standardized log message for a scrape result.

        Args:
            status (ScrapeStatus): The status of the scrape.
            id (int): The scrape ID.
            url (str): The scraped URL.
            latency (float): Latency in seconds.
            content_length (int): Length of response content.
            error (str, optional): Error message if present.

        Returns:
            str: Formatted log message.
        """
        return (
            f"[ID: {id}] "
            f"[{status.value.upper()}]"
            f"[{self.method.value.upper()}] "
            f"url={URLUtils.short_url(url)} "
            f"latency={latency:.3f}s "
            f"content_length={content_length} "
            f"error={error or "N/A"}"
        )

    # --- Shortcuts ---
    def build_empty(self, id: int, url: str) -> ScrapeResult:
        """
        Build a result for an empty response.

        Args:
            id (int): The scrape ID.
            url (str): The URL with empty response.

        Returns:
            ScrapeResult: Result object marked as EMPTY.
        """
        return self.build_failure(
            id,
            url,
            "Empty response",
            ScrapeStatus.EMPTY
        )

    def build_blocked(self, id: int, url: str) -> ScrapeResult:
        """
        Build a result for a blocked response.

        Args:
            id (int): The scrape ID.
            url (str): The blocked URL.

        Returns:
            ScrapeResult: Result object marked as BLOCKED.
        """
        return self.build_failure(
            id,
            url,
            "Blocked by site",
            ScrapeStatus.BLOCKED
        )

    def build_captcha(self, id: int, url: str) -> ScrapeResult:
        """
        Build a result for a CAPTCHA response.

        Args:
            id (int): The scrape ID.
            url (str): The URL where CAPTCHA was detected.

        Returns:
            ScrapeResult: Result object marked as CAPTCHA.
        """
        return self.build_failure(
            id,
            url,
            "CAPTCHA found",
            ScrapeStatus.CAPTCHA
        )

    def build_pdf(self, id: int, url: str) -> ScrapeResult:
        """
        Build a result for a PDF response.

        Args:
            id (int): The scrape ID.
            url (str): The URL pointing to a PDF.

        Returns:
            ScrapeResult: Result object marked as PDF.
        """
        return self.build_failure(
            id,
            url,
            "PDF found",
            ScrapeStatus.PDF
        )

    def build_timeout(self, id: int, url: str) -> ScrapeResult:
        """
        Build a result for a timeout response.

        Args:
            id (int): The scrape ID.
            url (str): The URL that timed out.

        Returns:
            ScrapeResult: Result object marked as TIMEOUT.
        """
        return self.build_failure(
            id,
            url,
            "Timeout",
            ScrapeStatus.TIMEOUT
        )

    # --- Smart processor ---
    def process(self, id: int, url: str, text: str) -> ScrapeResult:
        """
        Process raw response content and determine the correct result type.

        Applies validation and detection logic:
            - Empty or whitespace-only content → EMPTY
            - CAPTCHA detected → CAPTCHA
            - Block detected → BLOCKED
            - Otherwise → SUCCESS

        Args:
            id (int): The scrape ID.
            url (str): The URL that was scraped.
            text (str): Raw response content.

        Returns:
            ScrapeResult: The appropriate result object based on detected
                          status.
        """
        status_map = {
            ScrapeStatus.CAPTCHA: self.build_captcha,
            ScrapeStatus.BLOCKED: self.build_blocked,
            ScrapeStatus.EMPTY: self.build_empty,
        }

        if not text or not text.strip():
            return self.build_empty(id, url)

        status: ScrapeStatus = detector.detect(text)
        builder: Callable[[int, str], ScrapeResult] = status_map.get(
            status, self.build_success)

        if builder == self.build_success:
            result: ScrapeResult = builder(id, url, text)
        else:
            result: ScrapeResult = builder(id, url)

        return result
