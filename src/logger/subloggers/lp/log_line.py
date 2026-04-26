# ./src/logger/subloggers/lp/log_line.py
from .deps import Optional, URLUtils


class LogLine:
    def __init__(self):
        self._parts: list[str] = []

    # ===== HELPER =====
    def add(self, value: str) -> "LogLine":
        self._parts.append(value)
        return self

    # ===== PRIMITIVES =====
    def kv(self, key: str, value) -> "LogLine":
        return self.add(f"{key}={value}")

    def bracket(self, text: str) -> "LogLine":
        return self.add(f"[{text}]")

    def item(self, text: str) -> "LogLine":
        return self.add(f"[{text.upper()}]")

    def text(self, value: str) -> "LogLine":
        return self.add(value)

    # ===== TYPED FIELDS =====
    def id(self, id: int) -> "LogLine":
        return self.add(f"[ID:{id}]")

    def method(self, method) -> "LogLine":
        return self.item(str(method))

    def status(self, status) -> "LogLine":
        return self.item(str(status))

    def url(self, url) -> "LogLine":
        return self.kv("url", URLUtils.short_url(url))

    def attempt(
        self,
        attempt: Optional[int],
        retries: Optional[int]
    ) -> "LogLine":
        return (
            self.add(f"(attempt {attempt}/{retries})")
            if attempt is not None
            else self
        )

    # ===== FORMATTED VALUES =====
    def seconds(self, key: str, value: float) -> "LogLine":
        return self.kv(key, f"{value:.3f}s")

    def ms(self, key: str, value: float) -> "LogLine":
        return self.kv(key, f"{value:.0f}ms")

    def error(self, error: Optional[str]) -> "LogLine":
        return self.kv("error", error or "N/A")

    # ===== COMPOSITES =====
    def prefix(self, id: int, method, url, timeout: float) -> "LogLine":
        return (
            self.id(id).method(method).url(url).seconds("timeout", timeout)
        )

    def terminated(self, reason: str) -> "LogLine":
        return self.text(f"Pipeline terminated: {reason}")

    # ===== BUILD =====
    def build(self, sep: str = " ") -> str:
        return sep.join(self._parts)

    def __str__(self) -> str:
        return self.build()
