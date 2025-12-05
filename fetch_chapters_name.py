import asyncio
import json
import re

from browser import init_browser

OUTPUT_FILE = "names.json"


def clean_title(title: str) -> str:
    """
    Очищает название главы от даты и лишних пробелов.

    Преобразует, например:
        "Золотой век IV 2020-09-12" → "Золотой век IV"

    :param title: исходное название главы
    :return: очищенное название
    """
    title = re.sub(r"\d{4}-\d{2}-\d{2}", "", title)
    return title.strip()


async def fetch_chapters(page, url):
    """
    Парсит страницу манги и собирает структуру томов и глав.

    Структура результата:
    {
        "Volume 1": [{"Chapter": "0", "Title": "Название"}],
        "Volume 2": [{"Chapter": "1", "Title": "Название"}],
        ...
    }

    :param url: ссылка на страницу манги
    :param page: объект страницы Playwright
    :return: словарь с томами и главами
    """
    await page.goto(url, wait_until="networkidle")
    rows = await page.locator("table tr").all()
    result = {}

    for row in rows:
        text = await row.inner_text()
        if text.strip().startswith("Том"):
            parts = text.split()
            volume = parts[1]
            chapter = parts[3]
            raw_title = " ".join(parts[4:]).strip()
            title = clean_title(raw_title)

            volume_key = f"Volume {volume}"
            if volume_key not in result:
                result[volume_key] = []

            result[volume_key].append({
                "Chapter": chapter,
                "Title": title
            })

    return result


async def get_chapters_name(url):
    """
    Основная функция для получения списка глав и сохранения его в JSON-файл.

    Использует браузер Playwright для получения данных со страницы манги.
    """
    async with init_browser(url) as page:
        chapters = await fetch_chapters(page, url)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chapters, f, ensure_ascii=False, indent=4)

    print(f"Сохранено в {OUTPUT_FILE}")


if __name__ == "__main__":
    asyncio.run(get_chapters_name("https://im.manga-chan.me/manga/3175-berserk.html"))
