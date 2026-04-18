# ./src/services/result_manager/savers/__init__.py

"""
Savers Package
==============

This package contains the savers for the result_manager package.
It is used by the result_manager package to save the results of the scraping
process.

Imports:
    - BaseSaver: Base saver for persisting scrape results.
    - CSVResultSaver: CSV saver for persisting scrape results.

Example:
    >>> from src.services.result_manager.savers import (
    ...     BaseSaver,
    ...     CSVResultSaver,
    ... )
    >>> base_saver = BaseSaver()
    >>> csv_saver = CSVResultSaver("results.csv")
    >>> base_saver.save(results)
    >>> csv_saver.save(results)
"""

from .base import BaseSaver
from .csv_saver import CSVResultSaver

__all__ = ["BaseSaver", "CSVResultSaver"]
