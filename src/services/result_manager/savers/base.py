# ./src/services/result_manager/savers/base.py

from pathlib import Path
from src.utils.logger import Logger
from abc import ABC, abstractmethod
from typing import List, Callable, Any
from src.models.scrape_result import ScrapeResult

logger = Logger(__name__)


class BaseSaver(ABC):
    """
    Abstract base class for saving scraped results.

    Subclasses must implement the `save` method to define how
    `ScrapeResult` objects are persisted.
    """
    @abstractmethod
    def save(self, results: List[ScrapeResult]) -> None:
        """
        Save a list of scrape results.

        Args:
            results (List[ScrapeResult]): A list of `ScrapeResult` instances
                                          to be saved.

        Raises:
            NotImplementedError: Must be implemented in subclasses.
        """
        pass

    @staticmethod
    def write_file(
        file_path: Path,
        write_func: Callable[[Any], None],
        mode: str = "w",
        description: str = "file",
    ) -> None:
        """
        Write content to a file using a provided writing function.

        This method handles opening the file, calling the provided
        `write_func` to write content, and logging success or failure.

        Args:
            file_path (Path): The path to the file where content will
                              be written.
            write_func (Callable[[Any], None]): A function that takes
                                                a file-like object and
                                                writes the desired content
                                                to it.
            mode (str, optional): File opening mode. Defaults to "w".
            description (str, optional): A human-readable description of
                                         the file for logging purposes.
                                         Defaults to "file".

        Raises:
            Exception: Propagates any exception raised during file writing.
        """
        logger.info(f"Saving {description}: {file_path}")
        try:
            with file_path.open(mode, encoding="utf-8") as f:
                write_func(f)
            logger.info(f"{description} saved successfully to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save {description}: {e}")
            raise
