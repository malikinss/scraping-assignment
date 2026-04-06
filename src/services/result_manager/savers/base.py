# ./src/services/result_manager/savers/base.py

from .deps import (
    Path,
    Logger,
    ABC,
    abstractmethod,
    ScrapeResult,
    List,
    Callable,
    Any,
)

logger = Logger("BaseSaver")


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

        Example:
            >>> saver = BaseSaver()
            >>> saver.save([ScrapeResult("url", "content", "status")])
            NotImplementedError: Must be implemented in subclasses.
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

        Example:
            >>> BaseSaver.write_file(
            ...     Path("test.txt"),
            ...     lambda f: f.write("test"),
            ... )
            Saving file: test.txt
            file saved successfully to test.txt
        """
        try:
            with file_path.open(mode, encoding="utf-8") as f:
                write_func(f)
        except Exception:
            logger.exception(
                f"Failed to save {description}: path={file_path}"
            )
            raise
