# src/services/result_manager/result_manager.py

from typing import List
from src.utils.logger import Logger
from src.models.scrape_result import ScrapeResult
from .savers import CSVResultSaver, ErrorLogger, JSONResultSaver

logger = Logger(__name__)


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
        """
        logger.debug(
            f"Initializing ResultManager: "
            f"csv={csv_path}, "
            f"json={json_path}, "
            f"error_log={error_log_path}"
        )
        self.csv_saver: CSVResultSaver = CSVResultSaver(csv_path)
        self.json_saver: JSONResultSaver = JSONResultSaver(json_path)
        self.error_logger: ErrorLogger = ErrorLogger(error_log_path)

    def save_all(self, results: List[ScrapeResult]) -> None:
        """
        Save results using all configured saver implementations.

        Each saver is executed independently. Failures in one saver do not
        interrupt the execution of others.

        Args:
            results (List[ScrapeResult]): A list of `ScrapeResult` instances
                                          to be saved.

        Raises:
            None: Exceptions are caught and logged internally.
        """
        logger.debug(f"Saving {len(results)} results")

        self._safe_save("CSV", self.csv_saver.save, results)
        self._safe_save("JSON", self.json_saver.save, results)
        self._safe_save("Error Log", self.error_logger.save, results)

        logger.debug("All save operations completed")

    def _safe_save(self, name, save_func, results):
        """
        Execute a save operation safely with logging.

        Wraps a saver call in a try-except block to ensure that failures
        are logged but do not propagate further.

        Args:
            name (str): Human-readable name of the saver (for logging).
            save_func (Callable[[List[ScrapeResult]], None]): The save
                                                              function to
                                                              execute.
            results (List[ScrapeResult]): The results to pass to the saver.

        Raises:
            None: Exceptions are caught and logged internally.
        """
        try:
            logger.debug(f"Saving using {name} saver")
            save_func(results)
            logger.debug(f"Successfully saved using {name} saver")
        except Exception as e:
            logger.error(f"Failed to save using {name} saver: {e}")
