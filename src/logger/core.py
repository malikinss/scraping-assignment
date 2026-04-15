# ./src/logger/core.py

"""
Core logging abstraction built on top of Python's standard logging.

This module provides a lightweight wrapper around the built-in
`logging` module, simplifying configuration and usage while exposing
common logging methods.

It standardizes:
    - Log level configuration
    - Handler management
    - Common logging interface
    - Utility helpers for formatted output
"""

from .deps import logging, os, Optional

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
GREEN = "\x1b[32m"
RESET = "\x1b[0m"


class Logger:
    """
    Lightweight wrapper over Python's standard logger.

    Provides a simplified interface for logging with preconfigured
    log levels, handlers, and utility methods.

    Attributes:
        _logger (logging.Logger): Underlying Python logger instance.
    """

    def __init__(self, name: str = __name__, level: Optional[str] = None):
        """
        Initialize Logger with an optional name and log level.

        Args:
            name (str, optional): Logger name. Defaults to __name__.
            level (Optional[str], optional): Log level (e.g., "INFO", "DEBUG").
                                             Defaults to LOG_LEVEL environment
                                             variable.
        """
        self._logger = logging.getLogger(name)
        self._configure(level or LOG_LEVEL)

    # ===== CONFIG =====

    def _configure(self, level: str) -> None:
        """Configure logger settings.

        Sets log level and disables propagation to avoid duplicate logs.

        Args:
            level (str): Logging level (e.g., "INFO", "DEBUG").
        """
        self.set_level(level)
        self._logger.propagate = False

    # ===== HANDLERS =====

    def add_handler(self, handler: logging.Handler) -> None:
        """
        Attach a handler to the logger.

        Args:
            handler (logging.Handler): Logging handler instance.
        """
        self._logger.addHandler(handler)

    # ===== LOG LEVEL =====

    def set_level(self, level: str) -> None:
        """
        Set logging level.

        Args:
            level (str): Logging level name.
        """
        self._logger.setLevel(level.upper())

    # ===== LOG METHODS =====

    def debug(self, msg: str, *args, **kwargs):
        """
        Log debug message.

        Args:
            msg (str): Message to log.
            *args: Positional arguments for message formatting.
            **kwargs: Keyword arguments for message formatting.
        """
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        """
        Log info message.

        Args:
            msg (str): Message to log.
            *args: Positional arguments for message formatting.
            **kwargs: Keyword arguments for message formatting.
        """
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        """
        Log warning message.

        Args:
            msg (str): Message to log.
            *args: Positional arguments for message formatting.
            **kwargs: Keyword arguments for message formatting.
        """
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        """
        Log error message.

        Args:
            msg (str): Message to log.
            *args: Positional arguments for message formatting.
            **kwargs: Keyword arguments for message formatting.
        """
        self._logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs):
        """
        Log critical message.

        Args:
            msg (str): Message to log.
            *args: Positional arguments for message formatting.
            **kwargs: Keyword arguments for message formatting.
        """
        self._logger.critical(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs):
        """
        Log exception message.

        Args:
            msg (str): Message to log.
            *args: Positional arguments for message formatting.
            **kwargs: Keyword arguments for message formatting.
        """
        self._logger.exception(msg, *args, **kwargs)

    # ===== UTIL =====

    def separator(self, char: str = "=", length: int = 100):
        """
        Log a visual separator line.

        Args:
            char (str, optional): Character used for the separator.
                Defaults to "=".
            length (int, optional): Length of the separator line.
                Defaults to 100.
        """
        self.info(f"{GREEN}{char * length}{RESET}")

    def rows(self, rows: list[str], sep: str = " "):
        """
        Log multiple rows with space separation.

        Args:
            rows (list[str]): List of strings to log.
            sep (str, optional): Separator between rows. Defaults to " ".
        """
        self.info(sep.join(rows))
