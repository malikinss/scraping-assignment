# ./src/utils/__init__.py

"""
Utils Package
-------------

This package provides utility functions for URL manipulation and validation.
It includes methods for parsing URLs, checking file types, extracting domains,
shortening URLs, and validating URL formats.

Core Components:
    - URLUtils: Utility class for URL manipulation and validation.

Key Responsibilities:
    - Parse URLs into components.
    - Check if URLs point to PDF files.
    - Extract domains from URLs.
    - Shorten URLs to a maximum length.
    - Get the path from URLs.
    - Validate URLs.
"""

from .url_utils import URLUtils

__all__ = ["URLUtils"]
