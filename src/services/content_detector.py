# ./src/services/content_detector.py

from src.models.enums import ScrapeStatus


class ContentDetector:
    def detect(self, content: str) -> ScrapeStatus:
        if not content or self._is_empty(content):
            return ScrapeStatus.EMPTY

        if self._is_captcha(content):
            return ScrapeStatus.CAPTCHA

        if self._is_blocked(content):
            return ScrapeStatus.BLOCKED

        return ScrapeStatus.SUCCESS

    def _is_empty(self, content: str) -> bool:
        return len(content.strip()) < 100

    def _is_captcha(self, content: str) -> bool:
        keywords = [
            "captcha",
            "verify you are human",
            "i am not a robot",
            "cloudflare",
            "recaptcha"
        ]

        return self._contains_keywords(keywords, content)

    def _is_blocked(self, content: str) -> bool:
        keywords = [
            "access denied",
            "forbidden",
            "blocked",
            "403",
            "request blocked"
        ]

        return self._contains_keywords(keywords, content)

    def _contains_keywords(self, keywords: list[str], content: str) -> bool:
        content_lower = content.lower()

        for keyword in keywords:
            if keyword in content_lower:
                # print(f"Found keyword: {keyword}")
                return True

        return False


detector = ContentDetector()
