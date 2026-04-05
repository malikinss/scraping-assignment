# ./src/config/settings.py

from .deps import (
    os,
    load_dotenv,
    dataclass,
    Logger,
)

logger = Logger("Settings")
load_dotenv()


def _get_env(key: str, default, cast):
    """
    Safely get and cast environment variable.
    """
    try:
        return cast(os.getenv(key, default))
    except (TypeError, ValueError):
        raise ValueError(f"Invalid value for env '{key}'")


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
    http_timeout: float = 10.0
    browser_timeout: float = 10000.0
    retries: int = 2
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )
    max_concurrency: int = 5
    proxy_file: str = "data/proxy.json"
    urls_file: str = "data/urls.csv"
    output_csv_file: str = "data/results.csv"
    output_json_file: str = "data/results.json"
    output_error_file: str = "data/results.error"
    protocol: str = "https://"

    def __post_init__(self):
        """
        Post-initialization hook to load environment variables.

        This method is called after the object is initialized and is used to
        load environment variables into the settings object.

        Example:
            >>> settings = Settings()
            >>> settings.http_timeout
            10.0
        """
        self.http_timeout = _get_env("HTTP_TIMEOUT", self.http_timeout, float)
        self.browser_timeout = _get_env(
            "BROWSER_TIMEOUT", self.browser_timeout, float)
        self.retries = _get_env("RETRIES", self.retries, int)
        self.user_agent = _get_env(
            "USER_AGENT", self.user_agent, str)
        self.max_concurrency = _get_env(
            "MAX_CONCURRENCY", self.max_concurrency, int)
        self.proxy_file = _get_env("PROXY_FILE", self.proxy_file, str)
        self.urls_file = _get_env("URLS_FILE", self.urls_file, str)
        self.output_csv_file = _get_env(
            "OUTPUT_CSV_FILE", self.output_csv_file, str)
        self.output_json_file = _get_env(
            "OUTPUT_JSON_FILE", self.output_json_file, str)
        self.output_error_file = _get_env(
            "OUTPUT_ERROR_FILE", self.output_error_file, str)
        self.protocol = _get_env("PROTOCOL", self.protocol, str)

        self._validate()

    def _validate(self):
        """
        Validate the settings object.

        Raises:
            ValueError: If any of the settings are invalid.
        Example:
            >>> settings = Settings()
            >>> settings._validate()
        """
        if self.http_timeout <= 0:
            raise ValueError("HTTP timeout must be positive")
        if self.browser_timeout <= 0:
            raise ValueError("Browser timeout must be positive")
        if self.retries < 0:
            raise ValueError("Retries must be non-negative")
        if self.max_concurrency <= 0:
            raise ValueError("Max concurrency must be positive")
        if not self.user_agent:
            raise ValueError("User agent cannot be empty")
        if not self.proxy_file:
            raise ValueError("Proxy file cannot be empty")
        if not self.urls_file:
            raise ValueError("URLs file cannot be empty")
        if not self.output_csv_file:
            raise ValueError("Output CSV file cannot be empty")
        if not self.output_json_file:
            raise ValueError("Output JSON file cannot be empty")
        if not self.output_error_file:
            raise ValueError("Output error file cannot be empty")
        if not self.protocol.startswith(("http://", "https://")):
            raise ValueError("Protocol must start with http:// or https://")


settings = Settings()

logger.separator()
logger.info(
    f"Settings loaded: "
    f"source=.env "
    f"http_timeout={settings.http_timeout}s, "
    f"browser_timeout={settings.browser_timeout}ms, "
    f"retries={settings.retries}, "
    f"max_concurrency={settings.max_concurrency}, "
)
