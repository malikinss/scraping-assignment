# ./src/models/scrape_results.py

"""
Represents a collection of `ScrapeResult` objects.

This module provides the `ScrapeResults` class, which acts as a container
for managing multiple `ScrapeResult` instances. It enhances the basic
list structure with domain-specific functionality, including grouping,
filtering, transformation, and export capabilities.

Key Concepts:
    - ScrapeResults: A collection class that wraps a list of `ScrapeResult`
      objects, providing a rich API for working with scraping results.
    - Domain-Specific Collection: Extends standard list operations with
      methods tailored to scraping workflows, such as grouping by status,
      method, or custom keys.
    - Functional-Style Operations: Supports common functional programming
      patterns like map, filter, and reduce through method chaining.
    - Serialization: Includes built-in support for converting results to
      dictionaries and DataFrames for easy analysis and storage.

Usage:
    >>> results = ScrapeResults([
    ...     ScrapeResult(
    ...         id=1, url="https://example.com", status=ScrapeStatus.SUCCESS
    ...     ),
    ...     ScrapeResult(
    ...         id=2, url="https://example.org", status=ScrapeStatus.FAILURE
    ...     ),
    ... ]
    ... )
    >>> print(results)
    ScrapeResults(total=2)
    >>> results.group_by_status()
    {
        ScrapeStatus.SUCCESS: ScrapeResults(total=1),
        ScrapeStatus.FAILURE: ScrapeResults(total=1)
    }
    >>> results.to_df()

See Also:
    - :class:`~src.models.scrape_result.ScrapeResult` for individual
      result representation
    - :class:`~src.models.enums.ScrapeStatus` for status definitions
    - :class:`~src.models.enums.ScrapeMethod` for method definitions

Module Structure:
    - Imports: Core dependencies and domain enums
    - Type Aliases: Type hints for common patterns
    - Class Definition: `ScrapeResults` with comprehensive methods
    - Core Methods: Basic collection operations (add, extend, to_list)
    - Factory Methods: Creation from iterables and DataFrames
    - Magic Methods: Standard Python container protocols
    - Aggregation Methods: Grouping, counting, and value extraction
    - Domain Helpers: Status-based grouping and filtering
    - Transformation Methods: Mapping and filtering operations
    - Export Methods: DataFrame and CSV export

This module provides the foundation for working with collections of
scraping results, enabling efficient data management and analysis.
"""

from .scrape_result import ScrapeResult
from .common import Counts
from .deps import (
    List,
    pd,
    Optional,
    Callable,
    Dict,
    defaultdict,
    Iterable,
    Iterator,
    TypeVar,
)

K = TypeVar("K")
""" Type variable for keys in grouped results """

Predicate = Callable[[ScrapeResult], bool]
""" Predicate function for filtering results """

KeyFn = Callable[[ScrapeResult], K]
""" Function that extracts a key from a ScrapeResult """

Grouped = Dict[K, 'ScrapeResults']
""" Dictionary mapping keys to ScrapeResults collections """

TransformFn = Callable[[ScrapeResult], ScrapeResult]
""" Function that transforms a ScrapeResult """


