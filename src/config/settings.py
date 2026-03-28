# ./src/config/settings.py

import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()


@dataclass
class Settings:
    timeout: int = os.getenv("TIMEOUT", 10)
    retries: int = os.getenv("RETRIES", 2)
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )
    max_concurrency: int = 5
    proxy_file: str = os.getenv("PROXY_FILE", "data/proxy.json")
    urls_file: str = os.getenv("URLS_FILE", "data/urls.csv")
    output_csv_file: str = os.getenv("OUTPUT_CSV_FILE", "data/results.csv")
    output_json_file: str = os.getenv("OUTPUT_JSON_FILE", "data/results.json")
    output_error_file: str = os.getenv(
        "OUTPUT_ERROR_FILE", "data/results.error")
    protocol: str = os.getenv("PROTOCOL", "http://")


settings = Settings()
