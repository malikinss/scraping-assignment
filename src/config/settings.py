from dataclasses import dataclass


@dataclass
class Settings:
    timeout: int = 10
    retries: int = 2
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )
    max_concurrency: int = 5


settings = Settings()
