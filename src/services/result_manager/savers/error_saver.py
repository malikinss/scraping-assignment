# ./src/services/result_manager/savers/error_saver.py

from .base import BaseSaver
from .deps import (
    Any,
    List,
    Path,
    Logger,
    ScrapeResult,
    ScrapeResults
)

logger = Logger("ErrorSaver")


class ErrorLogger(BaseSaver):
    """
    Saver implementation for logging failed scrape results to a file.

    Filters `ScrapeResults` to include only entries with errors and writes
    them in a human-readable, line-based format.

    Each line contains key fields separated by a delimiter, making the file
    easy to inspect and parse.
    """

    def __init__(self, file_path: str):
        """
        Initialize the error logger.

        Args:
            file_path (str): Path to the file where errors will be stored.
        """
        self.file_path: Path = Path(file_path)

    def save(self, results: ScrapeResults) -> None:
        """
        Save only failed results (with errors) to a file.

        Skips execution if:
            - No results are provided
            - No errors are found in results

        Args:
            results (ScrapeResults): Collection of scrape results.

        Raises:
            Exception: Propagates exceptions raised during file writing.
        """
        if not results:
            logger.debug("Error save skipped: no results")
            return

        total = len(results)
        errors: ScrapeResults = results.filter(lambda r: r.error is not None)
        error_count = len(errors)

        if error_count == 0:
            logger.debug(f"Error save skipped: no errors total={total}")
            return

        def writer(f):
            """
            Write formatted error lines to file.

            Args:
                f (IO[Any]): File-like object opened for writing.
            """
            f.writelines(self._format_error(r) for r in errors)

        self.write_file(self.file_path, writer, description="error file")

        logger.info(
            f"Errors saved: "
            f"path={self.file_path} "
            f"errors={error_count} "
            f"total={total}"
        )

    # ===== INTERNAL HELPERS =====

    def _safe_str(self, value: Any) -> str:
        """
        Safely convert a value to string.

        Args:
            value (Any): Value to convert.

        Returns:
            str: String representation or "-" if value is None.
        """
        return str(value) if value is not None else "-"

    def _get_fields(self, result: ScrapeResult) -> List[str]:
        """
        Extract relevant fields from a ScrapeResult.

        Args:
            result (ScrapeResult): Result object.

        Returns:
            List[str]: List of fields for error formatting.
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
        Format a single error entry as a string.

        Args:
            result (ScrapeResult): Result object containing error.

        Returns:
            str: Formatted string representing the error line.
        """
        fields = self._get_fields(result)
        return " | ".join(self._safe_str(v) for v in fields) + "\n"
