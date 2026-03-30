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
        """
        logger.debug("Detecting content")

        if not content or self._is_empty(content):
            logger.debug("Content is empty")
            return ScrapeStatus.EMPTY

        if self._is_captcha(content):
            logger.debug("Content is captcha")
            return ScrapeStatus.CAPTCHA

        if self._is_blocked(content):
            logger.debug("Content is blocked")
            return ScrapeStatus.BLOCKED

        logger.debug("Content is success")
        return ScrapeStatus.SUCCESS

    def _is_empty(self, content: str) -> bool:
        """
        Returns True if the content is considered empty (short).

        Args:
            content (str): The text content to analyze.

        Returns:
            bool: True if the content is considered empty.
        """
        return len(content.strip()) < 100

    def _is_captcha(self, content: str) -> bool:
        """
        Returns True if the content likely contains a CAPTCHA challenge.

        Args:
            content (str): The text content to analyze.

        Returns:
            bool: True if the content likely contains a CAPTCHA challenge.
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
        """
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in keywords)


# Singleton instance for convenience
detector = ContentDetector()
