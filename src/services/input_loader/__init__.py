# ./src/services/input_loader/__init__.py

"""
URL input loading module.

This module provides the `URLInputLoader` class, which handles
loading, cleaning, and validating URLs from a CSV file.

Example:
    from .input_loader import URLInputLoader

    loader = URLInputLoader("urls.csv")
    urls = loader.load().clean().validate().get_urls()
"""

from .input_loader import URLInputLoader

__all__ = ["URLInputLoader"]
