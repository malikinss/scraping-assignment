# ./src/config/settings.py

"""
Application settings and environment configuration.

This module defines the `Settings` dataclass responsible for:
    - Loading configuration from environment variables
    - Providing default fallback values
    - Validating configuration integrity
    - Logging initialized settings

It serves as the central configuration layer of the application.
"""

from .deps import os, load_dotenv, dataclass, AppLogger

logger = AppLogger("Settings")
load_dotenv()


def _get_env(key: str, default, cast):
    """
    Retrieve and cast environment variable with fallback.

    Supports type casting and safe defaults. Special handling is included
    for boolean values.

    Args:
        key (str): Environment variable name.
        default (Any): Default value if env variable is missing.
        cast (type): Type to cast the value into.

    Returns:
        Any: Parsed and cast environment value or default.

    Raises:
        ValueError: If casting fails for invalid environment value.
    """
    value = os.getenv(key)
    if value is None:
        return default
    try:
        if cast is bool:
            return value.lower() in ("1", "true", "yes")
        return cast(value)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid value for env '{key}': {value}")


@dataclass
class Settings:
    """
    Application settings and environment configuration.

    This module defines the `Settings` dataclass responsible for:
        - Loading configuration from environment variables
        - Providing default fallback values
        - Validating configuration integrity
        - Logging initialized settings

    It serves as the central configuration layer of the application.
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

    # ===== FACTORY =====

    @classmethod
    def from_env(cls) -> "Settings":
        """
        Create Settings instance from environment variables.

        Loads configuration from environment variables with fallback to
        default values. Validates the loaded configuration and logs the
        initialized settings.

        Returns:
            Settings: Initialized Settings instance.

        Raises:
            ValueError: If any environment variable has an invalid value.
        """
        instance = cls(
            http_timeout=_get_env("HTTP_TIMEOUT", cls.http_timeout, float),
            browser_timeout=_get_env(
                "BROWSER_TIMEOUT", cls.browser_timeout, float),
            retries=_get_env("RETRIES", cls.retries, int),
            user_agent=_get_env("USER_AGENT", cls.user_agent, str),
            max_concurrency=_get_env(
                "MAX_CONCURRENCY", cls.max_concurrency, int
            ),
            proxy_file=_get_env("PROXY_FILE", cls.proxy_file, str),
            urls_file=_get_env("URLS_FILE", cls.urls_file, str),
            output_csv_file=_get_env(
                "OUTPUT_CSV_FILE", cls.output_csv_file, str
            ),
            output_json_file=_get_env(
                "OUTPUT_JSON_FILE", cls.output_json_file, str
            ),
            output_error_file=_get_env(
                "OUTPUT_ERROR_FILE", cls.output_error_file, str
            ),
            protocol=_get_env("PROTOCOL", cls.protocol, str),
        )

        instance._validate()
        instance._log()

        return instance

    # ===== INTERNAL =====

    def _validate(self) -> None:
        """
        Validate the integrity of the loaded settings.

        Performs the following checks:
            - All timeout values must be positive
            - Retries must be non-negative
            - Max concurrency must be positive
            - User agent must not be empty
            - Protocol must start with http:// or https://

        Raises:
            ValueError: If any validation check fails.
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
        if not self.protocol.startswith(("http://", "https://")):
            raise ValueError("Protocol must start with http:// or https://")

    def _log(self) -> None:
        """
        Log the initialized settings for debugging purposes.

        This method logs the following configuration values:
            - HTTP timeout
            - Browser timeout
            - Number of retries
            - Maximum concurrency level

        The log output is formatted for pipeline-level visibility.
        """
        logger.pipeline.settings(
            http_timeout=self.http_timeout,
            browser_timeout=self.browser_timeout,
            retries=self.retries,
            concurrency=self.max_concurrency
        )
