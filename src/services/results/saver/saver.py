# ./src/services/results/saver/saver.py
from .deps import Dict, AppLogger, ScrapeResults
from .savers import CSVResultSaver, BaseSaver as Saver
Statuses = Dict[str, bool]
Savers = Dict[str, Saver]
logger = AppLogger("SaverManager")


class SaverManager:
    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.savers: Savers = {}
        self.register_saver("csv", CSVResultSaver(self.file_path))

    # ===== REGISTRY =====
    def register_saver(self, name: str, saver: Saver) -> None:
        self.savers[name] = saver

    # ===== PUBLIC =====
    def save_all(self, results: ScrapeResults) -> Statuses:
        if not results:
            logger.storage.no_results()
            return {}
        statuses: Statuses = {name: self._safe_save(
            name, saver, results)for name, saver in self.savers.items()}
        logger.storage.save_success(statuses)
        return statuses

    # ===== CORE =====
    def _safe_save(self, name: str, saver: Saver, results: ScrapeResults) -> bool:
        try:
            saver.save(results)
            return True
        except Exception as e:
            logger.storage.save_failure(name, e)
            return False
