import asyncio
from contextlib import asynccontextmanager
from typing import Literal

from playwright.async_api import async_playwright

WaitUntil = Literal["commit", "domcontentloaded", "load", "networkidle"]


@asynccontextmanager
async def init_browser(url: str,
                       headless: bool = False,
                       force_lang: bool = True,
                       wait_until: WaitUntil = 'networkidle'
                       ):
    """Контекстный менеджер, который инициализирует playwright, браузер и страницу."""

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/121.0.0.0 Safari/537.36",
            locale="en-GB" if force_lang else "auto",
            java_script_enabled=True,
            bypass_csp=True
        )
        page = await context.new_page()
        await page.set_extra_http_headers({
            "Accept-Language": "en-GB,en;q=0.9",
            "DNT": "1"
        })

        await page.goto(url, wait_until=wait_until, timeout=15000)
        try:
            yield page
        finally:
            await browser.close()


async def scroll_page(page, scrollbar=None):
    """Прокручивает страницу, чтобы подгрузить больше игр."""
    if scrollbar is None:
        for _ in range(3):
            await page.mouse.wheel(0, 500)
            await asyncio.sleep(1)
    else:
        box = await scrollbar.bounding_box()

        if box:
            thumb_x = box["x"] + box["width"] / 2
            thumb_y_start = box["y"] + box["height"] / 2
            thumb_y_end = thumb_y_start + 50

            await page.mouse.move(thumb_x, thumb_y_start)
            await page.mouse.down()
            await page.mouse.move(thumb_x, thumb_y_end, steps=25)
            await page.mouse.up()
            await asyncio.sleep(1)
