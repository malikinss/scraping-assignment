# ./src/models/enums.py

"""
Enumerations for core domain concepts in the scraping system.

This module defines the `ScrapeStatus` and `ScrapeMethod` enums,
providing a type-safe and expressive way to represent scraping
outcomes and operational choices.

Key Concepts:
    - ScrapeStatus: Represents all possible outcomes of a scraping
      operation, including success, failure, and content-type
      classifications.
    - ScrapeMethod: Represents the underlying engine used for scraping,
      supporting both HTTP client and browser automation approaches.

These enums are central to the domain model and are used throughout
the system for classification, routing, and reporting.
"""

from .deps import Enum


class ScrapeStatus(str, Enum):
    """
    Enum representing the status of a scraping operation.

    This enum defines all possible outcomes of a scraping attempt,
    including success states, failure reasons, and content-type
    classifications.
    """

    SUCCESS = "success"      # Successfully scraped
    FAILED = "failed"        # Generic failure

    TIMEOUT = "timeout"      # Request timed out
    CAPTCHA = "captcha"      # CAPTCHA encountered
    BLOCKED = "blocked"      # Access blocked
    EMPTY = "empty"          # Empty response

    PDF = "pdf"              # PDF content detected
    IMAGE = "image"          # Image content detected
    VIDEO = "video"          # Video content detected
    AUDIO = "audio"          # Audio content detected

    # ===== CLASSIFIERS =====

    @classmethod
    def success_statuses(cls) -> set["ScrapeStatus"]:
        """
        Return the set of statuses considered successful.

        Includes both direct success responses and content-type
        based successful results.

        Returns:
            set[ScrapeStatus]: Set of success-related statuses.
        """
        return {cls.SUCCESS, *cls.content_statuses()}

    @classmethod
    def non_success_statuses(cls) -> set["ScrapeStatus"]:
        """
        Return the set of statuses considered non-successful.

        These statuses represent failed or blocked scraping attempts.

        Returns:
            set[ScrapeStatus]: Set of failure-related statuses.
        """
        return {cls.TIMEOUT, cls.CAPTCHA, cls.BLOCKED, cls.EMPTY, cls.FAILED}

    @classmethod
    def content_statuses(cls) -> set["ScrapeStatus"]:
        """
        Return the set of content-type statuses.

        These represent successful retrieval of non-HTML content.

        Returns:
            set[ScrapeStatus]: Set of content-related statuses.
        """
        return {cls.PDF, cls.IMAGE, cls.VIDEO, cls.AUDIO}

    # ===== INSTANCE PROPERTIES =====

    @property
    def is_success(self) -> bool:
        """
        Check if the status represents a successful result.

        Returns:
            bool: True if status is considered successful.
        """
        return self in self.success_statuses()

    @property
    def is_failure(self) -> bool:
        """
        Check if the status represents a failure.

        Returns:
            bool: True if status is considered a failure.
        """
        return self in self.non_success_statuses()

    @property
    def is_content(self) -> bool:
        """
        Check if the status represents content-type data.

        Returns:
            bool: True if status represents media/content response.
        """
        return self in self.content_statuses()

    # ===== FAST LOOKUP MAP =====

    @classmethod
    def from_name(cls, name: str) -> "ScrapeStatus":
        MAP = {
            "success": cls.SUCCESS,
            "failed": cls.FAILED,
            "timeout": cls.TIMEOUT,
            "captcha": cls.CAPTCHA,
            "blocked": cls.BLOCKED,
            "empty": cls.EMPTY,
            "pdf": cls.PDF,
            "image": cls.IMAGE,
            "video": cls.VIDEO,
            "audio": cls.AUDIO,
        }
        return MAP.get(name.lower(), cls.FAILED)


class ScrapeMethod(str, Enum):
    """
    Enum representing supported scraping methods.

    This defines which engine is used to perform the scraping
    operation (HTTP client or browser automation).
    """

    HTTPX = "httpx"              # Using httpx client
    PLAYWRIGHT = "playwright"    # Using Playwright browser automation

    @classmethod
    def default(cls) -> "ScrapeMethod":
        """
        Return the default scraping method.

        Returns:
            ScrapeMethod: Default method used for scraping.
        """
        return cls.HTTPX

    @classmethod
    def from_name(cls, name: str) -> "ScrapeMethod":
        """
        Convert a string to a ScrapeMethod.

        Args:
            name: String to convert

        Returns:
            ScrapeMethod: Converted ScrapeMethod
        """
        _ALIAS_MAP = {
            "http": cls.HTTPX,
            "httpx": cls.HTTPX,
            "requests": cls.HTTPX,
            "browser": cls.PLAYWRIGHT,
            "playwright": cls.PLAYWRIGHT,
            "chromium": cls.PLAYWRIGHT,
        }

        if not name:
            return cls.default()

        normalized = name.strip().lower()

        return _ALIAS_MAP.get(normalized, cls.default())
