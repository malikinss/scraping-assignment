from typing import List
import pandas as pd
from urllib.parse import urlparse


class URLInputLoader:
    """
    Class for loading URLs from a CSV file.

    Attributes:
        file_path (str): Path to the CSV file.
        raw_data (pd.DataFrame | None): Raw data loaded from CSV.
        urls (List[str]): List of URLs loaded from CSV.
    """

    def __init__(self, file_path: str):
        """
        Initialize the URLInputLoader.

        Args:
            file_path (str): Path to the CSV file.
        """
        self.file_path = file_path
        self.raw_data: pd.DataFrame | None = None
        self.urls: List[str] = []

    def load(self) -> "URLInputLoader":
        """
        Load URLs from a CSV file.

        Returns:
            URLInputLoader: self, for chaining

        Raises:
            ValueError: If the file cannot be loaded.
        """
        try:
            self.raw_data = pd.read_csv(self.file_path, header=None)
        except Exception as e:
            raise ValueError(f"Error loading file: {e}")

        return self

    def clean(self) -> "URLInputLoader":
        """
        Clean the loaded data: remove NaN, strip spaces, remove duplicates.

        Returns:
            URLInputLoader: self, for chaining

        Raises:
            ValueError: If data is not loaded.
        """
        if self.raw_data is None:
            raise ValueError("Data not loaded")

        # first column
        urls = self.raw_data[0]

        # remove NaN and spaces
        urls = urls.dropna().astype(str).str.strip()

        # remove duplicates
        urls = urls.unique().tolist()
        self.urls = urls

        return self

    def validate(self) -> "URLInputLoader":
        """
        Validate the URLs: keep only http/https URLs with netloc.

        Returns:
            URLInputLoader: self, for chaining
        """
        valid_urls = []
        for url in self.urls:
            parsed = urlparse(url)
            if parsed.scheme in ("http", "https") and parsed.netloc:
                valid_urls.append(url)
        self.urls = valid_urls
        return self

    def get_urls(self) -> List[str]:
        """
        Get the loaded URLs. Loads, cleans, removes duplicates,
        and validates if not already done.

        Returns:
            List[str]: List of valid URLs.
        """
        if not self.urls:
            self.load().clean().validate()
        return self.urls
