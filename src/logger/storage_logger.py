# ./src/logger/storage_logger.py

"""
Storage Logger Module
=====================

This module provides a structured logger for storage-related operations,
including file saving, loading, and summary reporting. It wraps the core
Logger class and uses LogParts for consistent log formatting.

Key Features:
    - Structured logging for file I/O operations
    - Helper methods for save/load operations and summary reporting
    - Uses LogParts for consistent log formatting

Classes:
    StorageLogger: Logger wrapper for storage operations

Dependencies:
    - src.logger.core.Logger
    - src.logger.deps.Optional
    - src.logger.log_parts.LogParts

Usage:
    >>> from src.logger import Logger, StorageLogger
    >>> logger = Logger()
    >>> storage_logger = StorageLogger(logger)
    >>> storage_logger.no_results("CSV", "data.csv")
    >>> storage_logger.file_save_success("CSV", "data.csv", 100)
    >>> storage_logger.save_success({"csv": True, "json": False})
    >>> storage_logger.save_failure("CSV", ValueError("File not found"))
    >>> storage_logger.load_failure("File not found", "data.csv")
    >>> storage_logger.load_success("data.csv")
    >>> storage_logger.load_summary(100, 90, 5, 5)

Example:
    >>> logger = Logger()
    >>> storage_logger = StorageLogger(logger)
    >>> storage_logger.no_results("CSV", "data.csv")
    CSV save skipped: No results to save [path=data.csv]
    >>> storage_logger.file_save_success("CSV", "data.csv", 100)
    CSV saved: [path=data.csv] [count=100]
    >>> storage_logger.save_success({"csv": True, "json": False})
    Save completed: [success=1/2] [details={'csv': True, 'json': False}]
    >>> storage_logger.save_failure("CSV", ValueError("File not found"))
    Save failed: [target=CSV] [error=File not found]
    >>> storage_logger.load_failure("File not found", "data.csv")
    Load failed: File not found [path=data.csv]
    >>> storage_logger.load_success("data.csv")
    Load success: [path=data.csv]
    >>> storage_logger.load_summary(100, 90, 5, 5)
    Load summary: [total=100] [valid=90] [duplicates=5] [invalid=5]

"""

from .core import Logger
from .log_parts import LogParts


class StorageLogger:
    """
    Logger wrapper for storage-related operations.

    This class provides structured logging utilities for file I/O operations
    such as saving results, loading data, and reporting summary statistics.
    It formats log messages using `LogParts` for consistency across the
    application.

    Attributes:
        log (Logger): Core logger instance used for output.
    """

    def __init__(self, logger: Logger):
        """
        Initialize the StorageLogger.

        Args:
            logger (Logger): Core logger instance used for emitting logs.
        """
        self.log: Logger = logger

    def no_results(self, file_type: str = "File", file_path: str = "") -> None:
        """
        Log a message indicating that a save operation was skipped due to
        отсутствию данных.

        Args:
            file_type (str): Type of file (e.g., CSV, JSON). Defaults to "File"
            file_path (str): Path to the target file.
        """
        rows = [
            f"{file_type} save skipped:",
            "No results to save",
            LogParts.path(file_path)
        ]
        self.log.rows(rows)

    def file_save_success(
        self,
        file_type: str,
        file_path: str,
        count: int
    ) -> None:
        """
        Log successful file save operation.

        Args:
            file_type (str): Type of file (e.g., CSV, JSON).
            file_path (str): Path where file was saved.
            count (int): Number of saved records.
        """
        rows = [
            f"{file_type} saved:",
            LogParts.path(file_path),
            LogParts.count(count)
        ]
        self.log.rows(rows)

    def save_success(self, statuses: dict) -> None:
        """
        Log summary of multiple save operations.

        Args:
            statuses (dict): Dictionary mapping saver names to success flags.
        """
        success = sum(statuses.values())
        rows = [
            "Save completed:",
            LogParts.success(success, len(statuses)),
            LogParts.details(statuses)
        ]
        self.log.rows(rows)

    def save_failure(self, name: str, error: Exception) -> None:
        """
        Log a failure that occurred during a save operation.

        Args:
            name (str): Name of the storage target (e.g., CSV, JSON).
            error (Exception): Exception that was raised.
        """
        rows = [
            "Save failed:",
            LogParts.target(name),
            LogParts.error(error)
        ]
        self.log.error(" ".join(rows))

    def load_failure(self, message: str, file_path: str) -> None:
        """
        Log a failure that occurred during a load operation.

        Args:
            message (str): Error message describing the failure.
            file_path (str): Path of the file being loaded.
        """
        rows = [
            "Load failed:",
            message,
            LogParts.path(file_path)
        ]
        self.log.error(" ".join(rows))

    def load_success(self, file_path: str) -> None:
        """
        Log successful file load operation.

        Args:
            file_path (str): Path of the successfully loaded file.
        """
        rows = [
            "Load success:",
            LogParts.path(file_path)
        ]
        self.log.rows(rows)

    def load_summary(
        self,
        total: int,
        valid: int,
        duplicates: int,
        invalid: int
    ) -> None:
        """
        Log summary statistics of a file loading process.

        Args:
            total (int): Total number of records processed.
            valid (int): Number of valid records.
            duplicates (int): Number of duplicate records removed.
            invalid (int): Number of invalid records.
        """
        rows = [
            "Load summary:",
            LogParts.total(total),
            LogParts.valid(valid),
            LogParts.duplicates_removed(duplicates),
            LogParts.invalid(invalid)
        ]
        self.log.rows(rows)
