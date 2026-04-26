# ./src/logger/subloggers/metrics_logger.py
from .lp import LLine
from .core import Logger


class MetricsLogger:
    def __init__(self, logger: Logger):
        self.log: Logger = logger

    def log_metrics(self, name: str, metrics: dict):
        msg = LLine().bracket(name).text("METRICS:").text(str(metrics))
        self.log.info(msg.build())

    def log_distribution(self, name: str, distribution: dict):
        msg = LLine().bracket(name).text("DISTRIBUTION:")
        msg.text(str(distribution))
        self.log.info(msg.build())

    def log_no_metrics(self, name: str):
        msg = LLine().bracket(name).text("NO METRICS")
        self.log.warning(msg.build())

    def log_metrics_exception(self, name: str, e: Exception):
        self.log.exception(f"Failed metrics for {name}: {e}")
