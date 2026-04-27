# ./src/models/scrape/results.py
from .result import ScrapeResult
from .subtypes import K, Predicate, KeyFn, Grouped, TransformFn, Counts
from .deps import (
    List,
    pd,
    Optional,
    defaultdict,
    Iterable,
    Iterator,
)


class ScrapeResults:
    def __init__(self, results: Optional[Iterable[ScrapeResult]] = None):
        self._results: List[ScrapeResult] = list(results) if results else []

    # ===== CORE METHODS =====
    def add(self, result: ScrapeResult) -> None:
        self._results.append(result)

    def extend(self, results: Iterable[ScrapeResult]) -> None:
        self._results.extend(results)

    def to_list(self, include_content: bool = True) -> List[dict]:
        return [
            r.to_dict(include_content=include_content)
            for r in self._results
        ]

    def to_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.to_list())

    # ===== FACTORY METHODS =====
    @classmethod
    def from_iterable(cls, iterable: Iterable[dict]) -> "ScrapeResults":
        return cls(ScrapeResult(**item) for item in iterable)

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> "ScrapeResults":
        return cls(
            ScrapeResult(**row.to_dict())
            for _, row in df.iterrows()
        )

    # ===== MAGIC METHODS =====
    def __len__(self) -> int:
        return len(self._results)

    def __getitem__(self, index: int) -> ScrapeResult:
        return self._results[index]

    def __iter__(self) -> Iterator[ScrapeResult]:
        return iter(self._results)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(total={len(self)})"

    # ===== AGGREGATION METHODS =====
    def group(self, key_fn: KeyFn) -> Grouped:
        grouped: Grouped = defaultdict(ScrapeResults)
        for r in self._results:
            grouped[key_fn(r)].add(r)
        return dict(grouped)

    def count(self, key_fn: KeyFn) -> Counts:
        counts: Counts = defaultdict(int)
        for r in self._results:
            counts[key_fn(r)] += 1
        return dict(counts)

    def values(self, key_fn: KeyFn) -> List[K]:
        return [key_fn(r) for r in self._results]

    # ===== DOMAIN HELPERS =====
    def group_by_status(self) -> Grouped:
        return self.group(lambda r: r.status)

    def group_by_method(self) -> Grouped:
        return self.group(lambda r: r.method)

    def count_by_status(self) -> Counts:
        return self.count(lambda r: r.status)

    def count_by_method(self) -> Counts:
        return self.count(lambda r: r.method)

    # ===== FUNCTIONAL OPERATIONS =====
    def filter(self, predicate: Predicate) -> "ScrapeResults":
        return ScrapeResults(r for r in self._results if predicate(r))

    def transform(self, transform_fn: TransformFn) -> "ScrapeResults":
        return ScrapeResults(transform_fn(r) for r in self._results)

    def map(self, key_fn: KeyFn) -> List[K]:
        return self.values(key_fn)
