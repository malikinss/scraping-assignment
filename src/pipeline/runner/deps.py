# ./src/pipeline/runner/deps.py
from typing import Optional
from src.config import settings
from src.logger import AppLogger
from src.models import ScrapeResults, URLs
from src.services import SaverManager, URLInputLoader, MetricsReporter

INPUT_FILE = settings.files.urls
OUTPUT_FILE = settings.files.output_csv
logger: AppLogger = AppLogger("Runner")

__all__ = [
    "Optional",
    "ScrapeResults",
    "URLs",
    "URLInputLoader",
    "SaverManager",
    "MetricsReporter",
    "logger",
    "INPUT_FILE",
    "OUTPUT_FILE"
]
