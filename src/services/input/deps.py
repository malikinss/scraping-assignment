# ./src/services/input/deps.py
import pandas as pd
from src.models import URLs
from src.utils import URLUtils
from src.services.deps import AppLogger
logger = AppLogger("Loader")
__all__ = ["pd", "URLs", "URLUtils", "logger"]
