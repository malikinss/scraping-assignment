# ./src/services/result_manager/savers/json_saver.py

from .base import BaseSaver
from .deps import (
    json,
    Any,
    List,
    Path,
    Logger,
    ScrapeResult,
)


logger = Logger("JSONSaver")


class JSONResultSaver(BaseSaver):
    """
    Saver implementation for exporting scrape results to a JSON file.

    This class serializes `ScrapeResult` objects into JSON format and writes
    them to a file. It supports both pretty-printed and compact output.
    """

    def __init__(self, file_path: str, pretty: bool = True):
        """
        Initialize the JSON result saver.

        Args:
            file_path (str): Path to the JSON file where results will be saved.
            pretty (bool, optional): If True, the JSON output will be formatted
                                     with indentation for readability.
                                     If False, a compact JSON representation
                                     will be used.
                                     Defaults to True.

        Example:
            >>> saver = JSONResultSaver("results.json")
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
        self.pretty: bool = pretty

    def save(self, results: List[ScrapeResult]) -> None:
        """
        Save scrape results to a JSON file.

        Converts each `ScrapeResult` instance to a dictionary and writes
        the resulting list to a JSON file. If no results are provided,
        the method logs the event and exits early.

        Args:
            results (List[ScrapeResult]): A list of `ScrapeResult` instances
                to be serialized and saved.

        Raises:
            Exception: Propagates any exception raised during file writing.

        Example:
            >>> saver = JSONResultSaver("results.json")
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
            logger.debug(
                f"JSON save skipped: no results path={self.file_path}"
            )
            return

        count = len(results)
        data = [self._safe_to_dict(r) for r in results]
        indent = 4 if self.pretty else None

        def writer(f):
            """
            Write JSON data to an open file handle.

            Args:
                f (IO[Any]): A file-like object opened for writing.
            """
            json.dump(data, f, ensure_ascii=False, indent=indent)

        self.write_file(self.file_path, writer, description="JSON file")
        logger.info(
            f"JSON saved: path={self.file_path} "
            f"count={count} "
            f"pretty={self.pretty}"
        )

    @staticmethod
    def _safe_to_dict(result: ScrapeResult) -> dict[str, Any]:
        """
        Safely convert ScrapeResult to dictionary.

        Ensures the result is JSON-serializable.
        """
        try:
            return result.to_dict()
        except Exception as e:
            return {
                "error": "serialization_failed",
                "reason": str(e),
                "raw": str(result),
            }
