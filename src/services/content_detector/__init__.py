# ./src/services/content_detector/__init__.py

"""
This module serves as the entry point for the ContentDetector service.

It exposes the detector object, which is a singleton instance of
ContentDetector, providing easy access to content detection functionality
throughout the application.

Exposes:
    - detector: The singleton instance of ContentDetector.

Usage:
    >>> from src.services.content_detector import detector
    >>> status = detector.detect(content)
    >>> print(status)

Example:
    >>> from src.services.content_detector import detector
    >>> content = "403 Forbidden"
    >>> status = detector.detect(content)
    >>> print(status)
    ScrapeStatus.BLOCKED
"""

from .content_detector import detector

__all__ = ["detector"]
