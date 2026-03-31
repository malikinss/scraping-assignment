# ./src/config/deps.py

"""
Dependencies for the config module.

This module provides:
    - os: For operating system interactions.
    - json: For JSON parsing.
    - Path: For path manipulation.
    - Logger: For logging.
    - load_dotenv: For loading environment variables.
    - dataclass: For creating data classes.
"""

import os
import json
from pathlib import Path
from src.utils import Logger
from dotenv import load_dotenv
from dataclasses import dataclass

__all__ = [
    "os",
    "json",
    "Path",
    "Logger",
    "load_dotenv",
    "dataclass",
]
