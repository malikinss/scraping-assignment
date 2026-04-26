# ./src/config/settings/settings.py

from .deps import dataclass, logger
from .subsettings import (
    FilesSettings,
    HTTPXSettings,
    BrowserSettings,
    UserAgentSettings,
)


@dataclass
class Settings:
    files: FilesSettings
    httpx: HTTPXSettings
    browser: BrowserSettings
    user_agent: UserAgentSettings

    def __post_init__(self) -> None:
        self._validate()
        self._log()

    # ===== INTERNAL =====
    def _validate(self) -> None:
        self.files._validate()
        self.httpx._validate()
        self.browser._validate()
        self.user_agent._validate()

    def _log(self) -> None:
        logger.pipeline.settings(
            http_timeout=self.httpx.timeout,
            browser_timeout=self.browser.timeout,
            retries=self.httpx.retries,
            concurrency=self.httpx.max_concurrency
        )

    # ===== PUBLIC =====
    @classmethod
    def from_env(cls):
        return cls(
            files=FilesSettings.from_env(),
            httpx=HTTPXSettings.from_env(),
            browser=BrowserSettings.from_env(),
            user_agent=UserAgentSettings.from_env()
        )
