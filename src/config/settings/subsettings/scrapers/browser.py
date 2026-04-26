# ./src/config/settings/subsettings/scrapers/browser.py
from .deps import dataclass, Proxy, ProxyManager, get_env


@dataclass
class BrowserSettings:
    timeout: float = 10000.0
    locale: str = "en-US"
    state: str = "networkidle"
    headless: bool = True
    proxy: Proxy = None

    def __post_init__(self) -> None:
        self._validate()

    @classmethod
    def from_env(cls, proxy_manager: ProxyManager) -> "BrowserSettings":
        return cls(
            timeout=get_env("BROWSER_TIMEOUT", cls.timeout, float),
            locale=get_env("BROWSER_LOCALE", cls.locale, str),
            state=get_env("BROWSER_STATE", cls.state, str),
            headless=get_env("BROWSER_HEADLESS", cls.headless, bool),
            proxy=proxy_manager.get_playwright_proxy(),
        )

    # ===== INTERNAL =====
    def _validate(self) -> None:
        if self.timeout <= 0:
            raise ValueError("Browser timeout must be positive")
        if not self.locale:
            raise ValueError("Browser locale cannot be empty")
        if self.state not in ["load", "domcontentloaded", "networkidle"]:
            raise ValueError(
                "Browser state must be 'load', 'domcontentloaded', "
                "or 'networkidle'"
            )
