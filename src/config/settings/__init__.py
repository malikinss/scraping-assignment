# ./src/config/__init__.py
from .settings import Settings
settings = Settings.from_env()
__all__ = ["settings"]
