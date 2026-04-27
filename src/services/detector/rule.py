# ./src/services/detector/rule.py
from .deps import ScrapeStatus, dataclass, Tuple

Rules = Tuple["Rule", ...]
KeyWords = Tuple[str, ...]


@dataclass(frozen=True)
class Rule:
    status: ScrapeStatus
    keywords: KeyWords
