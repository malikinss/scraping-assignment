# ./src/models/scrape/result.py
from .status import ScrapeStatus
from .method import ScrapeMethod
from .deps import Optional, dataclass, asdict


@dataclass(slots=True)
class ScrapeResult:
    id: int
    url: str
    method: ScrapeMethod
    status: ScrapeStatus
    latency: float
    content_length: int
    error: Optional[str] = None
    content: Optional[str] = None

    # ===== SERIALIZATION =====
    def to_dict(self, include_content: bool = True) -> dict:
        result = asdict(self)
        if not include_content:
            result["content"] = None
        return result

    # ===== REPRESENTATION =====
    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"    id={self.id},\n"
            f"    url='{self.url}',\n"
            f"    method={self.method.value},\n"
            f"    status={self.status.value},\n"
            f"    latency={self.latency:.3f}s,\n"
            f"    content_length={self.content_length},\n"
            f"    error={self.error},\n"
            f"    content={'<omitted>' if self.content else None}\n"
            f")"
        )

    def __repr__(self) -> str:
        return self.__str__()

    # ===== DOMAIN PROPERTIES =====

    @property
    def is_success(self) -> bool:
        return self.status.is_success

    @property
    def is_failure(self) -> bool:
        return self.status.is_failure

    @property
    def is_content(self) -> bool:
        return self.status.is_content

    # ===== DATAFRAME CONVERSION =====
    @classmethod
    def from_row(cls, row: dict) -> "ScrapeResult":
        return cls(
            id=int(row.get("id") or 0),
            url=str(row.get("url") or ""),
            method=ScrapeMethod.from_name(row.get("method") or "httpx"),
            status=ScrapeStatus.from_name(row.get("status") or "failed"),
            latency=float(row.get("latency") or 0.0),
            content_length=int(row.get("content_length") or 0),
            error=row.get("error") or None,
            content=row.get("content") or None,
        )
