# ./src/pipeline/runner.py

import asyncio

from src.config.settings import settings
from src.services.result_saver import ResultSaver
from src.services.input_loader import URLInputLoader
from src.pipeline.orchestrator import PipelineOrchestrator


async def main():
    loader = URLInputLoader(settings.urls_file)
    urls = loader.get_urls()

    orchestrator = PipelineOrchestrator()
    await orchestrator.launch()
    results = await orchestrator.run(urls)

    saver = ResultSaver(settings.output_file)
    saver.save(results)


if __name__ == "__main__":
    asyncio.run(main())
