# ./src/config/proxy/deps.py

# ===== STD LIB =====
import json

# ===== INTERNAL =====
from src.config.deps import (
    Path,
    Optional,
    AppLogger,
    dataclass
)

# ===== ALIASES =====
logger = AppLogger("Proxy")

__all__ = ["json", "Path", "Optional", "dataclass", "logger"]
