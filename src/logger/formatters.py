# ./src/logger/formatters.py

"""
Custom logging formatters with colorized output.

This module provides a `ColoredFormatter` that enhances log readability
by applying ANSI color codes to different parts of log messages,
including timestamps, module names, log levels, and message content.

It also supports:
    - Highlighting request IDs
    - Emphasizing scraper-related keywords (e.g., HTTPX, PLAYWRIGHT)
"""

from .deps import logging, re


class ColoredFormatter(logging.Formatter):
    """
    Logging formatter with ANSI color support.

    Enhances log output readability in terminal environments by applying
    colors to structured log components such as:
        - Timestamp
        - Logger name (module)
        - Log level
        - Message content (IDs and keywords)

    Attributes:
        LEVEL_COLORS (dict): Mapping of log levels to ANSI color codes.
        COLORS (dict): Mapping of UI elements to ANSI color codes.
        NAME_WIDTH (int): Fixed width for logger name display.
        LEVEL_WIDTH (int): Fixed width for log level display.
        TIME_FORMAT (str): Format string for timestamps.
    """

    RESET = "\x1b[0m"

    # ===== LEVEL COLORS =====
    LEVEL_COLORS = {
        "DEBUG": "\x1b[35m",
        "INFO": "\x1b[34m",
        "WARNING": "\x1b[33m",
        "ERROR": "\x1b[91m",
        "CRITICAL": "\x1b[31m",
    }

    # ===== UI COLORS =====
    COLORS = {
        "MODULE": "\x1b[38;5;208m",
        "TIME": "\x1b[90m",
        "BRACKETS": "\x1b[32m",
        "ID": "\x1b[38;5;201m",
        "PLAYWRIGHT": "\x1b[38;5;118m",
        "BROWSER": "\x1b[38;5;118m",
        "HTTPX": "\x1b[38;5;229m",
        "NUMBER": "\x1b[94m",
    }

    NAME_WIDTH = 25
    LEVEL_WIDTH = 10
    TIME_FORMAT = "%H:%M:%S"

    ID_PATTERN = re.compile(r"(\[)(ID:)(\s*)(\d+)(\])")
    KEYWORDS_PATTERN = re.compile(r"\b(PLAYWRIGHT|BROWSER|HTTPX|HTTP)\b")

    # ===== MAIN ENTRY =====

    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record into a colored string.

        Applies message-level highlighting (IDs and keywords) and then
        constructs the final formatted output.

        Args:
            record (logging.LogRecord): Log record to format.

        Returns:
            str: Fully formatted and colorized log message.
        """
        message = record.getMessage()

        message = self._highlight_ids(message)
        message = self._highlight_keywords(message)

        return self._format_shell(record, message)

    # ===== SHELL FORMAT =====

    def _format_shell(self, record: logging.LogRecord, message: str) -> str:
        """
        Construct the final log output string.

        Combines colored timestamp, module name, and log level with the
        processed message.

        Args:
            record (logging.LogRecord): Log record metadata.
            message (str): Preprocessed message string.

        Returns:
            str: Fully formatted log line.
        """
        time = self._colored_time(record)
        name = self._colored_name(record)
        level = self._colored_level(record)

        return f"[{time}][{name}][{level}] {message}"

    # ===== TIME =====

    def _colored_time(self, record: logging.LogRecord) -> str:
        """
        Format and colorize the timestamp.

        Args:
            record (logging.LogRecord): Log record metadata.

        Returns:
            str: Colorized timestamp string.
        """
        time_str = self.formatTime(record, self.TIME_FORMAT)
        return f"{self.COLORS['TIME']}{time_str}{self.RESET}"

    # ===== MODULE =====

    def _colored_name(self, record: logging.LogRecord) -> str:
        """
        Format and colorize the logger name (module).

        Args:
            record (logging.LogRecord): Log record metadata.

        Returns:
            str: Colorized and padded module name.
        """
        name = f"{record.name[:self.NAME_WIDTH]:^{self.NAME_WIDTH}}"
        return f"{self.COLORS['MODULE']}{name}{self.RESET}"

    # ===== LEVEL =====

    def _colored_level(self, record: logging.LogRecord) -> str:
        """
        Format and colorize the log level.

        Args:
            record (logging.LogRecord): Log record metadata.

        Returns:
            str: Colorized and padded log level.
        """
        level_color = self.LEVEL_COLORS.get(record.levelname, self.RESET)
        level = f"{record.levelname:^{self.LEVEL_WIDTH}}"
        return f"{level_color}{level}{self.RESET}"

    # ===== HIGHLIGHTING =====

    def _highlight_ids(self, message: str) -> str:
        """
        Highlight request IDs in the message.

        Matches patterns like "[ID: 123]" and applies color formatting
        to individual components.

        Args:
            message (str): Raw log message.

        Returns:
            str: Message with highlighted IDs.
        """
        def highlight_id(match):
            """
            Helper function to apply colors to matched ID components.

            Args:
                match (re.Match): Regex match object.

            Returns:
                str: Colorized ID components.
            """
            return (
                f"{self.COLORS['BRACKETS']}{match.group(1)}"
                f"{self.COLORS['ID']}{match.group(2)}"
                f"{self.COLORS['BRACKETS']}{match.group(3)}"
                f"{self.COLORS['NUMBER']}{match.group(4)}"
                f"{self.COLORS['BRACKETS']}{match.group(5)}{self.RESET}"
            )

        return self.ID_PATTERN.sub(highlight_id, message)

    def _highlight_keywords(self, message: str) -> str:
        """
        Highlight specific keywords in the message.

        Matches keywords like "PLAYWRIGHT", "BROWSER", "HTTPX" and applies
        distinct colors to them.

        Args:
            message (str): Raw log message.

        Returns:
            str: Message with highlighted keywords.
        """
        def highlight(match):
            """
            Helper function to apply colors to matched keywords.

            Args:
                match (re.Match): Regex match object.

            Returns:
                str: Colorized keyword.
            """
            color = self.COLORS.get(match.group(1), self.RESET)
            return f"{color}{match.group(1)}{self.RESET}"

        return self.KEYWORDS_PATTERN.sub(highlight, message)
