# ./src/services/result_manager/__init__.py

"""
Result management module for persisting scrape results.

This module provides the `ResultManager` class, which coordinates
saving `ScrapeResult` data across multiple formats including CSV, JSON,
and error logs.

Example:
    from .result_manager import ResultManager

    manager = ResultManager(
        csv_path="results.csv",
        json_path="results.json",
        error_log_path="errors.log"
    )
    manager.save_all(results)
"""

from .result_manager import ResultManager

__all__ = ["ResultManager"]
