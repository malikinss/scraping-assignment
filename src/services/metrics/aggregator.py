# ./src/services/metrics/aggregator.py

from .deps import (
    List,
    Dict,
    Callable,
    defaultdict,
    TypeVar,
    Logger,
    ScrapeResult,
    ScrapeMethod,
    ScrapeStatus,
)


logger = Logger("MetricsAggregator")
K = TypeVar("K")


class MetricsAggregator:
    """
    Aggregates scraping results into grouped metrics.
    """
    @staticmethod
    def _group(
        results: List[ScrapeResult],
        key_fn: Callable[[ScrapeResult], K],
    ) -> Dict[K, List[ScrapeResult]]:
        """
        Groups ScrapeResult objects by a given key function.

        Args:
            results (List[ScrapeResult]): List of scrape results.
            key_fn (Callable[[ScrapeResult], K]): Function to extract the key
            from a ScrapeResult.

        Returns:
            Dict[K, List[ScrapeResult]]: Dictionary mapping each key to a list
            of ScrapeResult objects.
        Example:
            >>> results = [
            ...     ScrapeResult(
            ...         url="https://example.com",
            ...         method=ScrapeMethod.HTTPX,
            ...         status=ScrapeStatus.SUCCESS,
            ...         latency=1.0,
            ...         length=100
            ...     ),
            ...     ScrapeResult(
            ...         url="https://example.com",
            ...         method=ScrapeMethod.BROWSER,
            ...         status=ScrapeStatus.SUCCESS,
            ...         latency=2.0,
            ...         length=200
            ...     ),
            ... ]
            >>> MetricsAggregator._group(results, lambda r: r.method)
            {ScrapeMethod.HTTPX: [
                ScrapeResult(
                    url='https://example.com',
                    method=ScrapeMethod.HTTPX,
                    status=ScrapeStatus.SUCCESS,
                    latency=1.0,
                    length=100
                )
            ],
            ScrapeMethod.BROWSER: [
                ScrapeResult(
                    url='https://example.com',
                    method=ScrapeMethod.BROWSER,
                    status=ScrapeStatus.SUCCESS,
                    latency=2.0,
                    length=200
                )
            ]}
        """
        grouped: Dict[K, List[ScrapeResult]] = defaultdict(list)
        for r in results:
            grouped[key_fn(r)].append(r)
        return dict(grouped)

    @staticmethod
    def _count(
        results: List[ScrapeResult],
        key_fn: Callable[[ScrapeResult], K]
    ) -> Dict[K, int]:
        """
        Counts the number of ScrapeResult objects for each key.

        Args:
            results (List[ScrapeResult]): List of scrape results.
            key_fn (Callable[[ScrapeResult], K]): Function to extract the key
            from a ScrapeResult.

        Returns:
            Dict[K, int]: Dictionary mapping each key to the count of results.
        Example:
            >>> results = [
            ...     ScrapeResult(
            ...         url="https://example.com",
            ...         method=ScrapeMethod.HTTPX,
            ...         status=ScrapeStatus.SUCCESS,
            ...         latency=1.0,
            ...         length=100
            ...     ),
            ...     ScrapeResult(
            ...         url="https://example.com",
            ...         method=ScrapeMethod.BROWSER,
            ...         status=ScrapeStatus.SUCCESS,
            ...         latency=2.0,
            ...         length=200
            ...     ),
            ... ]
            >>> MetricsAggregator._count(results, lambda r: r.method)
            {ScrapeMethod.HTTPX: 1,
            ScrapeMethod.BROWSER: 1}
        """
        counts: Dict[K, int] = defaultdict(int)
        for r in results:
            counts[key_fn(r)] += 1
        return dict(counts)

    @staticmethod
    def group_by_method(
        results: List[ScrapeResult]
    ) -> Dict[ScrapeMethod, List[ScrapeResult]]:
        """
        Groups ScrapeResult objects by ScrapeMethod.

        Args:
            results (List[ScrapeResult]): List of scrape results.

        Returns:
            Dict[ScrapeMethod, List[ScrapeResult]]: Dictionary mapping each
                                                    ScrapeMethod to a list of
                                                    results.
        Example:
            >>> results = [
            ...     ScrapeResult(
            ...         url="https://example.com",
            ...         method=ScrapeMethod.HTTPX,
            ...         status=ScrapeStatus.SUCCESS,
            ...         latency=1.0,
            ...         length=100
            ...     ),
            ...     ScrapeResult(
            ...         url="https://example.com",
            ...         method=ScrapeMethod.BROWSER,
            ...         status=ScrapeStatus.SUCCESS,
            ...         latency=2.0,
            ...         length=200
            ...     ),
            ... ]
            >>> MetricsAggregator.group_by_method(results)
            {ScrapeMethod.HTTPX: [
                ScrapeResult(
                    url='https://example.com',
                    method=ScrapeMethod.HTTPX,
                    status=ScrapeStatus.SUCCESS,
                    latency=1.0,
                    length=100
                )
            ],
            ScrapeMethod.BROWSER: [
                ScrapeResult(
                    url='https://example.com',
                    method=ScrapeMethod.BROWSER,
                    status=ScrapeStatus.SUCCESS,
                    latency=2.0,
                    length=200
                )
            ]}
        """
        if not results:
            return {}
        return MetricsAggregator._group(results, lambda r: r.method)

    @staticmethod
    def group_by_status(
        results: List[ScrapeResult]
    ) -> Dict[ScrapeStatus, int]:
        """
        Counts the number of ScrapeResult objects for each ScrapeStatus.

        Args:
            results (List[ScrapeResult]): List of scrape results.

        Returns:
            Dict[ScrapeStatus, int]: Dictionary mapping each ScrapeStatus to
                                     the count of results.
        Example:
            >>> results = [
            ...     ScrapeResult(
            ...         url="https://example.com",
            ...         method=ScrapeMethod.HTTPX,
            ...         status=ScrapeStatus.SUCCESS,
            ...         latency=1.0,
            ...         length=100
            ...     ),
            ...     ScrapeResult(
            ...         url="https://example.com",
            ...         method=ScrapeMethod.BROWSER,
            ...         status=ScrapeStatus.SUCCESS,
            ...         latency=2.0,
            ...         length=200
            ...     ),
            ... ]
            >>> MetricsAggregator.group_by_status(results)
            {ScrapeStatus.SUCCESS: 2}
        """
        if not results:
            return {}
        return MetricsAggregator._count(results, lambda r: r.status)
