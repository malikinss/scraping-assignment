# ./src/services/result_manager/savers/error_saver.py

from .base import BaseSaver
from .deps import (
    Any,
    List,
    Path,
    Logger,
    ScrapeResult,
)

logger = Logger("ErrorSaver")


class ErrorLogger(BaseSaver):
    """
    Saver implementation for logging failed scrape results to a file.

    This class filters out failed `ScrapeResult` entries and writes
    them to a plain text file in a human-readable format.
    """

    def __init__(self, file_path: str):
        """
        Initialize the error logger.

        Args:
            file_path (str): Path to the file where error logs will be stored.

        Example:
            >>> saver = ErrorLogger("errors.txt")
            >>> saver.save([
            ...     ScrapeResult(
            ...         "url",
            ...         "method",
            ...         "status",
            ...         "latency",
            ...         "content_length",
            ...         "error"
            ...     ),
            ... ])
        """
        self.file_path: Path = Path(file_path)

    def save(self, results: List[ScrapeResult]) -> None:
        """
        Save failed scrape results to a file.

        This method filters results with status "failed" (case-insensitive)
        and writes them line-by-line to the specified file. If no results
        or no errors are found, the method exits early.

        Args:
            results (List[ScrapeResult]): A list of `ScrapeResult` instances
                                          to be processed.

        Raises:
            Exception: Propagates any exception raised during file writing.

        Example:
            >>> saver = ErrorLogger("errors.txt")
            >>> saver.save([
            ...     ScrapeResult(
            ...         "url",
            ...         "method",
            ...         "status",
            ...         "latency",
            ...         "content_length",
            ...         "error"
            ...     ),
            ... ])
        """
        if not results:
            logger.debug("Error save skipped: no results")
            return

        total = len(results)
        errors: List[ScrapeResult] = [r for r in results if r.is_error]
        error_count = len(errors)

        if error_count == 0:
            logger.debug(
                f"Error save skipped: no errors total={total}"
            )
            return

        def safe_str(value: Any) -> str:
            """
            Convert a value to string safely.
            """
            return str(value) if value is not None else "-"

        def format_error(r: ScrapeResult) -> str:
            """
            Format a single error entry into a string.
            """
            fields = [
                r.id,
                r.url,
                r.method,
                r.status,
                r.error,
            ]
            return " | ".join(safe_str(v) for v in fields) + "\n"

        def writer(f):
            """
            Write error entries to an open file handle.

            Args:
                f (IO[Any]): A file-like object opened for writing.
            """
            f.writelines(format_error(r) for r in errors)

        self.write_file(self.file_path, writer, description="error file")

        logger.info(
            f"Errors saved: "
            f"path={self.file_path} "
            f"errors={error_count} "
            f"total={total}"
        )
