# ./src/services/result_manager/savers/csv_saver.py

from .deps import (
    csv,
    List,
    Path,
    Logger,
    ScrapeResult,
)
from .base import BaseSaver

logger = Logger("CSVSaver")


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

        Example:
            >>> saver = CSVResultSaver("test.csv")
            >>> saver.save([ScrapeResult("url", "content", "status")])
            file saved successfully to test.csv
        """
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

        Example:
            >>> saver = CSVResultSaver("test.csv")
            >>> saver.save([ScrapeResult("url", "content", "status")])
            Saving file: test.csv
            file saved successfully to test.csv
        """
        if not results:
            logger.debug(
                f"CSV save skipped: no results path={self.file_path}"
            )
            return

        mode: str = "a" if self.append else "w"

        def writer(f):
            """
            Write results to an open file handle.

            Args:
                f (IO[Any]): A file-like object opened for writing.
            """
            fieldnames = [
                "id",
                "url",
                "method",
                "status",
                "latency",
                "content_length",
                "error",
            ]
            writer = csv.DictWriter(
                f,
                fieldnames=fieldnames,
            )

            # Write header only if file is empty or in overwrite mode
            need_header = (
                not self.append
                or not self.file_path.exists()
                or self.file_path.stat().st_size == 0
            )
            if need_header:
                writer.writeheader()

            for r in results:
                row = r.to_dict()
                filtered_row = {k: row.get(k, None) for k in fieldnames}
                writer.writerow(filtered_row)

        # Use BaseSaver's utility to write file safely
        self.write_file(
            self.file_path,
            writer,
            mode,
            description="CSV file"
        )
        logger.info(
            f"CSV saved: path={self.file_path} count={len(results)}"
        )
