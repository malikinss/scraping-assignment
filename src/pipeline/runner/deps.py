# ./src/pipeline/runner/deps.py
from src.services import SaverManager, URLInputLoader, MetricsReporter
from src.pipeline.deps import (
    Optional, settings, AppLogger, ScrapeResults, URLs
)

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
