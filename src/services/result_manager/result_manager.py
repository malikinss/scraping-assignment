# src/services/result_manager/result_manager.py

from typing import List
from src.models.scrape_result import ScrapeResult
from src.services.result_manager.csv_saver import CSVResultSaver
from src.services.result_manager.error_saver import ErrorLogger
from src.services.result_manager.json_saver import JSONResultSaver


class ResultManager:
    def __init__(self, csv_path: str, json_path: str, error_log_path: str):
        self.csv_saver = CSVResultSaver(csv_path)
        self.json_saver = JSONResultSaver(json_path)
        self.error_logger = ErrorLogger(error_log_path)

    def save_all(self, results: List[ScrapeResult]) -> None:
        self.csv_saver.save(results)
        self.json_saver.save(results)
        self.error_logger.save(results)
