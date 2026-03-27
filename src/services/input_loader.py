# ./src/services/input_loader.py

from typing import List
import pandas as pd
from urllib.parse import urlparse


class URLInputLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.raw_data: pd.DataFrame | None = None
        self.urls: List[str] = []

    def load(self) -> "URLInputLoader":
        try:
            self.raw_data = pd.read_csv(self.file_path, header=None)
        except Exception as e:
            raise ValueError(f"Error loading file: {e}")

        return self

    def clean(self) -> "URLInputLoader":
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
        valid_urls = []
        for url in self.urls:
            parsed = urlparse(url)
            if parsed.scheme in ("http", "https") and parsed.netloc:
                valid_urls.append(url)
        self.urls = valid_urls
        return self

    def get_urls(self) -> List[str]:
        if not self.urls:
            self.load().clean().validate()
        return self.urls
