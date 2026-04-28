# ./src/config/deps.py
# ===== STD LIB =====
from pathlib import Path
# ===== INTERNAL =====
from src.logger import AppLogger
from src.deps import Optional, dataclass
__all__ = [
    "Path",
    "Optional",
    "dataclass",
    "AppLogger"
]
