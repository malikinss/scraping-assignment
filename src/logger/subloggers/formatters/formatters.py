# ./src/logger/subloggers/formatters/formatters.py
from .deps import re, Formatter, LogRecord


class ColoredFormatter(Formatter):
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

    ID_PATTERN = re.compile(r"(\[)(ID:)(\d+)(\])")
    KEYWORDS_PATTERN = re.compile(r"\b(PLAYWRIGHT|BROWSER|HTTPX|HTTP)\b")

    # ===== MAIN ENTRY =====
    def format(self, record: LogRecord) -> str:
        message = record.getMessage()
        message = self._highlight_ids(message)
        message = self._highlight_keywords(message)
        return self._format_shell(record, message)

    # ===== SHELL FORMAT =====
    def _format_shell(self, record: LogRecord, message: str) -> str:
        time = self._colored_time(record)
        name = self._colored_name(record)
        level = self._colored_level(record)
        return f"[{time}][{name}][{level}] {message}"

    # ===== TIME =====
    def _colored_time(self, record: LogRecord) -> str:
        time_str = self.formatTime(record, self.TIME_FORMAT)
        return f"{self.COLORS['TIME']}{time_str}{self.RESET}"

    # ===== MODULE =====
    def _colored_name(self, record: LogRecord) -> str:
        name = f"{record.name[:self.NAME_WIDTH]:^{self.NAME_WIDTH}}"
        return f"{self.COLORS['MODULE']}{name}{self.RESET}"

    # ===== LEVEL =====
    def _colored_level(self, record: LogRecord) -> str:
        level_color = self.LEVEL_COLORS.get(record.levelname, self.RESET)
        level = f"{record.levelname:^{self.LEVEL_WIDTH}}"
        return f"{level_color}{level}{self.RESET}"

    # ===== HIGHLIGHTING =====
    def _highlight_ids(self, message: str) -> str:
        def highlight_id(match):
            return (
                f"{self.COLORS['BRACKETS']}{match.group(1)}"
                f"{self.COLORS['ID']}{match.group(2)}"
                f"{self.COLORS['NUMBER']}{match.group(3)}"
                f"{self.COLORS['BRACKETS']}{match.group(4)}{self.RESET}"
            )
        return self.ID_PATTERN.sub(highlight_id, message)

    def _highlight_keywords(self, message: str) -> str:
        def highlight(match):
            key = match.group(1)
            color = self.COLORS.get(key, self.RESET)
            return f"{color}{key}{self.RESET}"
        return self.KEYWORDS_PATTERN.sub(highlight, message)
