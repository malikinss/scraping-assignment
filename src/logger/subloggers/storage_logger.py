# ./src/logger/subloggers/storage_logger.py
from .lp import LLine
from .core import Logger


class StorageLogger:

    def __init__(self, logger: Logger):
        self.log: Logger = logger

    def no_results(self, file_type: str = "File", file_path: str = "") -> None:
        msg = LLine().bracket(file_type).text("save skipped:")
        msg.text("No results to save").kv("path", file_path)
        self.log.info(msg.build())

    def file_save_success(
        self,
        file_type: str,
        file_path: str,
        count: int
    ) -> None:
        msg = LLine().bracket(file_type).text("saved:")
        msg.text(str(count)).kv("path", file_path)
        self.log.info(msg.build())

    def save_success(self, statuses: dict) -> None:
        success = sum(statuses.values())
        msg = LLine().text("Save completed:")
        msg.kv("success", success)
        msg.kv("total", len(statuses))
        self.log.info(msg.build())

    def save_failure(self, name: str, error: Exception) -> None:
        msg = LLine().text("Save failed:").kv("target", name)
        msg.error(error)
        self.log.error(msg.build())

    def load_failure(self, message: str, file_path: str) -> None:
        msg = LLine().text("Load failed:").text(message)
        msg.kv("path", file_path)
        self.log.error(msg.build())

    def load_success(self, file_path: str) -> None:
        msg = LLine().text("Load success:")
        msg.kv("path", file_path)
        self.log.info(msg.build())

    def load_summary(
        self,
        total: int,
        valid: int,
        duplicates: int,
        invalid: int
    ) -> None:
        msg = LLine().text("Load summary:")
        msg.kv("total", total)
        msg.kv("valid", valid)
        msg.kv("duplicates", duplicates)
        msg.kv("invalid", invalid)
        self.log.info(msg.build())
