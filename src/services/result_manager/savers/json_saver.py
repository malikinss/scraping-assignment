# ./src/services/result_manager/savers/json_saver.py

from .base import BaseSaver
from .deps import json, Path, Logger, ScrapeResults

logger = Logger("JSONSaver")


class JSONResultSaver(BaseSaver):
    """
    Saver implementation for writing scrape results to a JSON file.

    Serializes `ScrapeResults` into JSON format. Supports both compact
    and pretty-printed output for readability.

    Attributes:
        file_path (Path): Path to the JSON file.
        pretty (bool): Whether to format JSON with indentation.
    """

    def __init__(self, file_path: str, pretty: bool = True):
        """
        Initialize the JSON saver.

        Args:
            file_path (str): Path to the JSON file.
            pretty (bool, optional): If True, formats JSON with indentation
                for readability. Defaults to True.
        """
        self.file_path: Path = Path(file_path)
        self.pretty: bool = pretty

    def save(self, results: ScrapeResults) -> None:
        """
        Save scrape results to a JSON file.

        Skips execution if results are empty. Uses BaseSaver's `write_file`
        utility to ensure safe file operations.

        Args:
            results (ScrapeResults): Collection of scrape results.

        Raises:
            Exception: Propagates exceptions raised during file writing.
        """
        if not results:
            logger.debug(
                f"JSON save skipped: no results path={self.file_path}"
            )
            return

        count = len(results)
        data = results.to_list()
        indent = 4 if self.pretty else None

        def writer(f):
            """
            Write JSON data to file.

            Args:
                f (IO[Any]): File-like object opened for writing.
            """
            json.dump(data, f, ensure_ascii=False, indent=indent)

        self.write_file(self.file_path, writer, description="JSON file")

        logger.info(
            f"JSON saved: path={self.file_path} "
            f"count={count} "
            f"pretty={self.pretty}"
        )
