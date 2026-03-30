# ./src/services/content_detector/__init__.py

"""
Content detection module.

Provides functionality to detect content types such as EMPTY, CAPTCHA,
BLOCKED, or SUCCESS from text content.
"""

from .content_detector import ContentDetector, detector

__all__ = ["ContentDetector", "detector"]
