# ./src/services/result_manager/result_manager.py

from .deps import Dict, Callable, List, Logger, ScrapeResult
from .savers import CSVResultSaver, ErrorLogger, JSONResultSaver

logger = Logger("ResultManager")


class ResultManager:
    """
    Coordinator for saving scrape results using multiple saver strategies.

    This class aggregates different saver implementations (CSV, JSON,
    error log) and ensures that results are persisted across all formats.

    Each save operation is executed safely to prevent one failure from
    affecting others.
    """

    def __init__(self, csv_path: str, json_path: str, error_log_path: str):
        """
        Initialize the result manager with saver configurations.

        Args:
            csv_path (str): Path to the CSV file for storing results.
            json_path (str): Path to the JSON file for storing results.
            error_log_path (str): Path to the file for logging failed results.

        Raises:
            None: Exceptions are caught and logged internally.

        Returns:
            None: Returns nothing.

        Examples:
            >>> result_manager = ResultManager(
            ...     csv_path="results.csv",
            ...     json_path="results.json",
            ...     error_log_path="errors.log"
            ... )
            >>> result_manager.save_all([
            ...     ScrapeResult(
            ...         id="1",
            ...         url="https://example.com",
            ...         title="Example Domain",
            ...         status="success",
            ...         content="<p>Example Domain</p>",
            ...         timestamp="2022-01-01T00:00:00Z"
            ...     )
            ... ])
        """
        self.savers: Dict[str, Callable[[List[ScrapeResult]], None]] = {
            "csv": CSVResultSaver(csv_path).save,
            "json": JSONResultSaver(json_path).save,
            "error_log": ErrorLogger(error_log_path).save,
        }

    def save_all(
        self,
        results: List[ScrapeResult],
        only_csv: bool = False
    ) -> Dict[str, bool]:
        """
        Save results using all configured saver implementations.

        If only_csv is True, only save to CSV file.

        Each saver is executed independently. Failures in one saver do not
        interrupt the execution of others.

        Args:
            results (List[ScrapeResult]): A list of `ScrapeResult` instances
                                          to be saved.
            only_csv (bool): If True, only save to CSV file.

        Raises:
            None: Exceptions are caught and logged internally.

        Returns:
            Dict[str, bool]: A dictionary mapping saver names to boolean
                             success indicators.

        Examples:
            >>> result_manager = ResultManager(
            ...     csv_path="results.csv",
            ...     json_path="results.json",
            ...     error_log_path="errors.log"
            ... )
            >>> statuses = result_manager.save_all([
            ...     ScrapeResult(
            ...         id="1",
            ...         url="https://example.com",
            ...         title="Example Domain",
            ...         status="success",
            ...         content="<p>Example Domain</p>",
            ...         timestamp="2022-01-01T00:00:00Z"
            ...     )
            ... ])
            >>> statuses
            {'csv': True, 'json': True, 'error_log': True}
        """
        if not results:
            logger.debug("Save skipped: no results")
            return {}

        statuses: Dict[str, bool] = {}

        for name, save_func in self.savers.items():
            if only_csv and name != "csv":
                continue
            statuses[name] = self._safe_save(name, save_func, results)

        success_count: int = sum(statuses.values())

        logger.info(
            f"Save completed: "
            f"success={success_count}/{len(statuses)} "
            f"details={statuses}"
        )

        return statuses

    def _safe_save(
        self,
        name: str,
        save_func,
        results: List[ScrapeResult]
    ) -> bool:
        """
        Executes a save operation safely with logging.

        Args:
            name (str): Human-readable name of the saver (for logging).
            save_func (Callable[[List[ScrapeResult]], None]): The save
                                                              function to
                                                              execute.
            results (List[ScrapeResult]): The results to pass to the saver.

        Raises:
            None: Exceptions are caught and logged internally.

        Returns:
            bool: True if the save operation was successful, False otherwise.

        Examples:
            >>> result_manager = ResultManager(
            ...     csv_path="results.csv",
            ...     json_path="results.json",
            ...     error_log_path="errors.log"
            ... )
            >>> result_manager._safe_save(
            ...     "CSV",
            ...     result_manager.csv_saver.save,
            ...     [
            ...         ScrapeResult(
            ...             id="1",
            ...             url="https://example.com",
            ...             title="Example Domain",
            ...             status="success",
            ...             content="<p>Example Domain</p>",
            ...             timestamp="2022-01-01T00:00:00Z"
            ...         )
            ...     ]
            ... )
        """
        try:
            save_func(results)
            return True
        except Exception as e:
            logger.error(
                f"Save failed: target={name} error={e}"
            )
            return False
