# ./src/logger/app_logger.py

"""
Application Logger Module
=========================

This module provides a central application logger with domain-specific
extensions for different components of the scraping application. It uses
lazy initialization for sub-loggers to keep the interface lightweight
while providing structured logging for various domains.

Key Features:
    - Unified logging interface with domain-specific extensions
    - Lazy initialization of sub-loggers to avoid unnecessary object creation
    - Support for multiple domain-specific loggers
        (scraper, pipeline, metrics, storage)
    - Colored output formatting for better readability

Classes:
    AppLogger: Central application logger with domain-specific extensions

Dependencies:
    - src.logger.core.Logger
    - src.logger.deps.logging
    - src.logger.scraper_logger.ScraperLogger
    - src.logger.pipeline_logger.PipelineLogger
    - src.logger.metrics_logger.MetricsLogger
    - src.logger.storage_logger.StorageLogger
    - src.logger.formatters.ColoredFormatter

Usage:
    >>> from src.logger import AppLogger
    >>> logger = AppLogger("my_app")
    >>> logger.core.info("Application started")
    >>> logger.scraper.request("GET", "http://example.com", 200)
    >>> logger.pipeline.start_pipeline()
    >>> logger.metrics.report_metrics({"count": 100})
    >>> logger.storage.file_save_success("CSV", "data.csv", 100)

Example:
    >>> logger = AppLogger("scraper_app")
    >>> logger.core.info("Application started")
    Application started
    >>> logger.scraper.request("GET", "http://example.com", 200)
    [HTTPX] GET http://example.com → 200 OK
    >>> logger.pipeline.start_pipeline()
    Pipeline started
    >>> logger.metrics.report_metrics({"count": 100})
    Metrics: {'count': 100}
    >>> logger.storage.file_save_success("CSV", "data.csv", 100)
    CSV saved: [path=data.csv] [count=100]

"""

from .deps import logging
from .core import Logger
from .scraper_logger import ScraperLogger
from .pipeline_logger import PipelineLogger
from .metrics_logger import MetricsLogger
from .storage_logger import StorageLogger
from .formatters import ColoredFormatter


class AppLogger:
    """
    Central application logger with domain-specific extensions.

    Provides a unified logging interface with support for multiple
    domain-specific loggers (scraper, pipeline, metrics, storage).

    Uses lazy initialization for sub-loggers to avoid unnecessary
    object creation and keep the interface lightweight.

    Attributes:
        core (Logger): Underlying core logger instance.
    """

    def __init__(self, name: str = "app"):
        """
        Initialize AppLogger with a named core logger.

        Args:
            name (str, optional): Logger name. Defaults to "app".
        """
        self.core = self._create_logger(name)

        # lazy-style composition (lightweight, but explicit)
        self._scraper = None
        self._pipeline = None
        self._metrics = None
        self._storage = None

    # ===== CORE =====
    def _create_logger(self, name: str) -> Logger:
        """
        Create and configure the core logger.

        Attaches a stream handler with colored formatting.

        Args:
            name (str): Logger name.

        Returns:
            Logger: Configured logger instance.
        """
        logger = Logger(name)
        handler = logging.StreamHandler()
        handler.setFormatter(ColoredFormatter())
        logger.add_handler(handler)
        return logger

    # ===== DOMAIN LOGGERS (lazy) =====

    @property
    def scraper(self) -> ScraperLogger:
        """
        Access scraper-specific logger.

        Returns:
            ScraperLogger: Logger for scraping-related events.
        """
        return self._get_logger("_scraper", ScraperLogger)

    @property
    def pipeline(self) -> PipelineLogger:
        """
        Access pipeline-specific logger.

        Returns:
            PipelineLogger: Logger for pipeline-related events.
        """
        return self._get_logger("_pipeline", PipelineLogger)

    @property
    def metrics(self) -> MetricsLogger:
        """
        Access metrics-specific logger.

        Returns:
            MetricsLogger: Logger for metrics-related events.
        """
        return self._get_logger("_metrics", MetricsLogger)

    @property
    def storage(self) -> StorageLogger:
        """
        Access storage-specific logger.

        Returns:
            StorageLogger: Logger for storage-related events.
        """
        return self._get_logger("_storage", StorageLogger)

    def _get_logger(self, attr_name: str, logger_type):
        """
        Lazily initialize and return a domain-specific logger.

        Creates the logger only once and caches it for future use.

        Args:
            attr_name (str): Attribute name used for caching.
            logger_type (Type): Logger class to instantiate.

        Returns:
            Any: Instance of the requested logger type.
        """
        logger = getattr(self, attr_name, None)

        if logger is None:
            logger = logger_type(self.core)
            setattr(self, attr_name, logger)

        return logger
