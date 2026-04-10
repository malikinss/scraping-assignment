# ./src/services/result_manager/__init__.py

"""
Result Manager service package.

This package provides a high-level interface for managing and persisting
scraping results through different output strategies (CSV, JSON, error logs).

The main entry point is `ResultManager`, which orchestrates multiple
savers and coordinates saving results in different formats.
"""

from .result_manager import ResultManager

__all__ = ["ResultManager"]
