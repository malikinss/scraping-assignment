# ./src/services/results/saver/savers/json.py

import json
from .base import BaseSaver
from .deps import Path, AppLogger, ScrapeResults, IO

logger = AppLogger("JSONSaver")


class JSONResultSaver(BaseSaver):

    def __init__(self, file_path: str, pretty: bool = True):
        self.file_path: Path = Path(file_path)
        self.pretty: bool = pretty

    # ===== PUBLIC =====
    def save(self, results: ScrapeResults) -> None:
        if not results:
            logger.storage.no_results("JSON", str(self.file_path))
            return

        self.write_file(
            self.file_path,
            lambda f: self._writer(f, results),
            description="JSON file"
        )

        logger.storage.file_save_success(
            "JSON",
            str(self.file_path),
            len(results)
        )

    def _writer(self, file: IO[str], results: ScrapeResults) -> None:
        json.dump(
            results.to_list(),
            file,
            ensure_ascii=False,
            indent=(4 if self.pretty else None)
        )
