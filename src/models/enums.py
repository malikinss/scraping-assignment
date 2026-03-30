# ./src/models/enums.py

from enum import Enum


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


class ScrapeMethod(str, Enum):
    """
    Enum representing the method used for scraping.
    """

    HTTPX = "httpx"          # Using httpx client
    PLAYWRIGHT = "playwright"  # Using Playwright browser