class ScrapeResults:
    """
    Container for managing a collection of `ScrapeResult` objects.

    Provides functional-style operations, aggregation utilities, and
    conversion helpers for working with scraping results.

    This class acts as a domain-specific collection wrapper over a list
    of `ScrapeResult`, adding grouping, filtering, transformation, and
    export capabilities.
    """

    def __init__(self, results: Optional[Iterable[ScrapeResult]] = None):
        """
        Initialize the ScrapeResults container.

        Args:
            results (Optional[Iterable[ScrapeResult]]): Initial collection
                of scrape results. If None, an empty collection is created.
        """
        self._results: List[ScrapeResult] = list(results) if results else []

    # ===== CORE METHODS =====

    def add(self, result: ScrapeResult) -> None:
        """
        Add a single scrape result to the collection.

        Args:
            result (ScrapeResult): The scrape result to add.
        """
        self._results.append(result)

    def extend(self, results: Iterable[ScrapeResult]) -> None:
        """
        Add multiple scrape results to the collection.

        Args:
            results (Iterable[ScrapeResult]): Iterable of scrape results
                                              to add.
        """
        self._results.extend(results)

    def to_list(self, include_content: bool = True) -> List[dict]:
        """
        Convert all scrape results to a list of dictionaries.

        Args:
            include_content (bool): Whether to include full response content.
                Defaults to True.

        Returns:
            List[dict]: List of dictionary representations of scrape results.
        """
        return [
            r.to_dict(include_content=include_content)
            for r in self._results
        ]

    def to_df(self) -> pd.DataFrame:
        """
        Convert all scrape results to a pandas DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing all scrape results.
        """
        return pd.DataFrame(self.to_list())

    # ===== FACTORY METHODS =====

    @classmethod
    def from_iterable(cls, iterable: Iterable[dict]) -> "ScrapeResults":
        """
        Create ScrapeResults from an iterable of dictionaries.

        Args:
            iterable (Iterable[dict]): Iterable of dictionaries, where each
                dictionary represents a scrape result.

        Returns:
            ScrapeResults: New ScrapeResults instance containing the
                converted results.
        """
        return cls(ScrapeResult(**item) for item in iterable)

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> "ScrapeResults":
        """
        Create ScrapeResults from a pandas DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing scrape results.

        Returns:
            ScrapeResults: New ScrapeResults instance containing the
                converted results.
        """
        return cls(
            ScrapeResult(**row.to_dict())
            for _, row in df.iterrows()
        )

    # ===== MAGIC METHODS =====

    def __len__(self) -> int:
        """
        Return the number of scrape results in the collection.

        Returns:
            int: Number of scrape results.
        """
        return len(self._results)

    def __getitem__(self, index: int) -> ScrapeResult:
        """
        Get a scrape result by index.

        Args:
            index (int): Index of the scrape result to retrieve.

        Returns:
            ScrapeResult: Scrape result at the specified index.
        """
        return self._results[index]

    def __iter__(self) -> Iterator[ScrapeResult]:
        """
        Return an iterator over the scrape results.

        Returns:
            Iterator[ScrapeResult]: Iterator yielding scrape results.
        """
        return iter(self._results)

    def __repr__(self) -> str:
        """
        Return developer-friendly representation of the object.

        Returns:
            str: Same as __str__ for consistent debugging output.
        """
        return f"{self.__class__.__name__}(total={len(self)})"

    # ===== AGGREGATION METHODS =====

    def group(self, key_fn: KeyFn) -> Grouped:
        """
        Group scrape results by a key extracted from each result.

        Args:
            key_fn (KeyFn): Function that extracts a key from a ScrapeResult.

        Returns:
            Grouped: Dictionary mapping keys to ScrapeResults collections.
        """
        grouped: Grouped = defaultdict(ScrapeResults)
        for r in self._results:
            grouped[key_fn(r)].add(r)
        return dict(grouped)

    def count(self, key_fn: KeyFn) -> Counts:
        """
        Count occurrences of each key extracted from the scrape results.

        Args:
            key_fn (KeyFn): Function that extracts a key from a ScrapeResult.

        Returns:
            Counts: Dictionary mapping keys to their occurrence counts.
        """
        counts: Counts = defaultdict(int)
        for r in self._results:
            counts[key_fn(r)] += 1
        return dict(counts)

    def values(self, key_fn: KeyFn) -> List[K]:
        """
        Extract values from all scrape results using a key function.

        Args:
            key_fn (KeyFn): Function that extracts a value from a ScrapeResult.

        Returns:
            List[K]: List of extracted values.
        """
        return [key_fn(r) for r in self._results]

    # ===== DOMAIN HELPERS =====

    def group_by_status(self) -> Grouped:
        """
        Group scrape results by HTTP status code.

        Returns:
            Grouped: Dictionary mapping status codes to ScrapeResults
                     collections.
        """
        return self.group(lambda r: r.status)

    def group_by_method(self) -> Grouped:
        """
        Group scrape results by HTTP method.

        Returns:
            Grouped: Dictionary mapping HTTP methods to ScrapeResults
                     collections.
        """
        return self.group(lambda r: r.method)

    def count_by_status(self) -> Counts:
        """
        Count occurrences of each HTTP status code.

        Returns:
            Counts: Dictionary mapping status codes to their occurrence counts.
        """
        return self.count(lambda r: r.status)

    def count_by_method(self) -> Counts:
        """
        Count occurrences of each HTTP method.

        Returns:
            Counts: Dictionary mapping HTTP methods to their occurrence counts.
        """
        return self.count(lambda r: r.method)

    # ===== FUNCTIONAL OPERATIONS =====

    def filter(self, predicate: Predicate) -> "ScrapeResults":
        """
        Filter scrape results based on a predicate.

        Args:
            predicate (Predicate): Function that returns True for results to
                                   keep.

        Returns:
            ScrapeResults: New ScrapeResults instance with filtered results.
        """
        return self.from_iterable(r for r in self._results if predicate(r))

    def transform(self, transform_fn: TransformFn) -> "ScrapeResults":
        """
        Transform each scrape result using a transformation function.

        Args:
            transform_fn (TransformFn): Function that transforms a
                                        ScrapeResult.

        Returns:
            ScrapeResults: New ScrapeResults instance with transformed
                           results.
        """
        return self.from_iterable(transform_fn(r) for r in self._results)

    def map(self, key_fn: KeyFn) -> List[K]:
        """
        Map each scrape result to a value using a key function.

        Args:
            key_fn (KeyFn): Function that extracts a value from a ScrapeResult.

        Returns:
            List[K]: List of extracted values.
        """
        return self.values(key_fn)
