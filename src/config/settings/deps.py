# ./src/config/settings/deps.py

# ===== STD LIB =====
import os
from pathlib import Path
from typing import Optional

# ===== EXTERNAL =====
from dotenv import load_dotenv
from dataclasses import dataclass

# ===== INTERNAL =====
from src.utils import get_env
from src.logger import AppLogger
from src.config.proxy import ProxyManager

# ===== PUBLIC =====
logger = AppLogger("Settings")

__all__ = [
    "os",
    "Path",
    "Optional",
    "load_dotenv",
    "dataclass",
    "logger",
    "ProxyManager",
    "get_env"
]
