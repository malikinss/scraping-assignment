# ./src/config/settings/subsettings/user_agent.py
from .deps import dataclass, get_env


@dataclass
class UserAgentSettings:
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )
    languages: str = "en-US,en;q=0.9"

    def __post_init__(self) -> None:
        self._validate()

    @classmethod
    def from_env(cls) -> "UserAgentSettings":
        return cls(
            languages=get_env("LANGUAGES", cls.languages, str),
            user_agent=get_env("USER_AGENT", cls.user_agent, str)
        )

    # ===== INTERNAL =====

    def _validate(self) -> None:
        if not self.languages:
            raise ValueError("Languages cannot be empty")
        if not self.user_agent:
            raise ValueError("User agent cannot be empty")
