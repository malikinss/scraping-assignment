# ./src/services/input_loader/input_loader.py

from .deps import (
    pd,
    List,
    Optional,
    URLUtils,
    Logger,
)


logger = Logger("URLLoader")


URL = str
URLs = List[URL]


class URLInputLoader:
    """
    A class for loading and processing URLs from a CSV file.

    Attributes:
        file_path (str): The path to the CSV file.
        raw_data (Optional[pd.DataFrame]): The raw data loaded from the CSV
        file.
        urls (List[str]): The list of valid URLs.
        _total_loaded (int): The total number of URLs loaded.
        _duplicates_removed (int): The number of duplicate URLs removed.
        _invalid_urls (int): The number of invalid URLs removed.

    Methods:
        load(self) -> "URLInputLoader": Loads the CSV file.
        clean(self) -> "URLInputLoader": Cleans the data.
        validate(self) -> "URLInputLoader": Validates the data.
        get_urls(self) -> List[str]: Gets the list of valid URLs.

    Raises:
        ValueError: If the data is not loaded.
        FileNotFoundError: If the file is not found.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If the file is not parsed.
        Exception: If any other error occurs.

    Example:
        >>> loader = URLInputLoader("urls.csv")
        >>> loader.load().clean().validate()
        >>> loader.get_urls()
    """

    def __init__(self, file_path: str):
        """
        Initializes the URLInputLoader.

        Args:
            file_path (str): The path to the CSV file.
        """
        self.file_path: str = file_path
        self.raw_data: Optional[pd.DataFrame] = None
        self.urls: URLs = []

        # internal counters
        self._total_loaded: int = 0
        self._duplicates_removed: int = 0
        self._invalid_urls: int = 0

    def load(self) -> "URLInputLoader":
        """
        Loads the CSV file.

        Returns:
            URLInputLoader: The URLInputLoader instance.
        """
        try:
            self.raw_data = pd.read_csv(self.file_path, header=None)
            self._total_loaded = len(self.raw_data)
        except FileNotFoundError:
            logger.error(f"Load failed: file not found path={self.file_path}")
            raise
        except pd.errors.EmptyDataError:
            logger.error(f"Load failed: empty file path={self.file_path}")
            raise
        except pd.errors.ParserError:
            logger.error(f"Load failed: parser error path={self.file_path}")
            raise
        except Exception as e:
            logger.error(
                f"Load failed: path={self.file_path} error={e}"
            )
            raise

        return self

    def clean(self) -> "URLInputLoader":
        """
        Cleans the data.

        Returns:
            URLInputLoader: The URLInputLoader instance.
        """
        self._ensure_loaded()
        urls_series = self.raw_data.iloc[:, 0]
        urls_series = urls_series.dropna().astype(str).str.strip()
        unique_urls = urls_series.unique()
        self._duplicates_removed = len(urls_series) - len(unique_urls)
        self.urls = unique_urls.tolist()
        return self

    def validate(self) -> "URLInputLoader":
        """
        Validates the data.

        Returns:
            URLInputLoader: The URLInputLoader instance.
        """
        self._ensure_loaded()
        valid_urls: List[str] = [
            url for url in self.urls if URLUtils.is_valid(url)
        ]
        self._invalid_urls = len(self.urls) - len(valid_urls)
        self.urls = valid_urls
        return self

    def get_urls(self) -> URLs:
        """
        Gets the list of valid URLs.

        Returns:
            List[str]: The list of valid URLs.
        """
        if not self.urls:
            self.load().clean().validate()

            logger.info(
                f"URLs loaded: "
                f"total={self._total_loaded} "
                f"valid={len(self.urls)} "
                f"duplicates_removed={self._duplicates_removed} "
                f"invalid={self._invalid_urls}"
            )
        return self.urls

    def _ensure_loaded(self):
        """
        Ensures that the data is loaded.

        Raises:
            ValueError: If the data is not loaded.
        """
        if self.raw_data is None:
            raise ValueError("Data not loaded. Call load() first")
