###### ./src/services/results/saver/savers/

- Structure:

```text
./src/services/results/saver/savers/
|
├── __init__.py # expose public APIs
├── base.py     #
├── csv.py      #
├── deps.py     #
├── error.py    #
├── csv.py      #
└── json.py     #
```

- Implemetation:

```py
# ./src/services/results/saver/savers/__init__.py
from .base import BaseSaver
from .csv import CSVResultSaver
# from .error import ErrorSaver
# from .json import JSONResultSaver
__all__ = ["BaseSaver", "CSVResultSaver"]
```

```py
# ./src/services/results/saver/savers/base.py
from .deps import (Path, AppLogger, ABC, abstractmethod, Callable, Any, ScrapeResults)
WriterFunc = Callable[[Any], None]
logger = AppLogger("BaseSaver")

class BaseSaver(ABC):
    @abstractmethod
    def save(self, results: ScrapeResults) -> None:
        raise NotImplementedError()

    # ===== CORE IO UTILITY =====
    @staticmethod
    def write_file(file_path: Path, writer: WriterFunc, mode: str = "w", description: str = "file") -> None:
        try:
            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            # Write data to file
            with file_path.open(mode, encoding="utf-8") as f:
                writer(f)
        # Handle exceptions
        except Exception as e:
            msg = f"Failed to save {description}: path={file_path}, error={e}"
            logger.storage.save_failure(description, msg)
            raise
```

```py
# ./src/services/results/saver/savers/csv.py
import csv
from .base import BaseSaver
from .deps import Any, List, Path, AppLogger, ScrapeResults
logger = AppLogger("CSVSaver")

class CSVResultSaver(BaseSaver):
    FIELDNAMES: List[str] = ["id", "url", "method", "status", "latency", "content_length", "error"]

    def __init__(self, file_path: str, append: bool = False):
        self.file_path: Path = Path(file_path)
        self.append: bool = append

    # ===== PUBLIC =====

    def save(self, results: ScrapeResults) -> None:
        if not results:
            logger.storage.no_results("CSV", str(self.file_path))
            return
        self.write_file(self.file_path, lambda f: self._write_csv(f, results), self._get_mode(), description="CSV file")
        logger.storage.file_save_success("CSV", str(self.file_path), len(results))

    # ===== CORE WRITER =====
    def _write_csv(self, f, results: ScrapeResults) -> None:
        writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
        self._handle_header(writer)
        for r in results:
            row = r.to_dict()
            writer.writerow(self._filter_row(row))

    # ===== INTERNAL HELPERS =====
    def _need_header(self) -> bool:
        return (
            not self.append
            or not self.file_path.exists()
            or self.file_path.stat().st_size == 0
        )

    def _get_mode(self) -> str:
        return "a" if self.append else "w"

    def _filter_row(self, row: dict[str, Any]) -> dict[str, Any]:
        return {k: row.get(k, None) for k in self.FIELDNAMES}

    def _handle_header(self, writer: csv.DictWriter) -> None:
        if self._need_header():
            writer.writeheader()
```

```py
# ./src/services/results/saver/savers/deps.py
# ===== STD LIB =====
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Callable, Any, IO
# ===== INTERNAL =====
from src.services.results.result_manager.deps import AppLogger, ScrapeResult, ScrapeResults
__all__ = ["Path", "ABC", "abstractmethod", "List", "Callable", "Any", "IO", "AppLogger", "ScrapeResult", "ScrapeResults"]
```

```py
# ./src/services/results/saver/savers/json.py
import json
from .base import BaseSaver
from .deps import Path, AppLogger, ScrapeResults, IO
logger = AppLogger("JSONSaver")

class JSONResultSaver(BaseSaver):
    def __init__(self, file_path: str, pretty: bool = True):
        self.file_path: Path = Path(file_path)
        self.pretty: bool = pretty

    # ===== PUBLIC =====
    def save(self, results: ScrapeResults) -> None:
        if not results:
            logger.storage.no_results("JSON", str(self.file_path))
            return
        self.write_file(self.file_path, lambda f: self._writer(f, results), description="JSON file")
        logger.storage.file_save_success( "JSON", str(self.file_path), len(results))

    def _writer(self, file: IO[str], results: ScrapeResults) -> None:
        json.dump(results.to_list(), file, ensure_ascii=False, indent=(4 if self.pretty else None))
```

```py
# ./src/services/results/saver/savers/error.py
from .base import BaseSaver
from .deps import Any, List, Path, AppLogger, ScrapeResult, ScrapeResults, IO
logger = AppLogger("ErrorSaver")

class ErrorSaver(BaseSaver):
    def __init__(self, file_path: str):
        self.file_path: Path = Path(file_path)

    # ===== PUBLIC =====
    def save(self, results: ScrapeResults) -> None:
        if not results:
            logger.storage.no_results("Error", str(self.file_path))
            return
        errors: ScrapeResults = results.filter(lambda r: r.error is not None)
        if not errors:
            logger.storage.no_results("Error", str(self.file_path))
            return
        self.write_file(self.file_path, lambda f: self._writer(f, errors), description="error file")
        logger.storage.file_save_success( "Error", str(self.file_path), len(errors))

    # ===== CORE =====
    def _writer(self, file: IO[str], errors: ScrapeResults) -> None:
        file.writelines(self._format_error(r) for r in errors)

    # ===== INTERNAL HELPERS =====
    def _safe_str(self, value: Any) -> str:
        return str(value) if value is not None else "-"

    def _get_fields(self, result: ScrapeResult) -> List:
        return [result.id, result.url, result.method, result.status, result.error]

    def _format_error(self, result: ScrapeResult) -> str:
        fields = self._get_fields(result)
        return " | ".join(self._safe_str(v) for v in fields) + "\n"
```
