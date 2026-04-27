# ./src/models/scrape/status.py
from .deps import Enum, Dict


class ScrapeStatus(str, Enum):
    SUCCESS = "success"      # Successfully scraped
    FAILED = "failed"        # Generic failure
    TIMEOUT = "timeout"      # Request timed out
    CAPTCHA = "captcha"      # CAPTCHA encountered
    BLOCKED = "blocked"      # Access blocked
    EMPTY = "empty"          # Empty response
    PDF = "pdf"              # PDF content detected

    @classmethod
    def _alias_map(cls) -> Dict[str, "ScrapeStatus"]:
        if not hasattr(cls, "_cached_alias_map"):
            cls._cached_alias_map = {
                "success": cls.SUCCESS,
                "failed": cls.FAILED,
                "timeout": cls.TIMEOUT,
                "captcha": cls.CAPTCHA,
                "blocked": cls.BLOCKED,
                "empty": cls.EMPTY,
                "pdf": cls.PDF
            }
        return cls._cached_alias_map

    @classmethod
    def default(cls) -> "ScrapeStatus":
        return cls.FAILED

    # ===== CLASSIFIERS =====
    @classmethod
    def success_statuses(cls) -> set["ScrapeStatus"]:
        return {cls.SUCCESS, *cls.content_statuses()}

    @classmethod
    def non_success_statuses(cls) -> set["ScrapeStatus"]:
        return {cls.TIMEOUT, cls.BLOCKED, cls.FAILED}

    @classmethod
    def content_statuses(cls) -> set["ScrapeStatus"]:
        return {cls.PDF}

    # ===== INSTANCE PROPERTIES =====
    @property
    def is_success(self) -> bool:
        return self in self.success_statuses()

    @property
    def is_failure(self) -> bool:
        return self in self.non_success_statuses()

    @property
    def is_content(self) -> bool:
        return self in self.content_statuses()

    # ===== FAST LOOKUP MAP =====
    @classmethod
    def from_name(cls, name: str) -> "ScrapeStatus":
        if not name:
            return cls.default()
        normalized = name.strip().lower()
        return cls._alias_map().get(normalized, cls.default())
