# ./src/pipeline/orchestrator/deps.py
from dataclasses import replace
from asyncio import Task, Queue, QueueEmpty
from typing import List, Callable, Awaitable, Union
from src.scrapers import HTTPScraper, BrowserScraper
from src.models import ScrapeResult, ScrapeStatus, ScrapeMethod, URL
from src.pipeline.deps import (
    Optional, settings, AppLogger, ScrapeResults, URLs
)

# unnormal types
UnNormalResult = Union[ScrapeResult, Exception]
UnNormalResults = List[UnNormalResult]

# tasks
HttpTask = tuple[int, URL]
BrowserTask = tuple[int, URL, ScrapeResult]

# queues
HTTPQueue = Queue[Optional[HttpTask]]
BrowserQueue = Queue[Optional[BrowserTask]]
ResultQueue = Queue[ScrapeResult]

# handlers
Handler = Callable[..., Awaitable[None]]

logger: AppLogger = AppLogger("Orchestrator")

__all__ = [
    # dataclasses
    "replace",
    # async
    "Task",
    "Queue",
    "QueueEmpty",
    # config
    "settings",
    # logger
    "logger",
    # typing
    "Optional",
    "List",
    "Callable",
    "Awaitable",
    "Union",
    # models
    "ScrapeResult",
    "ScrapeResults",
    "ScrapeStatus",
    "ScrapeMethod",
    "URL",
    "URLs",
    # scrapers
    "HTTPScraper",
    "BrowserScraper",
    # tasks
    "HttpTask",
    "BrowserTask",
    # results
    "UnNormalResult",
    "UnNormalResults",
    # queues
    "HTTPQueue",
    "BrowserQueue",
    "ResultQueue",
    # handlers
    "Handler"
]
