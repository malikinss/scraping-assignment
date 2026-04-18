# ./src/utils/url_utils.py

"""
URL Utilities Module

This module provides utility functions for URL manipulation and validation.
It includes methods for parsing URLs, checking file types, extracting domains,
shortening URLs, and validating URL formats.

Core Components:
    - ParsedURL: Represents a parsed URL.

Key Responsibilities:
    - Parse URLs into components.
    - Check if URLs point to PDF files.
    - Extract domains from URLs.
    - Shorten URLs to a maximum length.
    - Get the path from URLs.
    - Validate URLs.
"""

from .deps import urlparse, URL, NamedTuple


class ParsedURL(NamedTuple):
    """Represents a parsed URL."""
    scheme: str
    netloc: str
    path: str


class URLUtils:
    """
    Utility class for URL manipulation and validation.
    """

    # ===== CORE =====
    @staticmethod
    def parse(url: URL) -> ParsedURL:
        """
        Parse a URL into its components.

        Args:
            url: URL to parse

        Returns:
            ParsedURL: Parsed URL with scheme, netloc, and path
        """
        p = urlparse(url)
        return ParsedURL(
            scheme=p.scheme,
            netloc=p.netloc,
            path=p.path
        )

    # ===== PUBLIC API =====

    @classmethod
    def is_pdf(cls, url: URL) -> bool:
        """
        Check if the URL points to a PDF file.

        Args:
            url: URL to check

        Returns:
            bool: True if the URL points to a PDF file, False otherwise
        """
        parsed = cls.parse(url)
        return parsed.path.lower().endswith(".pdf")

    @classmethod
    def get_domain(cls, url: URL, strip_www: bool = True) -> str:
        """
        Get the domain from a URL.

        Args:
            url: URL to get the domain from
            strip_www: Whether to strip the www subdomain

        Returns:
            str: Domain of the URL
        """
        parsed = cls.parse(url)
        netloc = parsed.netloc

        if strip_www and netloc.startswith("www."):
            return netloc[4:]

        return netloc

    @staticmethod
    def short_url(url: URL, max_length: int = 50) -> str:
        """
        Shorten a URL to a maximum length.

        Args:
            url: URL to shorten
            max_length: Maximum length of the shortened URL

        Returns:
            str: Shortened URL
        """
        if len(url) <= max_length:
            return url

        return f"{url[: max_length - 3]}..."

    @classmethod
    def get_path(cls, url: URL) -> str:
        """
        Get the path from a URL.

        Args:
            url: URL to get the path from

        Returns:
            str: Path of the URL
        """
        parsed = cls.parse(url)
        return parsed.path

    @classmethod
    def is_valid(cls, url: URL) -> bool:
        """
        Check if the URL is valid.

        Args:
            url: URL to check

        Returns:
            bool: True if the URL is valid, False otherwise
        """
        if not url or " " in url:
            return False

        parsed = cls.parse(url)

        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
        )
