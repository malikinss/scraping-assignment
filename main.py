# ./main.py

"""
Main Module

This module is the entry point for the scraping pipeline.

It initializes the `PipelineRunner` and executes it asynchronously.

Core Components:
    - PipelineRunner: Runs the scraping pipeline.

Key Responsibilities:
    - Initialize and run the scraping pipeline.
    - Handle KeyboardInterrupt exceptions.
    - Log pipeline execution and errors.

Design:
    The `main` module implements a simple but effective design:
    1. Initialize the `PipelineRunner` class.
    2. Run the `PipelineRunner` asynchronously using `asyncio.run()`.
    3. Handle `KeyboardInterrupt` exceptions gracefully.
    4. Log any unhandled exceptions that occur.

Typical Workflow:
    1. Import necessary modules (`asyncio`, `PipelineRunner`, `AppLogger`).
    2. Get the `AppLogger` instance.
    3. Define the `main` function.
    4. Create an instance of `PipelineRunner`.
    5. Run the pipeline using `asyncio.run(runner.run())` within a try-except
       block.
    6. Handle `KeyboardInterrupt` and other exceptions.
    7. Use the `if __name__ == "__main__":` block to run the `main` function.
"""

import asyncio
from src.pipeline import PipelineRunner
from src.logger import AppLogger

logger: AppLogger = AppLogger("Main")


def main() -> None:
    """
    Entry point for the scraping pipeline.

    Initializes the `PipelineRunner` and executes it asynchronously.
    """
    runner = PipelineRunner()
    try:
        asyncio.run(runner.run())
    except KeyboardInterrupt:
        logger.pipeline.interrupted()
    except Exception as e:
        logger.pipeline.exception(e)


if __name__ == "__main__":
    main()
