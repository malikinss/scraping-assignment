# ./src/services/result_manager/__init__.py

"""
Result Manager Service Package
============================

This package provides an interface for managing and persisting scraping results
through different output strategies.

This package is used by the PipelineOrchestrator to save the results of the
scraping process.

Imports:
    ResultManager: Main entry point for managing and persisting scraping
                   results.

Usage:
    >>> from src.services.result_manager import ResultManager
    >>> result_manager = ResultManager()
    >>> result_manager.save(results)
"""

from .result_manager import ResultManager

__all__ = ["ResultManager"]
