# ./src/models/scrape/subtypes.py
from .result import ScrapeResult
from .status import ScrapeStatus
from .deps import (
    Callable,
    Dict,
    TypeVar,
    TYPE_CHECKING
)

if TYPE_CHECKING:
    from .results import ScrapeResults
K = TypeVar("K")
Predicate = Callable[[ScrapeResult], bool]
KeyFn = Callable[[ScrapeResult], K]
Grouped = Dict[K, "ScrapeResults"]
TransformFn = Callable[[ScrapeResult], ScrapeResult]
Counts = Dict[ScrapeStatus, int]
