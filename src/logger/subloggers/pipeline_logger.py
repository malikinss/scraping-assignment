# ./src/logger/subloggers/pipeline_logger.py
from .lp import LLine
from .core import Logger
from .deps import Counts


class PipelineLogger:
    def __init__(self, logger: Logger):
        self.log = logger

    # ===== PIPELINE LIFECYCLE =====

    def start(self, total: int, concurrency: int):
        self.log.separator()
        msg = LLine().text("Pipeline started:")
        msg.kv("total", total).kv("concurrency", concurrency)
        self.log.info(msg.build())

    def summary(self, stats: Counts) -> None:
        self.log.separator()
        data = LLine().text("Pipeline completed:")
        for key, value in stats.items():
            data.kv(key.value, value)
        self.log.info(data.build())
        self.log.separator()

    # ===== CONTROL FLOW EVENTS =====

    def no_urls(self):
        msg = LLine().text("No URLs to process.")
        self.log.warning(msg.build())

    def no_results(self):
        msg = LLine().text("No results produced.")
        self.log.warning(msg.build())

    def interrupted(self):
        msg = LLine().text("Interrupted by user.")
        self.log.warning(msg.build())

    def no_proxy(self, method: str) -> None:
        msg = LLine().prefix(-1, method, "N/A", 0)
        msg.text("NO PROXY CONFIGURED")
        self.log.warning(msg.build())

    def exception(self, e: Exception):
        self.log.exception(f"Pipeline exception: {e}")

    # ===== SCRAPING FALLBACKS =====

    def fallback(self, id: int, url: str, status: str) -> None:
        msg = LLine().id(id).bracket("FALLBACK_BROWSER")
        msg.url(url).kv("reason", status)
        self.log.warning(msg.build())

    # ===== CONFIGURATION =====

    def settings(
        self,
        http_timeout: float,
        browser_timeout: float,
        retries: int,
        concurrency: int
    ) -> None:
        self.log.separator()
        msg = LLine().text("Settings loaded").kv("source", ".env")
        msg.kv("http_timeout", http_timeout)
        msg.kv("browser_timeout", browser_timeout)
        msg.kv("retries", retries)
        msg.kv("concurrency", concurrency)
        self.log.info(msg.build())

    # ===== PROXY EVENTS =====

    def proxy_fail(self, e: Exception):
        self.log.error(f"Failed to initialize proxy manager: {e}")

    def proxy_success(self, hostname: str):
        msg = LLine().text("Loaded proxy for")
        msg.kv("hostname", hostname)
        self.log.info(msg.build())
