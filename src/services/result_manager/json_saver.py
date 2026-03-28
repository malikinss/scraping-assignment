# src/services/result_manager/json_saver.py

import json
from pathlib import Path
from typing import List

from src.models.scrape_result import ScrapeResult
from src.services.result_manager.base import BaseSaver


class JSONResultSaver(BaseSaver):
    def __init__(self, file_path: str, pretty: bool = True):
        self.file_path = Path(file_path)
        self.pretty = pretty

    def save(self, results: List[ScrapeResult]) -> None:
        data = [r.to_dict() for r in results]
        with self.file_path.open("w", encoding="utf-8") as f:
            if self.pretty:
                json.dump(data, f, ensure_ascii=False, indent=4)
            else:
                json.dump(data, f, ensure_ascii=False)
