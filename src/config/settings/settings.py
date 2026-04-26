# ./src/config/settings/settings.py

from .deps import dataclass, logger, Path, ProxyManager
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
        self._log()

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
        files = FilesSettings.from_env()
        proxy_manager = ProxyManager.from_file(Path(files.proxy))
        return cls(
            files=files,
            httpx=HTTPXSettings.from_env(proxy_manager),
            browser=BrowserSettings.from_env(proxy_manager),
            user_agent=UserAgentSettings.from_env(),
        )
