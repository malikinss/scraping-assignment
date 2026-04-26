# ./src/config/deps.py
# ===== STD LIB =====
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

# ===== INTERNAL =====
from src.logger import AppLogger

__all__ = [
    "Path",
    "Optional",
    "dataclass",
    "AppLogger"
]
