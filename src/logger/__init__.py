# ./src/logger/__init__.py

"""
Application logging package.

This package provides the main logging interface used across the
application. It exposes `AppLogger`, a structured logging utility
designed for consistent and contextual logging.

Example:
    from src.logger import AppLogger

    logger = AppLogger("MyService")
    logger.info("Service started")
"""

from .app_logger import AppLogger

__all__ = ["AppLogger"]
