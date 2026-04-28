# ./src/utils/deps.py

# ===== STD LIB =====
from typing import NamedTuple
from dotenv import load_dotenv
from urllib.parse import urlparse

# ===== INTERNAL =====
from src.deps import os
from src.models import URL

__all__ = [
    "os",
    "NamedTuple",
    "load_dotenv",
    "urlparse",
    "URL"
]
