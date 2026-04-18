# ./src/services/content_detector/content_detector.py

"""
Content Detector Service
========================

This module provides a structured way to detect the status of scraped content
based on predefined rules.

Key Features:
    - Rule-based content detection
    - Empty content detection with threshold
    - Common blocking and captcha patterns
    - Singleton instance for easy access

Classes:
    Rule: Represents a detection rule.
    ContentDetector: Handles content detection logic.

Usage:
    >>> from src.services.content_detector import detector
    >>> status = detector.detect(content)
    >>> print(status)

Example:
    >>> content = "403 Forbidden"
    >>> status = detector.detect(content)
    >>> print(status)
    ScrapeStatus.BLOCKED

"""

from .deps import ScrapeStatus, dataclass, Tuple

KeyWords = Tuple[str, ...]


@dataclass(frozen=True)
class Rule:
    """
    Rule for content detection.

    Attributes:
        status (ScrapeStatus): The status of the scrape.
        keywords (KeyWords): The keywords to match.
    """
    status: ScrapeStatus
    keywords: KeyWords


Rules = Tuple[Rule, ...]


class ContentDetector:
    """
    ContentDetector class for content detection.

    Attributes:
        EMPTY_THRESHOLD (int): The threshold for empty content.
        rules (Rules): The rules for content detection.
    """

    # ===== CONSTANTS =====
    EMPTY_THRESHOLD: int = 100
    rules: Rules = (
        Rule(
            status=ScrapeStatus.CAPTCHA,
            keywords=(
                "captcha",
                "verify you are human",
                "i am not a robot",
                "cloudflare",
                "recaptcha"
            )
        ),
        Rule(
            status=ScrapeStatus.BLOCKED,
            keywords=(
                "access denied",
                "forbidden",
                "blocked",
                "403",
                "request blocked"
            )
        ),
    )

    # ===== PUBLIC =====
    def detect(self, content: str) -> ScrapeStatus:
        """
        Detect the status of the scrape.

        Args:
            content (str): The content of the scrape.

        Returns:
            ScrapeStatus: The status of the scrape.
        """
        if not content or self._is_empty(content):
            return ScrapeStatus.EMPTY

        content_lower = content.lower()

        for rule in self.rules:
            if self._match(rule.keywords, content_lower):
                return rule.status

        return ScrapeStatus.SUCCESS

    # ===== RULE ENGINE =====
    def _match(self, keywords: KeyWords, content: str) -> bool:
        """
        Check if any of the keywords match the content.

        Args:
            keywords (KeyWords): The keywords to match.
            content (str): The content to match.

        Returns:
            bool: True if any of the keywords match the content,
                  False otherwise.
        """
        return any(keyword in content for keyword in keywords)

    def _is_empty(self, content: str) -> bool:
        """
        Check if the content is empty.

        Args:
            content (str): The content to check.

        Returns:
            bool: True if the content is empty, False otherwise.
        """
        if not content:
            return True
        return len(content.strip()) < self.EMPTY_THRESHOLD


# Singleton instance for convenience
detector = ContentDetector()
