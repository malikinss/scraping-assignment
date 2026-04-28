# ./src/scrapers/http/http_client.py

from .deps import httpx, settings, Client


class HTTPXClient:
    def __init__(self):
        self.client: Client = None

    async def start(self):
        if not self.client:
            self.client = self._build_client()

    async def close(self):
        if self.client:
            await self.client.aclose()
            self.client = None

    def _build_client(self) -> Client:
        return httpx.AsyncClient(
            timeout=settings.httpx.timeout,
            headers={
                "User-Agent": settings.user_agent.user_agent,
                "Accept-Language": settings.user_agent.languages,
            },
            proxy=settings.httpx.proxy,
            follow_redirects=settings.httpx.redirects,
            limits=httpx.Limits(
                max_connections=settings.httpx.connections,
                max_keepalive_connections=settings.httpx.keepalive
            )
        )
