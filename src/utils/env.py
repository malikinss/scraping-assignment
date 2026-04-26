# ./src/utils/env.py
from .deps import os, load_dotenv
load_dotenv()


def get_env(key: str, default, cast):
    value = os.getenv(key)
    if value is None:
        return default
    try:
        if cast is bool:
            return value.lower() in ("1", "true", "yes")
        return cast(value)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid value for env '{key}': {value}")
