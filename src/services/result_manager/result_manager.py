# ./src/services/result_manager/result_manager.py

from .deps import Dict, Logger, ScrapeResults
from .savers import CSVResultSaver

logger = Logger("ResultManager")

Statuses = Dict[str, bool]


class ResultManager:
    """
    High-level service for managing and coordinating result persistence.

    The ResultManager acts as an orchestrator for multiple saver strategies
    (e.g., CSV, JSON, logs). It allows registering different savers and
    executing them in a unified way while collecting execution statuses.

    Attributes:
        savers (Dict[str, Any]): Registered saver implementations indexed
                                 by name.
    """

    def __init__(self, file_path: str):
        """
        Initialize ResultManager with a default CSV saver.

        Args:
            file_path (str): Base file path used for default CSV saver.
        """
        self.savers = {
            "csv": CSVResultSaver(file_path),
        }

    def register_saver(self, name: str, saver) -> None:
        """
        Register a new saver implementation.

        Allows extending output formats dynamically at runtime.

        Args:
            name (str): Unique identifier for the saver.
            saver (Any): Saver instance implementing `save(results)` method.
        """
        self.savers[name] = saver

    def save_all(self, results: ScrapeResults) -> Statuses:
        """
        Execute all registered savers on the provided results.

        Each saver is executed safely, and failures do not interrupt
        other saver executions. Returns a status map indicating success
        or failure per saver.

        Args:
            results (ScrapeResults): Collection of scrape results.

        Returns:
            Statuses: Dictionary mapping saver name to success status.
        """
        if not results:
            logger.debug("Save skipped: no results")
            return {}

        statuses: Statuses = {
            name: self._safe_save(name, saver, results)
            for name, saver in self.savers.items()
        }

        success_count = sum(statuses.values())

        logger.info(
            f"Save completed: "
            f"success={success_count}/{len(statuses)} "
            f"details={statuses}"
        )

        return statuses

    def _safe_save(self, name: str, saver, results: ScrapeResults) -> bool:
        """
        Safely execute a saver and capture failures.

        Args:
            name (str): Saver identifier.
            saver (Any): Saver instance.
            results (ScrapeResults): Data to persist.

        Returns:
            bool: True if save succeeded, False otherwise.
        """
        try:
            saver.save(results)
            return True
        except Exception as e:
            logger.error(f"Save failed: target={name} error={e}")
            return False
