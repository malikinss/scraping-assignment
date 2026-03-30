# ./src/services/input_loader/input_loader.py

import pandas as pd
from typing import List, Optional
from urllib.parse import urlparse
from ...utils.logger import Logger

logger = Logger(__name__)


class URLInputLoader:
    """
    Loader for extracting, cleaning, and validating URLs from a CSV file.

    This class provides a pipeline to:
        1. Load URLs from a CSV file (first column, no header assumed).
        2. Clean the URLs by removing duplicates and trimming whitespace.
        3. Validate URLs to ensure they have a proper scheme and domain.
    """

    def __init__(self, file_path: str):
        """
        Initialize the URL input loader.

        Args:
            file_path (str): Path to the CSV file containing URLs.
        """
        logger.debug(
            f"Initializing URLInputLoader with file path: {file_path}")
        self.file_path: str = file_path
        self.raw_data: Optional[pd.DataFrame] = None
        self.urls: List[str] = []

    def load(self) -> "URLInputLoader":
        """
        Load raw URLs from the CSV file.

        Reads the first column of the CSV file into a DataFrame. Handles
        file not found, empty file, parsing errors, and generic exceptions.

        Returns:
            URLInputLoader: Self, to allow method chaining.

        Raises:
            FileNotFoundError: If the file does not exist.
            pd.errors.EmptyDataError: If the file is empty.
            pd.errors.ParserError: If the CSV cannot be parsed.
            Exception: For other errors during file reading.
        """
        logger.debug(f"Loading URLs from file path: {self.file_path}")
        try:
            self.raw_data = pd.read_csv(self.file_path, header=None)
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
            raise
        except pd.errors.EmptyDataError:
            logger.error(f"File is empty: {self.file_path}")
            raise
        except pd.errors.ParserError:
            logger.error(f"Error parsing file: {self.file_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading file: {e}")
            raise

        logger.debug(f"Loaded {len(self.raw_data)} rows")
        return self

    def clean(self) -> "URLInputLoader":
        """
        Clean URLs by trimming whitespace and removing duplicates.

        Returns:
            URLInputLoader: Self, to allow method chaining.

        Raises:
            ValueError: If data has not been loaded yet (call load() first).
        """
        if self.raw_data is None:
            raise ValueError("Data not loaded. Call load() first")

        logger.debug("Cleaning URLs")
        urls_series = self.raw_data.iloc[:, 0]
        urls = urls_series.dropna().astype(str).str.strip()

        before = len(urls)
        unique_urls = urls.unique().tolist()
        after = len(unique_urls)

        logger.debug(f"Removed {before - after} duplicate URLs")

        self.urls = unique_urls
        return self

    def validate(self) -> "URLInputLoader":
        """
        Validate URLs to ensure they have a valid HTTP/HTTPS scheme and domain.

        Returns:
            URLInputLoader: Self, to allow method chaining.
        """
        logger.debug("Validating URLs")
        valid_urls: List[str] = []
        invalid_count: int = 0

        for url in self.urls:
            parsed = urlparse(url)
            if parsed.scheme in ("http", "https") and parsed.netloc:
                valid_urls.append(url)
            else:
                invalid_count += 1

        logger.debug(f"Removed {invalid_count} invalid URLs")
        self.urls = valid_urls
        return self

    def get_urls(self) -> List[str]:
        """
        Retrieve the processed list of valid URLs.

        If URLs have not been loaded and processed yet, runs the full
        pipeline: load -> clean -> validate.

        Returns:
            List[str]: List of unique, valid URLs.
        """
        if not self.urls:
            logger.debug("URLs not processed yet, running full pipeline")
            self.load().clean().validate()

        logger.debug(f"Retrieved {len(self.urls)} URLs")
        return self.urls
