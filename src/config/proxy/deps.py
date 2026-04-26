# ./src/config/proxy/deps.py

# ===== STD LIB =====
import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


# ===== INTERNAL =====
from src.logger import AppLogger

# ===== ALIASES =====
logger = AppLogger("Proxy")

__all__ = ["json", "Path", "Optional", "dataclass", "logger"]
