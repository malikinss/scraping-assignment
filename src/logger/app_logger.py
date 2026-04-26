# ./src/logger/app_logger.py
from .deps import logging
from .subloggers import (
    Logger,
    ScraperLogger,
    PipelineLogger,
    MetricsLogger,
    StorageLogger,
    ColoredFormatter
)


class AppLogger:
    def __init__(self, name: str = "app"):
        self.core = self._create_logger(name)
        # lazy-style composition (lightweight, but explicit)
        self._scraper = None
        self._pipeline = None
        self._metrics = None
        self._storage = None

    # ===== CORE =====
    def _create_logger(self, name: str) -> Logger:
        logger = Logger(name)
        handler = logging.StreamHandler()
        handler.setFormatter(ColoredFormatter())
        logger.add_handler(handler)
        return logger

    # ===== DOMAIN LOGGERS (lazy) =====
    @property
    def scraper(self) -> ScraperLogger:
        return self._get_logger("_scraper", ScraperLogger)

    @property
    def pipeline(self) -> PipelineLogger:
        return self._get_logger("_pipeline", PipelineLogger)

    @property
    def metrics(self) -> MetricsLogger:
        return self._get_logger("_metrics", MetricsLogger)

    @property
    def storage(self) -> StorageLogger:
        return self._get_logger("_storage", StorageLogger)

    # ===== HELPERS =====
    def _get_logger(self, attr_name: str, logger_type):
        logger = getattr(self, attr_name, None)

        if logger is None:
            logger = logger_type(self.core)
            setattr(self, attr_name, logger)

        return logger
