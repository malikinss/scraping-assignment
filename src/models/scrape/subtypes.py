# ./src/models/scrape/subtypes.py

from .result import ScrapeResult

from .deps import (
    Callable,
    Dict,
    TypeVar,
)

K = TypeVar("K")
Predicate = Callable[[ScrapeResult], bool]
KeyFn = Callable[[ScrapeResult], K]
Grouped = Dict[K, 'ScrapeResults']
TransformFn = Callable[[ScrapeResult], ScrapeResult]
