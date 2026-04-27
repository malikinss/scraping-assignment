# ./src/pipeline/orchestrator/worker/worker.py
from .deps import asyncio, Handler, Queue, WorkerFn, Tasks


class WorkerGroup:
    def __init__(
        self,
        count: int,
        handler: Handler,
        queue: Queue,
        worker_fn: WorkerFn
    ):
        self.count = count
        self.handler = handler
        self.queue = queue
        self.worker_fn = worker_fn
        self.tasks: Tasks = []

    async def __aenter__(self) -> "WorkerGroup":
        self.start()
        return self

    async def __aexit__(self, *args) -> None:
        await self.stop()
        await self.wait()

    def start(self) -> None:
        self.tasks = [
            asyncio.create_task(self.worker_fn(self.handler, self.queue))
            for _ in range(self.count)
        ]

    async def stop(self) -> None:
        for _ in range(self.count):
            await self.queue.put(None)

    async def wait(self) -> None:
        await asyncio.gather(*self.tasks, return_exceptions=True)
