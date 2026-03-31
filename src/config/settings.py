# ./src/config/settings.py

from .deps import (
    os,
    load_dotenv,
    dataclass,
    Logger,
)

logger = Logger(__name__)
load_dotenv()


@dataclass
class Settings:
    """
    Application configuration loaded from environment variables.

    Attributes:
        http_timeout (`float`): Timeout for HTTP requests in seconds.
                              Defaults to 10.0.
        browser_timeout (`float`): Timeout for browser-based scraping in
                                 milliseconds. Defaults to 10000.0.
        retries (`int`): Number of retry attempts for failed requests.
                       Defaults to 2.
        user_agent (`str`): User-Agent string to be used for HTTP and browser
                          requests.
        max_concurrency (`int`): Maximum number of concurrent requests.
                               Defaults to 5.
        proxy_file (`str`): Path to JSON file containing proxy configurations.
        urls_file (`str`): Path to CSV file containing URLs to scrape.
        output_csv_file (`str`): Path to the CSV file where results will be
                               saved.
        output_json_file (`str`): Path to the JSON file where results will be
                                saved.
        output_error_file (`str`): Path to the file where errors will be
                                   logged.
        protocol (`str`): Default protocol to use for requests (e.g.,
                        "https://").
    """
    http_timeout: float = float(os.getenv("HTTP_TIMEOUT", 10.0))
    browser_timeout: float = float(os.getenv("BROWSER_TIMEOUT", 10000.0))
    retries: int = int(os.getenv("RETRIES", 2))
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
    protocol: str = os.getenv("PROTOCOL", "https://")


settings = Settings()
logger.info(
    f"Settings loaded: "
    f"http_timeout={settings.http_timeout}s, "
    f"browser_timeout={settings.browser_timeout}ms, "
    f"retries={settings.retries}, "
    f"max_concurrency={settings.max_concurrency}, "
    f"protocol={settings.protocol}, "
    f"user_agent={settings.user_agent}, "
    f"proxy_file={settings.proxy_file}"
)
