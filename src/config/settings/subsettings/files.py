# ./src/config/settings/subsettings/files.py
from .deps import dataclass


@dataclass
class FilesSettings:
    proxy: str = "data/proxy.json"
    urls: str = "data/urls.csv"
    output_csv: str = "data/results.csv"
    output_json: str = "data/results.json"
    output_error: str = "data/results.error"
