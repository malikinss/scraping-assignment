# ./src/scrapers/browser_scraper.py
from .deps import (
    Page,
    TimeoutError,
    settings,
    ScrapeResult,
    CTX,
    URL,
    ResultBuilder,
    logger,
    Content,
    METHOD,
)

from .browser_client import BrowserClient
from .browser_context import BrowserPageContext


class BrowserScraper:
    def __init__(self) -> None:
        self.timeout: float = settings.browser.timeout
        self._client: BrowserClient = BrowserClient()
        self._page_context: BrowserPageContext = BrowserPageContext(
            self._client)

    # ===== LIFECYCLE =====
    async def __aenter__(self) -> "BrowserScraper":
        await self._client.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        await self._client.close()
        return False

    # ===== CORE =====
    async def fetch(self, id: int, url: URL) -> ScrapeResult:
        ctx: CTX = CTX(id=id, method=METHOD, url=url, timeout=self.timeout)
        builder: ResultBuilder = ResultBuilder()
        logger.scraper.start(ctx)

        try:
            async with self._page_context.page() as page:
                content: Content = await self._get_content(ctx, page)

            if content is None:
                return builder.empty(ctx)

            return builder.process(ctx, content)

        except TimeoutError:
            return builder.timeout(ctx)

        except Exception as e:
            return builder.failure(ctx, str(e))

    # ===== PAGE PROCESSING =====
    async def _get_content(self, ctx: CTX, page: Page) -> Content:
        try:
            await page.goto(ctx.url, timeout=ctx.timeout)
            await page.wait_for_load_state(settings.browser.state)
            await self._smart_wait(page)
            content: Content = await page.content()
            length: int = len(content) if content else 0
            msg: str = f"CONTENT_LOADED length={length}"
            logger.scraper.event(ctx, msg, "debug")
            return content

        except TimeoutError:
            logger.scraper.timeout(ctx)
            return None
        except Exception as e:
            logger.scraper.request_error(ctx, str(e))
            return None

    async def _smart_wait(self, page: Page) -> None:
        delay: float = max(300, min(self.timeout // 2, 2000))
        await page.wait_for_timeout(delay)
