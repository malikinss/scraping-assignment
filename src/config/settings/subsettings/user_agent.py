# ./src/config/settings/subsettings/user_agent.py
from .deps import dataclass


@dataclass
class UserAgentSettings:
    default: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )
    languages: str = "en-US,en;q=0.9"
