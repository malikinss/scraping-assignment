# ./src/utils/url_utils.py
from .deps import urlparse, URL, NamedTuple


class ParsedURL(NamedTuple):
    scheme: str
    netloc: str
    path: str


class URLUtils:

    # ===== CORE =====
    @staticmethod
    def parse(url: URL) -> ParsedURL:
        p = urlparse(url)
        return ParsedURL(
            scheme=p.scheme,
            netloc=p.netloc,
            path=p.path
        )

    # ===== PUBLIC API =====
    @classmethod
    def is_pdf(cls, url: URL) -> bool:
        parsed = cls.parse(url)
        return parsed.path.lower().endswith(".pdf")

    @classmethod
    def get_domain(cls, url: URL, strip_www: bool = True) -> str:
        parsed = cls.parse(url)
        netloc = parsed.netloc
        if strip_www and netloc.startswith("www."):
            return netloc[4:]
        return netloc

    @staticmethod
    def short_url(url: URL, max_length: int = 50) -> str:
        if len(url) <= max_length:
            return url
        return f"{url[: max_length - 3]}..."

    @classmethod
    def get_path(cls, url: URL) -> str:
        parsed = cls.parse(url)
        return parsed.path

    @classmethod
    def is_valid(cls, url: URL) -> bool:
        if not url or " " in url:
            return False
        parsed = cls.parse(url)
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
        )
