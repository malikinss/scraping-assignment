# ./src/services/result_manager/savers/error_saver.py

from .base import BaseSaver
from .deps import (
    List,
    Path,
    Logger,
    ScrapeResult,
)

logger = Logger(__name__)


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
        """
        logger.debug(f"Initializing ErrorLogger with path={file_path}")
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
        """
        if not results:
            logger.info("No results provided to ErrorLogger.")
            return

        errors: List[ScrapeResult] = [
            r for r in results if r.status.lower() == "failed"
        ]

        if not errors:
            logger.debug("No errors found in results.")
            return

        logger.debug(f"Saving {len(errors)} errors to file: {self.file_path}")

        def writer(f):
            """
            Write error entries to an open file handle.

            Args:
                f (IO[Any]): A file-like object opened for writing.
            """
            logger.debug("Writing errors to file")
            for r in errors:
                line = f"{r.url} | {r.method} | {r.status} | {r.error}\n"
                f.write(line)
                logger.debug(f"Wrote line: {line.strip()}")

        self.write_file(self.file_path, writer, description="error file")
