# ./src/models/enums.py

from .deps import Enum


class ScrapeStatus(str, Enum):
    """
    Enum representing the status of a scraping result.
    """

    SUCCESS = "success"      # Successfully scraped
    TIMEOUT = "timeout"      # Request timed out
    CAPTCHA = "captcha"      # CAPTCHA encountered
    BLOCKED = "blocked"      # Access blocked
    EMPTY = "empty"          # Content empty
    PDF = "pdf"              # PDF content
    IMAGE = "image"          # Image content
    VIDEO = "video"          # Video content
    AUDIO = "audio"          # Audio content
    FAILED = "failed"        # Generic failure

    @classmethod
    def success_statuses(cls) -> set[str]:
        """
        Returns a set of success statuses.
        """
        return {cls.SUCCESS, cls.PDF, cls.IMAGE, cls.VIDEO, cls.AUDIO}

    @classmethod
    def non_success_statuses(cls) -> set[str]:
        """
        Returns a set of non-success statuses.
        """
        return {cls.TIMEOUT, cls.CAPTCHA, cls.BLOCKED, cls.EMPTY, cls.FAILED}

    @classmethod
    def content_statuses(cls) -> set[str]:
        """
        Returns a set of content statuses.
        """
        return {cls.PDF, cls.IMAGE, cls.VIDEO, cls.AUDIO}

    @property
    def is_success(self) -> bool:
        """
        Returns True if the status is a success status.
        """
        return self in self.success_statuses()

    @property
    def is_non_success(self) -> bool:
        """
        Returns True if the status is a non-success status.
        """
        return self in self.non_success_statuses()

    @property
    def is_content(self) -> bool:
        """
        Returns True if the status is a content status.
        """
        return self in self.content_statuses()


class ScrapeMethod(str, Enum):
    """
    Enum representing the method used for scraping.
    """

    HTTPX = "httpx"          # Using httpx client
    PLAYWRIGHT = "playwright"  # Using Playwright browser

    @classmethod
    def default(cls) -> "ScrapeMethod":
        """
        Returns default scraping method.
        """
        return cls.HTTPX
