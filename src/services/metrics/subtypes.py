# ./src/services/metrics/subtypes.py

from .deps import Callable, ScrapeResult, TypeVar, Dict, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .models import MetricsSummary

K = TypeVar("K")
Distribution = dict[K, int]
KeyFn = Callable[[ScrapeResult], K]
FormatterFn = Callable[[K], str]
GroupedMetrics = dict[str, "MetricsSummary"]
NonZeroMetrics = dict[str, int]

Rates = Dict[str, float]

MetricFieldSpec = Tuple[Tuple[str, str, str], ...]
