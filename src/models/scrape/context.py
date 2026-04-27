# ./src/models/scrape/context.py
from .method import ScrapeMethod
from .deps import dataclass, Optional, replace, URL


@dataclass(frozen=True, slots=True)
class ScraperContext:
    id: int
    url: URL
    method: ScrapeMethod
    timeout: float

    attempt: Optional[int] = None
    retries: Optional[int] = None
    error: Optional[str] = None

    def with_updates(self, **kwargs) -> "ScraperContext":
        return replace(self, **kwargs)
