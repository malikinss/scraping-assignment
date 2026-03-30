# ./src/services/result_manager/savers/json_saver.py

from .base import BaseSaver
from .deps import (
    json,
    List,
    Path,
    Logger,
    ScrapeResult,
)


logger = Logger(__name__)


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
        """
        logger.debug(
            f"Initializing JSONResultSaver with path={file_path} and "
            f"pretty={pretty}"
        )
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
        """
        if not results:
            logger.info("No results provided to JSONResultSaver.")
            return

        logger.debug(
            f"Saving {len(results)} results to JSON file: {self.file_path}"
        )
        data = [r.to_dict() for r in results]

        def writer(f):
            """
            Write JSON data to an open file handle.

            Args:
                f (IO[Any]): A file-like object opened for writing.
            """
            if self.pretty:
                logger.debug("Writing pretty JSON to file")
                json.dump(data, f, ensure_ascii=False, indent=4)
            else:
                logger.debug("Writing compact JSON to file")
                json.dump(data, f, ensure_ascii=False)

        self.write_file(self.file_path, writer, description="JSON file")
