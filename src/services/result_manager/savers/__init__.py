# ./src/services/result_manager/savers/__init__.py

"""
Savers Package
==============

This package contains the savers for the result_manager package.
It is used by the result_manager package to save the results of the scraping
process.

Imports:
    - CSVResultSaver: CSV saver for persisting scrape results.

Example:
    >>> from src.services.result_manager.savers import CSVResultSaver
    >>> saver = CSVResultSaver("results.csv")
    >>> saver.save(results)
"""

from .csv_saver import CSVResultSaver

__all__ = ["CSVResultSaver"]
