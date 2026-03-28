# ./src/pipeline/runner.py

import asyncio
from src.config.settings import settings
from src.services.input_loader import URLInputLoader
from src.pipeline.orchestrator import PipelineOrchestrator
from src.services.result_manager.result_manager import ResultManager


async def main():
    loader = URLInputLoader(settings.urls_file)
    urls = loader.get_urls()

    orchestrator = PipelineOrchestrator()
    await orchestrator.launch()
    results = await orchestrator.run(urls)

    saver = ResultManager(
        settings.output_csv_file,
        settings.output_json_file,
        settings.output_error_file,
    )

    saver.save_all(results)


if __name__ == "__main__":
    asyncio.run(main())
