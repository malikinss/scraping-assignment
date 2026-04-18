# ./src/scrapers/__init__.py
"""
Scrapers Package
==============

This package provides different types of scrapers for fetching content
from URLs. It includes:

- HTTPScraper: For making HTTP requests.
- BrowserScraper: For making browser-based requests using Playwright.

Key Features:
    - Async request handling
    - Retry mechanism
    - Timeout handling
    - PDF detection
    - Logging for each request

Classes:
    HTTPScraper: Scrapes content from URLs using HTTP requests.
    BrowserScraper: Scrapes content from URLs using browser operations.

Dependencies:
    - playwright: For browser operations.
    - asyncio: For asynchronous programming.

Example:
    >>> from src.scrapers import HTTPScraper, BrowserScraper

    # HTTP scraper usage
    >>> http_scraper = HTTPScraper()
    >>> result = await http_scraper.fetch(1, "https://example.com")
    >>> print(result)

    # Browser scraper usage
    >>> browser_scraper = BrowserScraper()
    >>> result = await browser_scraper.fetch(2, "https://example.com")
    >>> print(result)

    ScrapeResult(
        id='some-id',
        url='https://example.com',
        method='BROWSER',
        status=ScrapeStatus.SUCCESS,
        latency=0.5,
        content='Some content',
        content_length=12,
        error=None
    )
"""

from .http_scraper import HTTPScraper
from .browser_scraper import BrowserScraper

__all__ = ["HTTPScraper", "BrowserScraper"]
