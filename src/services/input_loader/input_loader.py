# ./src/services/input_loader/input_loader.py

"""
Input Loader Service
====================

This module is responsible for loading URLs from a file.
It uses a pipeline approach to load, extract, deduplicate, and validate URLs.

Key Features:
    - Pipeline-based URL loading
    - Deduplication while preserving order
    - URL validation
    - Logging of load summary

Usage:
    >>> from src.services.input_loader import input_loader
    >>> urls = input_loader.get_urls("data/raw/urls.txt")
    >>> print(urls)

Example:
    >>> from src.services.input_loader import URLInputLoader
    >>> loader = URLInputLoader("data/raw/urls.txt")
    >>> urls = loader.run()
    >>> print(urls)
"""

from .deps import URLUtils, AppLogger, URLs, pd

logger = AppLogger("URLLoader")


class URLInputLoader:
    """
    This class is responsible for loading URLs from a file.

    It uses a pipeline approach to load, extract, deduplicate, and validate
    URLs.

    Attributes:
        file_path (str): Path to the file containing URLs.
    """

    def __init__(self, file_path: str):
        """
        Initializes the URLInputLoader with the given file path.

        Args:
            file_path (str): Path to the file containing URLs.
        """

        self.file_path = file_path

    # ===== PUBLIC PIPELINE =====

    def run(self) -> URLs:
        """
        Runs the URL loading pipeline.

        Returns:
            URLs: List of valid URLs.
        """
        data = self._load()
        urls = self._extract(data)
        urls = self._deduplicate(urls)
        urls, invalid = self._validate(urls)
        total = len(data)
        valid = len(urls)
        duplicates = total - valid - invalid

        logger.storage.load_summary(total, valid, duplicates, invalid)
        return urls

    # ===== STEPS =====

    def _load(self) -> pd.DataFrame:
        """
        Loads URLs from the file.

        Returns:
            pd.DataFrame: DataFrame containing URLs.
        """
        try:
            return pd.read_csv(self.file_path, header=None)

        except FileNotFoundError as e:
            logger.storage.load_failure("file not found", self.file_path)
            raise e
        except pd.errors.EmptyDataError as e:
            logger.storage.load_failure("empty file", self.file_path)
            raise e
        except pd.errors.ParserError as e:
            logger.storage.load_failure("parser error", self.file_path)
            raise e
        except Exception as e:
            logger.storage.load_failure(str(e), self.file_path)
            raise e

    def _extract(self, df: pd.DataFrame) -> URLs:
        """
        Extracts URLs from the DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing URLs.

        Returns:
            URLs: List of extracted URLs.
        """

        return (
            df.iloc[:, 0]
            .dropna()
            .astype(str)
            .str.strip()
            .tolist()
        )

    def _deduplicate(self, urls: URLs) -> URLs:
        """
        Removes duplicate URLs while preserving order.

        Args:
            urls (URLs): List of URLs.

        Returns:
            URLs: List of unique URLs.
        """
        # preserves order (faster than manual loop)
        return list(dict.fromkeys(urls))

    def _validate(self, urls: URLs) -> tuple[URLs, int]:
        """
        Validates URLs.

        Args:
            urls (URLs): List of URLs.

        Returns:
            tuple[URLs, int]: Tuple containing list of valid URLs and number
            of invalid URLs.
        """
        valid = []
        invalid = 0

        for url in urls:
            if URLUtils.is_valid(url):
                valid.append(url)
            else:
                invalid += 1

        return valid, invalid

    # ===== OPTIONAL API =====

    def get_urls(self) -> URLs:
        """
        Gets the list of valid URLs.

        Returns:
            URLs: List of valid URLs.
        """
        return self.run()
