# ./src/services/results/saver/savers/error.py

from .base import BaseSaver
from .deps import (
    Any,
    List,
    Path,
    AppLogger,
    ScrapeResult,
    ScrapeResults,
    IO
)
logger = AppLogger("ErrorSaver")


class ErrorSaver(BaseSaver):

    def __init__(self, file_path: str):
        self.file_path: Path = Path(file_path)

    # ===== PUBLIC =====
    def save(self, results: ScrapeResults) -> None:
        if not results:
            logger.storage.no_results("Error", str(self.file_path))
            return

        errors: ScrapeResults = results.filter(lambda r: r.error is not None)
        if not errors:
            logger.storage.no_results("Error", str(self.file_path))
            return

        self.write_file(
            self.file_path,
            lambda f: self._writer(f, errors),
            description="error file"
        )

        logger.storage.file_save_success(
            "Error",
            str(self.file_path),
            len(errors)
        )

    # ===== CORE =====
    def _writer(self, file: IO[str], errors: ScrapeResults) -> None:
        file.writelines(self._format_error(r) for r in errors)

    # ===== INTERNAL HELPERS =====
    def _safe_str(self, value: Any) -> str:
        return str(value) if value is not None else "-"

    def _get_fields(self, result: ScrapeResult) -> List:
        return [
            result.id,
            result.url,
            result.method,
            result.status,
            result.error,
        ]

    def _format_error(self, result: ScrapeResult) -> str:
        fields = self._get_fields(result)
        return " | ".join(self._safe_str(v) for v in fields) + "\n"
