# ./src/services/results/saver/savers/base.py

from .deps import (
    Path,
    AppLogger,
    ABC,
    abstractmethod,
    Callable,
    Any,
    ScrapeResults
)
WriterFunc = Callable[[Any], None]
logger = AppLogger("BaseSaver")


class BaseSaver(ABC):
    @abstractmethod
    def save(self, results: ScrapeResults) -> None:
        raise NotImplementedError()

    # ===== CORE IO UTILITY =====
    @staticmethod
    def write_file(
        file_path: Path,
        writer: WriterFunc,
        mode: str = "w",
        description: str = "file",
    ) -> None:
        try:
            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            # Write data to file
            with file_path.open(mode, encoding="utf-8") as f:
                writer(f)
        # Handle exceptions
        except Exception as e:
            msg = f"Failed to save {description}: path={file_path}, error={e}"
            logger.storage.save_failure(description, msg)
            raise
