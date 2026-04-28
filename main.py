# ./main.py
import asyncio
from src import PipelineRunner, AppLogger
logger: AppLogger = AppLogger("Main")


def main() -> None:
    runner = PipelineRunner()
    try:
        asyncio.run(runner.run())
    except KeyboardInterrupt:
        logger.pipeline.interrupted()
    except Exception as e:
        logger.pipeline.exception(e)


if __name__ == "__main__":
    main()
