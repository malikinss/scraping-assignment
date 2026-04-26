# ./src/services/results/saver/savers/csv.py

import csv
from .base import BaseSaver
from .deps import (
    Any,
    List,
    Path,
    AppLogger,
    ScrapeResults
)
logger = AppLogger("CSVSaver")


class CSVResultSaver(BaseSaver):

    FIELDNAMES: List[str] = [
        "id",
        "url",
        "method",
        "status",
        "latency",
        "content_length",
        "error",
    ]

    def __init__(self, file_path: str, append: bool = False):
        self.file_path: Path = Path(file_path)
        self.append: bool = append

    # ===== PUBLIC =====
    def save(self, results: ScrapeResults) -> None:
        if not results:
            logger.storage.no_results("CSV", str(self.file_path))
            return

        self.write_file(
            self.file_path,
            lambda f: self._write_csv(f, results),
            self._get_mode(),
            description="CSV file"
        )

        logger.storage.file_save_success(
            "CSV",
            str(self.file_path),
            len(results)
        )

    # ===== CORE WRITER =====
    def _write_csv(self, f, results: ScrapeResults) -> None:
        writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)

        self._handle_header(writer)

        for r in results:
            row = r.to_dict()
            writer.writerow(self._filter_row(row))

    # ===== INTERNAL HELPERS =====
    def _need_header(self) -> bool:
        return (
            not self.append
            or not self.file_path.exists()
            or self.file_path.stat().st_size == 0
        )

    def _get_mode(self) -> str:
        return "a" if self.append else "w"

    def _filter_row(self, row: dict[str, Any]) -> dict[str, Any]:
        return {k: row.get(k, None) for k in self.FIELDNAMES}

    def _handle_header(self, writer: csv.DictWriter) -> None:
        if self._need_header():
            writer.writeheader()
