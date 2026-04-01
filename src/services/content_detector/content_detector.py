# ./src/services/content_detector/content_detector.py

from .deps import (
    List,
    Logger,
    ScrapeStatus,
)

logger = Logger(__name__)


class ContentDetector:
    """
    Detects the type of content based on text analysis.
    """

    def detect(self, content: str) -> ScrapeStatus:
        """
        Detects the content status: SUCCESS, EMPTY, CAPTCHA, or BLOCKED.

        Args:
            content (str): The text content to analyze.

        Returns:
            ScrapeStatus: The detected status.

        Example:
            >>> detector = ContentDetector()
            >>> detector.detect("Some content")
            ScrapeStatus.SUCCESS
        """
        if not content:
            logger.debug("Content detection: EMPTY (no content)")
            return ScrapeStatus.EMPTY

        length = len(content)

        if self._is_empty(content):
            logger.debug(f"Content detection: EMPTY (length={length})")
            return ScrapeStatus.EMPTY

        if self._is_captcha(content):
            logger.debug(f"Content detection: CAPTCHA (length={length})")
            return ScrapeStatus.CAPTCHA

        if self._is_blocked(content):
            logger.debug(f"Content detection: BLOCKED (length={length})")
            return ScrapeStatus.BLOCKED

        logger.debug(f"Content detection: SUCCESS (length={length})")
        return ScrapeStatus.SUCCESS

    def _is_empty(self, content: str) -> bool:
        """
        Returns True if the content is considered empty (short).

        Args:
            content (str): The text content to analyze.

        Returns:
            bool: True if the content is considered empty.

        Example:
            >>> detector = ContentDetector()
            >>> detector._is_empty("Some content")
            False
        """
        return len(content.strip()) < 100

    def _is_captcha(self, content: str) -> bool:
        """
        Returns True if the content likely contains a CAPTCHA challenge.

        Args:
            content (str): The text content to analyze.

        Returns:
            bool: True if the content likely contains a CAPTCHA challenge.

        Example:
            >>> detector = ContentDetector()
            >>> detector._is_captcha("Some content")
            False
        """
        keywords: List[str] = [
            "captcha",
            "verify you are human",
            "i am not a robot",
            "cloudflare",
            "recaptcha"
        ]
        return self._contains_keywords(keywords, content)

    def _is_blocked(self, content: str) -> bool:
        """
        Returns True if the content indicates the request was blocked.

        Args:
            content (str): The text content to analyze.

        Returns:
            bool: True if the content indicates the request was blocked.

        Example:
            >>> detector = ContentDetector()
            >>> detector._is_blocked("Some content")
            False
        """
        keywords: List[str] = [
            "access denied",
            "forbidden",
            "blocked",
            "403",
            "request blocked"
        ]
        return self._contains_keywords(keywords, content)

    def _contains_keywords(self, keywords: List[str], content: str) -> bool:
        """
        Checks if any keyword is present in the content (case-insensitive).

        Args:
            keywords (List[str]): The keywords to search for.
            content (str): The text content to analyze.

        Returns:
            bool: True if any keyword is present in the content.

        Example:
            >>> detector = ContentDetector()
            >>> detector._contains_keywords(["captcha"], "captcha")
            True
        """
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in keywords)


# Singleton instance for convenience
detector = ContentDetector()
