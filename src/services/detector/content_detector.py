# ./src/services/detector/content_detector.py
from .deps import ScrapeStatus
from .rule import Rule, Rules, KeyWords


class ContentDetector:
    # ===== CONSTANTS =====
    EMPTY_THRESHOLD: int = 100
    rules: Rules = (
        Rule(
            status=ScrapeStatus.CAPTCHA,
            keywords=(
                "captcha",
                "verify you are human",
                "i am not a robot",
                "cloudflare",
                "recaptcha"
            )
        ),
        Rule(
            status=ScrapeStatus.BLOCKED,
            keywords=(
                "access denied",
                "forbidden",
                "blocked",
                "403",
                "request blocked"
            )
        ),
        Rule(
            status=ScrapeStatus.PDF,
            keywords=("%pdf-", "application/pdf")
        )
    )

    # ===== PUBLIC =====
    def detect(self, content: str, snapshot_size: int = 3000) -> ScrapeStatus:
        if self._is_empty(content):
            return ScrapeStatus.EMPTY
        snapshot: str = content[:snapshot_size].lower()
        for rule in self.rules:
            if self._match(rule.keywords, snapshot):
                return rule.status
        return ScrapeStatus.SUCCESS

    # ===== RULE ENGINE =====
    def _match(self, keywords: KeyWords, content: str) -> bool:
        return any(keyword in content for keyword in keywords)

    def _is_empty(self, content: str) -> bool:
        if not content:
            return True
        return len(content.strip()) < self.EMPTY_THRESHOLD
