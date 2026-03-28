# src/services/result_manager/csv_saver.py

import csv
from pathlib import Path
from typing import List

from src.models.scrape_result import ScrapeResult
from src.services.result_manager.base import BaseSaver


class CSVResultSaver(BaseSaver):
    def __init__(self, file_path: str, append: bool = False):
        self.file_path = Path(file_path)
        self.append = append

    def save(self, results: List[ScrapeResult]) -> None:
        mode = "a" if self.append else "w"
        with self.file_path.open(mode, newline="", encoding="utf-8") as f:
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
                writer.writeheader()
            for r in results:
                writer.writerow(r.to_dict())
