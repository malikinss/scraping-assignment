# ./src/config/settings/deps.py

# ===== STD LIB =====
import os

# ===== EXTERNAL =====
from dotenv import load_dotenv

# ===== INTERNAL =====
from src.utils import get_env
from src.config.proxy import ProxyManager
from src.config.deps import (
    Path,
    Optional,
    AppLogger,
    dataclass
)

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
