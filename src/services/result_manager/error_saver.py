# src/services/result_manager/error_saver.py

from pathlib import Path
from typing import List

from src.models.scrape_result import ScrapeResult
from src.services.result_manager.base import BaseSaver


class ErrorLogger(BaseSaver):
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def save(self, results: List[ScrapeResult]) -> None:
        errors = [r for r in results if r.status.lower() != "success"]
        if not errors:
            return

        with self.file_path.open("w", encoding="utf-8") as f:
            for r in errors:
                f.write(
                    f"{r.url} | {r.method} | {r.status} | {r.error}\n"
                )
