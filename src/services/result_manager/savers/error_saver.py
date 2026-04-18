# ./src/services/result_manager/savers/error_saver.py

"""
Error Saver
============

This class is responsible for saving errors to a file.

Usage:
    >>> from src.services.result_manager.savers import ErrorSaver
    >>> saver = ErrorSaver("errors.txt")
    >>> saver.save(results)

Example:
    >>> from src.services.result_manager.savers import ErrorSaver
    >>> saver = ErrorSaver("errors.txt")
    >>> saver.save(results)
"""

from .base import BaseSaver
from .deps import (
    Any,
    List,
    Path,
    AppLogger,
    ScrapeResult,
    ScrapeResults,
    IO
)

logger = AppLogger("ErrorSaver")


class ErrorSaver(BaseSaver):
    """
    This class is responsible for saving errors to a file.
    """

    def __init__(self, file_path: str):
        """
        Initialize the ErrorSaver.

        Args:
            file_path (str): Path to the error file.
        """
        self.file_path: Path = Path(file_path)

    # ===== PUBLIC =====

    def save(self, results: ScrapeResults) -> None:
        """
        Save the errors to a file.

        Args:
            results (ScrapeResults): Results of the scraping process.
        """
        if not results:
            logger.storage.no_results("Error", str(self.file_path))
            return

        errors: ScrapeResults = results.filter(lambda r: r.error is not None)
        if not errors:
            logger.storage.no_results("Error", str(self.file_path))
            return

        self.write_file(
            self.file_path,
            lambda f: self._writer(f, errors),
            description="error file"
        )

        logger.storage.file_save_success(
            "Error",
            str(self.file_path),
            len(errors)
        )

    # ===== CORE =====

    def _writer(self, file: IO[str], errors: ScrapeResults) -> None:
        """
        Write the errors to a file.

        Args:
            file (IO[str]): File object to write the errors to.
            errors (ScrapeResults): Results of the scraping process.
        """
        file.writelines(self._format_error(r) for r in errors)

    # ===== INTERNAL HELPERS =====

    def _safe_str(self, value: Any) -> str:
        """
        Convert a value to a string, replacing None with "-".

        Args:
            value (Any): Value to convert.

        Returns:
            str: String representation of the value.
        """
        return str(value) if value is not None else "-"

    def _get_fields(self, result: ScrapeResult) -> List[str]:
        """
        Get the fields of a result.

        Args:
            result (ScrapeResult): Result to get fields from.

        Returns:
            List[str]: List of fields.
        """
        return [
            result.id,
            result.url,
            result.method,
            result.status,
            result.error,
        ]

    def _format_error(self, result: ScrapeResult) -> str:
        """
        Format an error result as a string.

        Args:
            result (ScrapeResult): Result to format.

        Returns:
            str: Formatted error string.
        """
        fields = self._get_fields(result)
        return " | ".join(self._safe_str(v) for v in fields) + "\n"
