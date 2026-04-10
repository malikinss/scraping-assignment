# ./src/services/result_manager/savers/base.py

from .deps import (
    Path,
    Logger,
    ABC,
    abstractmethod,
    Callable,
    Any,
    ScrapeResults
)

logger = Logger("BaseSaver")


class BaseSaver(ABC):
    """
    Abstract base class for result persistence strategies.

    Defines the interface for saving `ScrapeResults` and provides a shared
    utility method for safe file writing.

    Subclasses should implement the `save` method to define how results
    are serialized and stored (e.g., CSV, JSON, database).
    """

    @abstractmethod
    def save(self, results: ScrapeResults) -> None:
        """
        Persist scrape results.

        Args:
            results (ScrapeResults): Collection of scrape results to save.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError(
            "Subclasses must implement the `save` method."
        )

    @staticmethod
    def write_file(
        file_path: Path,
        write_func: Callable[[Any], None],
        mode: str = "w",
        description: str = "file",
    ) -> None:
        """
        Write data to a file using a provided writer function.

        Handles file opening and ensures consistent error logging.
        The actual writing logic is delegated to `write_func`.

        Args:
            file_path (Path): Path to the target file.
            write_func (Callable[[Any], None]): Function that receives
                a file-like object and writes data to it.
            mode (str, optional): File open mode (e.g., "w", "a").
                Defaults to "w".
            description (str, optional): Human-readable description of
                the file (used in logging). Defaults to "file".

        Raises:
            Exception: Re-raises any exception encountered during writing.
        """
        try:
            with file_path.open(mode, encoding="utf-8") as f:
                write_func(f)
        except Exception:
            logger.exception(
                f"Failed to save {description}: path={file_path}"
            )
            raise
