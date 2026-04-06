# ./src/utils/url_utils.py

from .deps import urlparse


class URLUtils:
    """
    Utility class for working with URLs.
    """

    __slots__ = ()

    @staticmethod
    def is_pdf(url: str) -> bool:
        """
        Checks whether the URL points to a PDF file.

        Handles query params and fragments.

        Example:
            >>> is_pdf("file.pdf?download=1") -> True
        """
        path = urlparse(url).path.lower()
        return path.endswith(".pdf")

    @staticmethod
    def get_domain(url: str, strip_www: bool = True) -> str:
        """
        Extracts domain from URL.

        Args:
            url (str): Input URL
            strip_www (bool): Remove 'www.' prefix

        Returns:
            str: Domain name
        """
        netloc = urlparse(url).netloc.lower()

        if strip_www and netloc.startswith("www."):
            return netloc[4:]

        return netloc

    @staticmethod
    def short_url(url: str, max_length: int = 50) -> str:
        """
        Truncates URL for logging purposes.

        Args:
            url (str): URL to shorten
            max_length (int): Maximum length of result

        Returns:
            str: Shortened URL

        Example:
            >>> short_url("https://example.com/very/long/path", 20)
            'https://example...'
        """
        if len(url) <= max_length:
            return url

        return url[: max_length - 3] + "..."

    @staticmethod
    def get_path(url: str) -> str:
        """
        Extracts path from URL.

        Example:
            >>> get_path("https://example.com/a/b") -> "/a/b"
        """
        return urlparse(url).path

    @staticmethod
    def is_valid(url: str) -> bool:
        """
        Basic validation of URL.

        Returns:
            bool: True if URL has scheme and netloc
        """
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
