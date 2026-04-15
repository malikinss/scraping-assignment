# ./src/logger/metrics_logger.py

"""
Metrics Logger Module
=====================

This module provides a structured metrics logger that wraps the core Logger
class to handle metrics-related logging operations.

Key Features:
    - Structured logging for metrics and distributions
    - Helper methods for common metrics logging scenarios
    - Uses LogParts for consistent log formatting

Classes:
    MetricsLogger: Logger wrapper for structured metrics reporting

Dependencies:
    - src.logger.core.Logger
    - src.logger.log_parts.LogParts

Usage:
    >>> from src.logger import Logger, MetricsLogger
    >>> logger = Logger()
    >>> metrics_logger = MetricsLogger(logger)
    >>> metrics_logger.log_metrics("test", {"count": 10})
    >>> metrics_logger.log_distribution("test", {"1-10": 5, "11-20": 5})
    >>> metrics_logger.log_no_metrics("test")
    >>> metrics_logger.log_metrics_exception("test", Exception("test"))

Example:
    >>> logger = Logger()
    >>> metrics_logger = MetricsLogger(logger)
    >>> metrics_logger.log_metrics("test", {"count": 10})
    [METRICS:] test
    {'count': 10}
    >>> metrics_logger.log_distribution("test", {"1-10": 5, "11-20": 5})
    [DISTRIBUTION:] test
    {'1-10': 5, '11-20': 5}
    >>> metrics_logger.log_no_metrics("test")
    [WARNING] [METRICS:] test
    >>> metrics_logger.log_metrics_exception("test", Exception("test"))
    [ERROR] Failed metrics for test: test

"""

from .core import Logger
from .log_parts import LogParts as LP


class MetricsLogger:
    """
    Logger wrapper for structured metrics reporting.

    This class provides helper methods for logging different types of
    metrics-related information such as aggregated metrics, distributions,
    and error states. It formats logs using `LogParts` utilities to ensure
    consistency across the application.

    Attributes:
        log (Logger): Underlying logger instance used for output.
    """

    def __init__(self, logger: Logger):
        """
        Initialize the MetricsLogger.

        Args:
            logger (Logger): Core logger instance used for emitting logs.
        """
        self.log: Logger = logger

    def log_metrics(self, name: str, metrics: dict):
        """
        Log aggregated metrics for a given component or stage.

        Args:
            name (str): Name of the component or context.
            metrics (dict): Dictionary containing aggregated metrics.
        """
        rows = [
            LP.title(name, 'METRICS:'),
            str(metrics)
        ]
        self.log.rows(rows)

    def log_distribution(self, name: str, distribution: dict):
        """
        Log distribution data (e.g., status breakdowns).

        Args:
            name (str): Name of the component or context.
            distribution (dict): Dictionary representing value distribution.
        """
        rows = [
            LP.title(name, 'DISTRIBUTION:'),
            str(distribution)
        ]
        self.log.rows(rows)

    def log_no_metrics(self, name: str):
        """
        Log that no metrics were available for a component.

        Args:
            name (str): Name of the component or context.
        """
        self.log.warning(f"{LP.title(name, 'NO METRICS')}")

    def log_metrics_exception(self, name: str, e: Exception):
        """
        Log an exception that occurred during metrics collection.

        Args:
            name (str): Name of the component or context.
            e (Exception): Exception that occurred.
        """
        self.log.exception(f"Failed metrics for {name}: {e}")
