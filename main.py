# ./main.py

import asyncio
from src.pipeline import PipelineRunner
from src.utils import Logger

logger = Logger("Main")


def main() -> None:
    """
    Entry point for the scraping pipeline.

    Initializes the PipelineRunner and executes it asynchronously.
    """
    runner = PipelineRunner()
    try:
        asyncio.run(runner.run())
    except KeyboardInterrupt:
        logger.warning("Pipeline interrupted by user.")
    except Exception as e:
        logger.exception(f"Unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
