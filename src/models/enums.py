# ./src/models/enums.py

from enum import Enum


class ScrapeStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CAPTCHA = "captcha"
    BLOCKED = "blocked"
    EMPTY = "empty"


class ScrapeMethod(str, Enum):
    HTTPX = "httpx"
    PLAYWRIGHT = "playwright"
