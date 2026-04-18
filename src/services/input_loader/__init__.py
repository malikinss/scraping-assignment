# ./src/services/input_loader/__init__.py

"""
Input Loader Service Package
============================

This package provides functionality for loading URLs from a file.

Public API:
    - URLInputLoader: Class for loading and validating URLs from a file.

Internal Components:
    - input_loader.py: Main implementation of URL loading pipeline.
    - deps.py: Dependencies and type aliases.

Usage:
    >>> from src.services.input_loader import URLInputLoader
    >>> loader = URLInputLoader("data/raw/urls.txt")
    >>> urls = loader.run()
    >>> print(urls)
"""

from .input_loader import URLInputLoader

__all__ = ["URLInputLoader"]
