# ./src/config/settings/subsettings/files.py
from .deps import dataclass, get_env


@dataclass
class FilesSettings:
    proxy: str = "data/proxy.json"
    urls: str = "data/urls.csv"
    output_csv: str = "data/results.csv"
    output_json: str = "data/results.json"
    output_error: str = "data/results.error"

    def __post_init__(self) -> None:
        self._validate()

    @classmethod
    def from_env(cls) -> "FilesSettings":
        return cls(
            proxy=get_env("PROXY_FILE", cls.proxy, str),
            urls=get_env("URLS_FILE", cls.urls, str),
            output_csv=get_env("OUTPUT_CSV_FILE", cls.output_csv, str),
            output_json=get_env("OUTPUT_JSON_FILE", cls.output_json, str),
            output_error=get_env("OUTPUT_ERROR_FILE", cls.output_error, str)
        )

    # ===== INTERNAL =====
    def _validate(self) -> None:
        if not self.proxy:
            raise ValueError("Proxy file cannot be empty")
        if not self.urls:
            raise ValueError("URLs file cannot be empty")
        if not self.output_csv:
            raise ValueError("Output CSV file cannot be empty")
        if not self.output_json:
            raise ValueError("Output JSON file cannot be empty")
        if not self.output_error:
            raise ValueError("Output error file cannot be empty")
