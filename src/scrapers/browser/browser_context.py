# ./src/scrapers/browser/browser_context.py

from .deps import (
    AsyncGenerator,
    asynccontextmanager,
    BrowserContext,
    Page,
    settings,
    Optional,
)
from .browser_client import BrowserClient


class BrowserPageContext:
    def __init__(self, client: BrowserClient) -> None:
        self.client = client

    @asynccontextmanager
    async def page(self) -> AsyncGenerator[Page, None]:
        await self.client.ensure()
        context: BrowserContext = await self._create_context()
        page: Page = await context.new_page()
        try:
            yield page
        finally:
            await self._cleanup(page, context)

    async def _create_context(self):
        await self.client.ensure()
        context: BrowserContext = await self.client.browser.new_context(
            user_agent=settings.browser.user_agent,
            locale=settings.browser.locale,
        )
        return context

    async def _cleanup(
        self, page: Optional[Page], context: Optional[BrowserContext]
    ) -> None:
        if page:
            await page.close()
        if context:
            await context.close()
