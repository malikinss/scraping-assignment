# ./main.py

import asyncio
from src.pipeline import PipelineRunner
from src.logger import AppLogger

logger: AppLogger = AppLogger("Main")


def main() -> None:
    """
    Entry point for the scraping pipeline.

    Initializes the PipelineRunner and executes it asynchronously.
    """
    runner = PipelineRunner()
    try:
        asyncio.run(runner.run())
    except KeyboardInterrupt:
        logger.pipeline.log_interrupted()
    except Exception as e:
        logger.pipeline.log_exception(e)


if __name__ == "__main__":
    main()
