# src/services/result_manager/base.py

from abc import ABC, abstractmethod
from typing import List

from src.models.scrape_result import ScrapeResult


class BaseSaver(ABC):
    @abstractmethod
    def save(self, results: List[ScrapeResult]) -> None:
        pass
