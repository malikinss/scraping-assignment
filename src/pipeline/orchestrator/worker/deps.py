# ./src/pipeline/orchestrator/worker/deps.py
import asyncio
from typing import List, Callable, Awaitable

# tasks
Task = asyncio.Task
Tasks = List[Task]

# queues
Queue = asyncio.Queue

# handlers
Handler = Callable[..., Awaitable[None]]
WorkerFn = Callable[[Handler, Queue], Awaitable[None]]

__all__ = ["asyncio", "Handler", "Queue", "WorkerFn", "Tasks"]
