# ./src/services/result_manager/savers/csv_saver.py

import csv
from typing import List
from pathlib import Path
from .base import BaseSaver
from src.utils.logger import Logger
from src.models.scrape_result import ScrapeResult

logger = Logger(__name__)


class CSVResultSaver(BaseSaver):
    """
    Saver implementation for exporting scrape results to a CSV file.

    This class writes `ScrapeResult` objects into a CSV file using
    `csv.DictWriter`. It supports both overwriting and appending modes.
    """

    def __init__(self, file_path: str, append: bool = False):
        """
        Initialize the CSV result saver.

        Args:
            file_path (str): Path to the CSV file where results will be saved.
            append (bool, optional): If True, results will be appended to the
                                     existing file. If False, the file will be
                                     overwritten.
                                     Defaults to False.
        """
        logger.debug(
            f"Initializing CSVResultSaver: path={file_path}, append={append}"
        )
        self.file_path: Path = Path(file_path)
        self.append: bool = append

    def save(self, results: List[ScrapeResult]) -> None:
        """
        Save scrape results to a CSV file.

        If no results are provided, the method logs the event and exits early.
        Otherwise, it writes each result as a row in the CSV file. A header row
        is written if the file is new or opened in overwrite mode.

        Args:
            results (List[ScrapeResult]): A list of `ScrapeResult` instances
                                          to be written to the CSV file.

        Raises:
            Exception: Propagates any exception raised during file writing.
        """
        if not results:
            logger.info(f"No results to save to CSV: {self.file_path}")
            return

        logger.debug(
            f"Saving {len(results)} results to CSV file: {self.file_path}"
        )

        mode: str = "a" if self.append else "w"

        def writer(f):
            """
            Write results to an open file handle.

            Args:
                f (IO[Any]): A file-like object opened for writing.
            """
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "url",
                    "method",
                    "status",
                    "latency",
                    "content_length",
                    "error",
                ],
            )
            if not self.append or self.file_path.stat().st_size == 0:
                logger.debug("Writing header to CSV file")
                writer.writeheader()

            for r in results:
                writer.writerow(r.to_dict())
                logger.debug(f"Writing result to CSV file: {r.url}")

        self.write_file(self.file_path, writer, mode, description="CSV file")
