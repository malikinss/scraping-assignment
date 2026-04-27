# ./src/pipeline/orchestrator/worker/deps.py
import asyncio
from typing import List, Callable
from src.pipeline.orchestrator.deps import Task, Queue, Awaitable, Handler

Tasks = List[Task]
WorkerFn = Callable[[Handler, Queue], Awaitable[None]]

__all__ = ["asyncio", "Handler", "Queue", "WorkerFn", "Tasks"]
