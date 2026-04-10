# ./src/services/result_manager/savers/__init__.py

"""
CSV saver module for persisting scrape results.

This module exposes the `CSVResultSaver`, which provides functionality
for writing `ScrapeResult` objects into a CSV file.

Example:
    from src.services.result_manager.savers import CSVResultSaver

    saver = CSVResultSaver("results.csv")
    saver.save(results)
"""

from .csv_saver import CSVResultSaver

__all__ = ["CSVResultSaver"]
