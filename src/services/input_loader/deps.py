# ./src/services/input_loader/deps.py

"""
This module contains the dependencies for the input loader service.

It re-exports commonly used components and types for easy access.

Imports:
    pandas as pd: For data manipulation (DataFrames).
    URLs: Type alias for list of URLs.
    URLUtils: Utility class for URL operations.
    AppLogger: Logger for the application.

Exposed Components:
    - pd: pandas library
    - URLs: Type alias for list of URLs
    - URLUtils: URL validation and utilities
    - AppLogger: Application logger
"""

import pandas as pd
from src.models import URLs
from src.utils import URLUtils
from src.logger import AppLogger

__all__ = ["pd", "URLs", "URLUtils", "AppLogger"]
