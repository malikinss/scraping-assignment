# ./src/services/metrics/aggregator.py

from .deps import (
    List,
    Dict,
    defaultdict,
    Logger,
    ScrapeResult,
    ScrapeMethod,
    ScrapeStatus,
)


logger = Logger(__name__)


class MetricsAggregator:
    """
    Aggregates scraping results into grouped metrics.
    """

    def group_by_method(
        self, results: List[ScrapeResult]
    ) -> Dict[ScrapeMethod, List[ScrapeResult]]:
        """
        Groups ScrapeResult objects by ScrapeMethod.

        Args:
            results (List[ScrapeResult]): List of scrape results.

        Returns:
            Dict[ScrapeMethod, List[ScrapeResult]]: Dictionary mapping each
                                                    ScrapeMethod to a list of
                                                    results.
        """
        logger.debug("Grouping results by method")
        grouped: Dict[ScrapeMethod, List[ScrapeResult]] = defaultdict(list)
        for r in results:
            grouped[r.method].append(r)
        logger.debug("Results grouped by method")
        return grouped

    def group_by_status(
        self, results: List[ScrapeResult]
    ) -> Dict[ScrapeStatus, int]:
        """
        Counts the number of ScrapeResult objects for each ScrapeStatus.

        Args:
            results (List[ScrapeResult]): List of scrape results.

        Returns:
            Dict[ScrapeStatus, int]: Dictionary mapping each ScrapeStatus to
                                     the count of results.
        """
        logger.debug("Grouping results by status")
        counts: Dict[ScrapeStatus, int] = defaultdict(int)
        for r in results:
            counts[r.status] += 1
        logger.debug("Results grouped by status")
        return dict(counts)
