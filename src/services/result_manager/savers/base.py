# ./src/services/result_manager/savers/base.py

"""
Base Saver
========

This abstract base class defines the interface for all saver classes.

It provides a common structure for saving results and handles file
I/O operations, including directory creation and error handling.

Usage:
    >>> from src.services.result_manager.savers import BaseSaver
    >>> saver = BaseSaver()
    >>> saver.save(results)

Example:
    >>> from src.services.result_manager.savers import BaseSaver
    >>> saver = BaseSaver()
    >>> saver.save(results)
"""

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
    """
    This abstract base class defines the interface for all saver classes.

    It provides a common structure for saving results and handles file
    I/O operations, including directory creation and error handling.
    """

    @abstractmethod
    def save(self, results: ScrapeResults) -> None:
        """
        Save the results to a file.

        Args:
            results (ScrapeResults): Results of the scraping process.

        Raises:
            NotImplementedError: If the method is not implemented by
                                 a subclass.
        """
        raise NotImplementedError(
            "Subclasses must implement the `save` method."
        )

    # ===== CORE IO UTILITY =====
    @staticmethod
    def write_file(
        file_path: Path,
        writer: WriterFunc,
        mode: str = "w",
        description: str = "file",
    ) -> None:
        """
        Write data to a file with proper error handling.

        Args:
            file_path (Path): Path to the file to write.
            writer (WriterFunc): Function to write data to the file.
            mode (str): Mode to open the file in.
            description (str): Description of the file.

        Raises:
            IOError: If the file cannot be written to.
        """
        try:
            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with file_path.open(mode, encoding="utf-8") as f:
                writer(f)

        # Handle exceptions
        except Exception as e:
            logger.storage.save_failure(
                description,
                f"Failed to save {description}: path={file_path}, error={e}"
            )
            raise
