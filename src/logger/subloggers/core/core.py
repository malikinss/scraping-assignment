# ./src/logger/subloggers/core/core.py
from .deps import logging, os, Optional

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
GREEN = "\x1b[32m"
RESET = "\x1b[0m"


class Logger:
    def __init__(self, name: str = __name__, level: Optional[str] = None):
        self._logger = logging.getLogger(name)
        self._configure(level or LOG_LEVEL)

    # ===== CONFIG =====
    def _configure(self, level: str) -> None:
        self.set_level(level)
        self._logger.propagate = False

    # ===== HANDLERS =====
    def add_handler(self, handler: logging.Handler) -> None:
        self._logger.addHandler(handler)

    # ===== LOG LEVEL =====
    def set_level(self, level: str) -> None:
        self._logger.setLevel(level.upper())

    # ===== LOG METHODS =====
    def debug(self, msg: str, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs):
        self._logger.critical(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs):
        self._logger.exception(msg, *args, **kwargs)

    # ===== UTIL =====
    def separator(self, char: str = "=", length: int = 100):
        self.info(f"{GREEN}{char * length}{RESET}")

    def rows(self, rows: list[str], sep: str = " "):
        self.info(sep.join(rows))
