# ./src/config/deps.py

"""
Shared dependencies for configuration module.

This module centralizes commonly used standard library imports,
third-party utilities, and internal helpers required for configuration
loading and initialization.

It is used to reduce import duplication across configuration-related
modules and provide a single access point for shared dependencies.
"""

import os
import json
from pathlib import Path
from src.logger import AppLogger
from dotenv import load_dotenv
from dataclasses import dataclass

__all__ = [
    "os",
    "json",
    "Path",
    "AppLogger",
    "load_dotenv",
    "dataclass",
]
