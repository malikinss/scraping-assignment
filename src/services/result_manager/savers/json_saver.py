# ./src/services/result_manager/savers/json_saver.py

"""
JSON Result Saver
================

This class is responsible for saving results to a JSON file.

Usage:
    >>> from src.services.result_manager.savers import JSONResultSaver
    >>> saver = JSONResultSaver("results.json")
    >>> saver.save(results)

Example:
    >>> from src.services.result_manager.savers import JSONResultSaver
    >>> saver = JSONResultSaver("results.json")
    >>> saver.save(results)
"""

from .base import BaseSaver
from .deps import json, Path, AppLogger, ScrapeResults, IO

logger = AppLogger("JSONSaver")


class JSONResultSaver(BaseSaver):
    """
    This class is responsible for saving results to a JSON file.
    """

    def __init__(self, file_path: str, pretty: bool = True):
        """
        Initialize the JSONResultSaver.

        Args:
            file_path (str): Path to the JSON file.
            pretty (bool): Whether to pretty-print the JSON file.
        """
        self.file_path: Path = Path(file_path)
        self.pretty: bool = pretty

    # ===== PUBLIC =====

    def save(self, results: ScrapeResults) -> None:
        """
        Save the results to a JSON file.

        Args:
            results (ScrapeResults): Results of the scraping process.
        """
        if not results:
            logger.storage.no_results("JSON", str(self.file_path))
            return

        self.write_file(
            self.file_path,
            lambda f: self._writer(f, results),
            description="JSON file"
        )

        logger.storage.file_save_success(
            "JSON",
            str(self.file_path),
            len(results)
        )

    def _writer(self, file: IO[str], results: ScrapeResults) -> None:
        """
        Write the results to a JSON file.

        Args:
            file (IO[str]): File object to write the results to.
            results (ScrapeResults): Results of the scraping process.
        """
        json.dump(
            results.to_list(),
            file,
            ensure_ascii=False,
            indent=(4 if self.pretty else None)
        )
