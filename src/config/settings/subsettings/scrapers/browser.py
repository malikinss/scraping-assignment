# ./src/config/settings/subsettings/scrapers/browser.py
from .deps import dataclass, Optional, proxy_manager


@dataclass
class BrowserSettings:
    timeout: float = 10000.0
    locale: str = "en-US"
    state: str = "networkidle"
    headless: bool = True
    proxy: Optional[str] = proxy_manager.get_proxy("browser")
