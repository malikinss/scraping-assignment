# ./src/services/result_manager/savers/__init__.py

"""
Saver implementations for persisting scrape results.

This module provides a unified interface and multiple concrete saver
implementations for storing `ScrapeResult` data in different formats.

Available savers:
    - BaseSaver: Abstract base class defining the saver interface.
    - CSVResultSaver: Saves results to a CSV file.
    - JSONResultSaver: Saves results to a JSON file.
    - ErrorLogger: Logs failed results to a plain text file.

These classes are exposed for convenient import via the package namespace.

Example:
    from .savers import CSVResultSaver

    saver = CSVResultSaver("results.csv")
    saver.save(results)
"""

from .base import BaseSaver
from .csv_saver import CSVResultSaver
from .error_saver import ErrorLogger
from .json_saver import JSONResultSaver

__all__ = ["BaseSaver", "CSVResultSaver", "ErrorLogger", "JSONResultSaver"]
