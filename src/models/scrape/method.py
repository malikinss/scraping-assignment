# ./src/models/scrape/method.py
from .deps import Enum, Dict


class ScrapeMethod(str, Enum):
    HTTPX = "httpx"              # Using httpx client
    PLAYWRIGHT = "playwright"    # Using Playwright browser automation

    @classmethod
    def _alias_map(cls) -> Dict[str, "ScrapeMethod"]:
        if not hasattr(cls, "_cached_alias_map"):
            cls._cached_alias_map = {
                "http": cls.HTTPX,
                "httpx": cls.HTTPX,
                "requests": cls.HTTPX,
                "browser": cls.PLAYWRIGHT,
                "playwright": cls.PLAYWRIGHT,
                "chromium": cls.PLAYWRIGHT,
            }
        return cls._cached_alias_map

    @classmethod
    def default(cls) -> "ScrapeMethod":
        return cls.HTTPX

    @classmethod
    def from_name(cls, name: str) -> "ScrapeMethod":
        if not name:
            return cls.default()
        normalized = name.strip().lower()
        return cls._alias_map().get(normalized, cls.default())
