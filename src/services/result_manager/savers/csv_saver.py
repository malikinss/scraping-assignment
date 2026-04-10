# ./src/services/result_manager/savers/csv_saver.py

from .deps import (
    Any,
    csv,
    List,
    Path,
    Logger,
    ScrapeResults
)
from .base import BaseSaver

logger = Logger("CSVSaver")


class CSVResultSaver(BaseSaver):
    """
    Saver implementation for writing scrape results to a CSV file.

    Serializes `ScrapeResults` into CSV format using `csv.DictWriter`.
    Supports both overwrite and append modes, and ensures consistent
    field ordering and header management.
    """

    def __init__(self, file_path: str, append: bool = False):
        """
        Initialize the CSV saver.

        Args:
            file_path (str): Path to the CSV file.
            append (bool, optional): If True, appends to the file.
                Otherwise overwrites it. Defaults to False.
        """
        self.file_path: Path = Path(file_path)
        self.append: bool = append

    def save(self, results: ScrapeResults) -> None:
        """
        Save scrape results to a CSV file.

        Skips writing if results are empty. Uses BaseSaver's `write_file`
        utility to ensure safe file operations.

        Args:
            results (ScrapeResults): Collection of scrape results.

        Raises:
            Exception: Propagates exceptions raised during file writing.
        """
        if not results:
            msg: str = f"CSV save skipped: no results path={self.file_path}"
            logger.debug(msg)
            return

        def writer(f):
            """
            Write rows into CSV file.

            Args:
                f (IO[Any]): File-like object opened for writing.
            """
            csv_writer = csv.DictWriter(f, fieldnames=self._get_fieldnames())
            self._handle_header(csv_writer)

            for r in results:
                csv_writer.writerow(self._get_filtered_row(r.to_dict()))

        self.write_file(
            self.file_path,
            writer,
            self._get_mode(),
            description="CSV file"
        )

        logger.info(f"CSV saved: path={self.file_path} count={len(results)}")

    # ===== INTERNAL HELPERS =====

    def _get_mode(self) -> str:
        """
        Determine file open mode.

        Returns:
            str: "a" for append mode or "w" for overwrite mode.
        """
        return "a" if self.append else "w"

    def _get_fieldnames(self) -> List[str]:
        """
        Return the ordered list of CSV columns.

        Returns:
            List[str]: Field names for CSV output.
        """
        return [
            "id",
            "url",
            "method",
            "status",
            "latency",
            "content_length",
            "error",
        ]

    def _get_filtered_row(self, row: dict[str, Any]) -> dict[str, Any]:
        """
        Filter and normalize a row to match CSV fieldnames.

        Ensures only expected fields are written and fills missing values
        with None.

        Args:
            row (dict[str, Any]): Raw row dictionary.

        Returns:
            dict[str, Any]: Filtered row aligned with CSV schema.
        """
        return {k: row.get(k, None) for k in self._get_fieldnames()}

    def _need_header(self) -> bool:
        """
        Determine whether the CSV header should be written.

        Header is written if:
            - File is opened in overwrite mode
            - File does not exist
            - File exists but is empty

        Returns:
            bool: True if header should be written.
        """
        return (
            not self.append
            or not self.file_path.exists()
            or self.file_path.stat().st_size == 0
        )

    def _handle_header(self, writer: csv.DictWriter) -> None:
        """
        Write CSV header if needed.

        Args:
            writer (csv.DictWriter): CSV writer instance.
        """
        if self._need_header():
            writer.writeheader()
