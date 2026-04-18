# ./src/services/result_manager/result_manager.py

"""
ResultManager Class
===================

This class is responsible for managing and persisting scraping results
through different output strategies.

This class is used by the PipelineOrchestrator to save the results of the
scraping process.

Imports:
    Dict: Dictionary type hint.
    AppLogger: Logger class for application-wide logging.
    ScrapeResults: Type hint for scraping results.
    CSVResultSaver: CSV saver class for saving results to a CSV file.
    BaseSaver: Base class for all saver classes.

Usage:
    >>> from src.services.result_manager import ResultManager
    >>> result_manager = ResultManager("results.csv")
    >>> result_manager.save_all(results)
"""

from .deps import Dict, AppLogger, ScrapeResults
from .savers import CSVResultSaver, BaseSaver as Saver

logger = AppLogger("ResultManager")

Statuses = Dict[str, bool]
Savers = Dict[str, Saver]


class ResultManager:
    """
    ResultManager class.

    This class is responsible for managing and persisting scraping results
    through different output strategies.

    """

    def __init__(self, file_path: str):
        """
        Initialize the ResultManager with the given file path.

        Args:
            file_path (str): The file path to save the results to.
        """
        self.savers: Savers = {
            "csv": CSVResultSaver(file_path),
        }

    # ===== REGISTRY =====
    def register_saver(self, name: str, saver: Saver) -> None:
        """
        Register a new saver with the given name.

        Args:
            name (str): The name of the saver.
            saver (Saver): The saver to register.
        """
        self.savers[name] = saver

    # ===== PUBLIC =====
    def save_all(self, results: ScrapeResults) -> Statuses:
        """
        Save the given results to all registered savers.

        Args:
            results (ScrapeResults): The results to save.

        Returns:
            Statuses: A dictionary of statuses for each saver.
        """
        if not results:
            logger.storage.no_results()
            return {}

        statuses: Statuses = {
            name: self._safe_save(name, saver, results)
            for name, saver in self.savers.items()
        }

        logger.storage.save_success(statuses)

        return statuses

    # ===== CORE =====
    def _safe_save(
        self, name: str, saver: Saver, results: ScrapeResults
    ) -> bool:
        """
        Save the given results to the given saver.

        Args:
            name (str): The name of the saver.
            saver (Saver): The saver to use.
            results (ScrapeResults): The results to save.

        Returns:
            bool: True if the results were saved successfully, False otherwise.
        """
        try:
            saver.save(results)
            return True
        except Exception as e:
            logger.storage.save_failure(name, e)
            return False
