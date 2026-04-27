# ./src/services/metrics/models.py
from .subtypes import MetricFieldSpec
from .deps import Dict, Any, dataclass, asdict, ClassVar


@dataclass
class MetricsSummary:
    total_requests: int = 0
    success_rate: float = 0.0
    blocked_rate: float = 0.0
    empty_rate: float = 0.0
    captcha_rate: float = 0.0
    timeout_rate: float = 0.0
    pdf_rate: float = 0.0
    failed_rate: float = 0.0
    avg_latency: float = 0.0
    p95_latency: float = 0.0
    avg_content_length: float = 0.0

    _FIELDS: ClassVar[MetricFieldSpec] = (
        ("total_requests", "Total requests", "{}"),
        ("success_rate", "Success rate", "{:.2%}"),
        ("failed_rate", "Failed rate", "{:.2%}"),
        ("blocked_rate", "Blocked rate", "{:.2%}"),
        ("empty_rate", "Empty rate", "{:.2%}"),
        ("captcha_rate", "Captcha rate", "{:.2%}"),
        ("timeout_rate", "Timeout rate", "{:.2%}"),
        ("pdf_rate", "PDF rate", "{:.2%}"),
        ("avg_latency", "Avg latency", "{:.2f}s"),
        ("p95_latency", "P95 latency", "{:.2f}s"),
        ("avg_content_length", "Avg content length", "{:.2f}")
    )

    def _should_include(self, field: str, value: Any) -> bool:
        if field == "total_requests":
            return True
        return value not in (None, 0, 0.0)

    def _format(self, sep: str = "\n") -> str:
        lines = []

        for field, label, fmt in self._FIELDS:
            value = getattr(self, field, None)

            if not self._should_include(field, value):
                continue

            try:
                formatted = fmt.format(value)
            except Exception:
                formatted = str(value)

            lines.append(f"{label}: {formatted}")

        return sep.join(lines)

    def __str__(self) -> str:
        return self._format()

    def to_log(self) -> str:
        return self._format(sep=" | ")

    def to_dict(self, exclude_zero: bool = False) -> Dict[str, Any]:
        data = asdict(self)
        if exclude_zero:
            data = {
                k: v
                for k, v in data.items()
                if not (isinstance(v, (int, float)) and v == 0)
            }
        return data
