# ./src/logger.py

from .deps import os, logging, re


class ColoredFormatter(logging.Formatter):
    """
    Logging formatter with ANSI color support.
    """

    RESET = "\x1b[0m"

    # basic level colors
    LEVEL_COLORS = {
        "DEBUG": "\x1b[35m",
        "INFO": "\x1b[34m",
        "WARNING": "\x1b[33m",
        "ERROR": "\x1b[91m",
        "CRITICAL": "\x1b[31m",
    }

    # custom colors
    COLORS = {
        "MODULE": "\x1b[38;5;208m",      # orange
        "TIME": "\x1b[90m",               # gray
        "BRACKETS": "\x1b[32m",           # green
        "ID": "\x1b[38;5;201m",           # pink
        "PLAYWRIGHT": "\x1b[38;5;118m",   # lime
        "BROWSER": "\x1b[38;5;118m",      # lime
        "HTTPX": "\x1b[38;5;229m",        # light yellow
        "NUMBER": "\x1b[94m",             # light blue (for IDs)
    }

    NAME_WIDTH = 25
    LEVEL_WIDTH = 10

    # regex patterns for dynamic highlighting
    ID_PATTERN = re.compile(r"(\[)(ID:)(\s*)(\d+)(\])")
    KEYWORDS_PATTERN = re.compile(r"\b(PLAYWRIGHT|BROWSER|HTTPX)\b")

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a log record with ANSI colors.

        Args:
            record: The log record to format.

        Returns:
            The formatted log record.
        """
        level_color = self.LEVEL_COLORS.get(record.levelname, self.RESET)

        name = f"{record.name[:self.NAME_WIDTH]:^{self.NAME_WIDTH}}"
        level = f"{record.levelname:^{self.LEVEL_WIDTH}}"
        time = (
            f"{self.COLORS['TIME']}"
            f"{self.formatTime(record, '%H:%M:%S')}"
            f"{self.RESET}"
        )

        name_colored = f"{self.COLORS['MODULE']}{name}{self.RESET}"
        level_colored = f"{level_color}{level}{self.RESET}"

        message = record.getMessage()

        # highlight [ID: number]
        def highlight_id(match):
            return (
                f"{self.COLORS['BRACKETS']}{match.group(1)}"  # [
                f"{self.COLORS['ID']}{match.group(2)}"        # ID:
                f"{self.COLORS['BRACKETS']}{match.group(3)}"  # space
                f"{self.COLORS['NUMBER']}{match.group(4)}"    # number
                f"{self.COLORS['BRACKETS']}{match.group(5)}{self.RESET}"  # ]
            )
        message = self.ID_PATTERN.sub(highlight_id, message)

        # highlight keywords PLAYWRIGHT/BROWSER/HTTPX
        def highlight_keywords(match):
            color = self.COLORS.get(match.group(1), self.RESET)
            return f"{color}{match.group(1)}{self.RESET}"
        message = self.KEYWORDS_PATTERN.sub(highlight_keywords, message)

        return f"[{time}][{name_colored}][{level_colored}] {message}"


class Logger:
    """
    Custom logger wrapper with colored output and ergonomic API.
    """

    __slots__ = ("_logger",)

    def __init__(self, name: str = __name__, level: str | None = None):
        self._logger = logging.getLogger(name)

        log_level = (level or os.getenv("LOG_LEVEL", "INFO")).upper()
        self._logger.setLevel(log_level)
        self._logger.propagate = False

        if not self._logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(ColoredFormatter())
            self._logger.addHandler(handler)

    # --- core logging (lazy formatting!) ---

    def debug(self, msg: str, *args, **kwargs):
        """
        Logs a debug message.

        Args:
            msg: The message to log.
            *args: Additional arguments to format the message.
            **kwargs: Additional keyword arguments to format the message.
        """
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        """
        Logs an info message.

        Args:
            msg: The message to log.
            *args: Additional arguments to format the message.
            **kwargs: Additional keyword arguments to format the message.
        """
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        """
        Logs a warning message.

        Args:
            msg: The message to log.
            *args: Additional arguments to format the message.
            **kwargs: Additional keyword arguments to format the message.
        """
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        """
        Logs an error message.

        Args:
            msg: The message to log.
            *args: Additional arguments to format the message.
            **kwargs: Additional keyword arguments to format the message.
        """
        self._logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs):
        """
        Logs a critical message.

        Args:
            msg: The message to log.
            *args: Additional arguments to format the message.
            **kwargs: Additional keyword arguments to format the message.
        """
        self._logger.critical(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs):
        """
        Logs an exception message.

        Args:
            msg: The message to log.
            *args: Additional arguments to format the message.
            **kwargs: Additional keyword arguments to format the message.
        """
        self._logger.exception(msg, *args, **kwargs)

    # --- utils ---

    def separator(self, char: str = "=", length: int = 100):
        """
        Logs a visual separator without breaking formatter.

        Args:
            char: The character to use for the separator.
            length: The length of the separator.
        """
        self._logger.info("\x1b[32m%s\x1b[0m", char * length)

    def set_level(self, level: str):
        """
        Dynamically change log level.

        Args:
            level: The new log level.
        """
        self._logger.setLevel(level.upper())

    def add_file_handler(self, filepath: str):
        """
        Adds file logging (without colors).

        Args:
            filepath: The path to the file to log to.
        """
        handler = logging.FileHandler(filepath)
        handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
                "%Y-%m-%d %H:%M:%S",
            )
        )
        self._logger.addHandler(handler)
