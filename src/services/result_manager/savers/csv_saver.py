# ./src/services/result_manager/savers/csv_saver.py

"""
CSV Result Saver
==============

This class is responsible for saving results to a CSV file.

Usage:
    >>> from src.services.result_manager.savers import CSVResultSaver
    >>> saver = CSVResultSaver("results.csv")
    >>> saver.save(results)

Example:
    >>> from src.services.result_manager.savers import CSVResultSaver
    >>> saver = CSVResultSaver("results.csv")
    >>> saver.save(results)
"""

from .deps import (
    Any,
    csv,
    List,
    Path,
    AppLogger,
    ScrapeResults
)
from .base import BaseSaver

logger = AppLogger("CSVSaver")


class CSVResultSaver(BaseSaver):
    """
    This class is responsible for saving results to a CSV file.
    """

    FIELDNAMES: List[str] = [
        "id",
        "url",
        "method",
        "status",
        "latency",
        "content_length",
        "error",
    ]

    def __init__(self, file_path: str, append: bool = False):
        """
        Initialize the CSVResultSaver.

        Args:
            file_path (str): Path to the CSV file.
            append (bool): Whether to append to the CSV file.
        """
        self.file_path: Path = Path(file_path)
        self.append: bool = append

        self._need_header = (
            not self.append
            or not self.file_path.exists()
            or self.file_path.stat().st_size == 0
        )

    # ===== PUBLIC =====

    def save(self, results: ScrapeResults) -> None:
        """
        Save the results to a CSV file.

        Args:
            results (ScrapeResults): Results of the scraping process.
        """
        if not results:
            logger.storage.no_results("CSV", str(self.file_path))
            return

        self.write_file(
            self.file_path,
            lambda f: self._write_csv(f, results),
            self._get_mode(),
            description="CSV file"
        )

        logger.storage.file_save_success(
            "CSV",
            str(self.file_path),
            len(results)
        )

    # ===== CORE WRITER =====

    def _write_csv(self, f, results: ScrapeResults) -> None:
        """
        Write the results to a CSV file.

        Args:
            f: File object to write the results to.
            results (ScrapeResults): Results of the scraping process.
        """
        writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)

        self._handle_header(writer)

        for r in results:
            row = r.to_dict()
            writer.writerow(self._filter_row(row))

    # ===== INTERNAL HELPERS =====

    def _get_mode(self) -> str:
        """
        Get the mode to open the file in.

        Returns:
            str: Mode to open the file in.
        """
        return "a" if self.append else "w"

    def _filter_row(self, row: dict[str, Any]) -> dict[str, Any]:
        """
        Filter the row to include only the fieldnames.

        Args:
            row (dict[str, Any]): Row to filter.

        Returns:
            dict[str, Any]: Filtered row.
        """
        return {k: row.get(k, None) for k in self.FIELDNAMES}

    def _handle_header(self, writer: csv.DictWriter) -> None:
        """
        Handle the header.

        Args:
            writer (csv.DictWriter): CSV writer.
        """
        if self._need_header:
            writer.writeheader()
