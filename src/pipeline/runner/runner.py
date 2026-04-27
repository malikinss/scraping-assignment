# ./src/pipeline/runner/runner.py

from .deps import (
    Optional,
    URLs,
    URLInputLoader,
    ScrapeResults,
    SaverManager,
    MetricsReporter,
    logger,
    INPUT_FILE,
    OUTPUT_FILE
)

from src.pipeline.orchestrator import PipelineOrchestrator


class PipelineRunner:
    def __init__(self,
                 loader: Optional[URLInputLoader] = None,
                 saver: Optional[SaverManager] = None,
                 reporter: Optional[MetricsReporter] = None,
                 orchestrator: Optional[PipelineOrchestrator] = None
                 ):
        self.urls: Optional[URLs] = None
        self.results: ScrapeResults = ScrapeResults()

        # dependency injection
        self.loader = loader or URLInputLoader(INPUT_FILE)
        self.saver = saver or SaverManager(OUTPUT_FILE)
        self.reporter = reporter or MetricsReporter()
        self.orchestrator = orchestrator or PipelineOrchestrator()

    # ===== PIPELINE EXECUTION =====

    async def run(self) -> None:
        self.urls = self._safe(self._load_urls)
        if not self.urls:
            logger.pipeline.no_urls()
            return

        self.results = await self._safe_async(self._process, self.urls)
        if not self.results:
            logger.pipeline.no_results()
            return

        self._safe(self._save, self.results)
        self._safe(self._report_metrics, self.results)

    # ===== PIPELINE STEPS =====

    def _load_urls(self) -> Optional[URLs]:
        return self.loader.get_urls()

    async def _process(self, urls: URLs) -> ScrapeResults:
        return await self.orchestrator.process_pipeline(urls)

    def _save(self, results: ScrapeResults) -> None:
        self.saver.save_all(results)

    def _report_metrics(self, results: ScrapeResults) -> None:
        self.reporter.report(results)

    # ===== SAFE EXECUTION LAYER =====

    def _safe(self, fn, *args, default=None):
        try:
            return fn(*args)
        except Exception as e:
            logger.pipeline.exception(e)
            return default

    async def _safe_async(self, fn, *args, default=None):
        try:
            return await fn(*args)
        except Exception as e:
            logger.pipeline.exception(e)
            results = ScrapeResults()
            if default is not None:
                results = default
            return results
