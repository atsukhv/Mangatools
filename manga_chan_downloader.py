import asyncio
from pathlib import Path

from browser import init_browser
from progress import create_progress, update_progress_filename, advance_progress


def file_exists(filename: str, existing_files: set) -> bool:
    """Проверяет, существует ли файл в папке."""
    return filename in existing_files


async def validate_download_url(manga_page_url):
    """Валидирует ссылку"""
    if "/manga/" in manga_page_url:
        valid_url = manga_page_url.replace("/manga/", "/download/")
    else:
        valid_url = manga_page_url

    return valid_url


async def len_links(url: str) -> int:
    """Считает количество ссылок на скачивание, ничего не сохраняя."""
    async with init_browser(url, headless=True) as page:
        await page.goto(url, wait_until="networkidle")
        locator = page.locator('a[href*="engine/download.php?id="]')
        count = await locator.count()
        print(f"Найдено ссылок: {count}")
        return count


def generate_chapter_list(start_chapter: int | None, end_chapter: int | None, total_chapters: int,
                          skip_chapters=None) -> list[int]:
    """Генерирует список глав для скачивания с учётом исключений.

    Если start_chapter=None → берём с 1
    Если end_chapter=None → берём до total_chapters
    """
    if skip_chapters is None:
        skip_chapters = set()
    else:
        skip_chapters = set(skip_chapters)

    if start_chapter is None:
        start_chapter = 1
    if end_chapter is None:
        end_chapter = total_chapters

    chapters = [i for i in range(start_chapter, end_chapter + 1) if i not in skip_chapters]
    return chapters


def prepare_environment(save_folder: Path) -> set[str]:
    save_folder.mkdir(parents=True, exist_ok=True)
    return {f.name for f in save_folder.iterdir() if f.is_file()}


async def pars_links(page):
    """Возвращает Locator всех подходящих ссылок на странице в порядке от первой до последней главы."""
    original_links = page.locator('a[href*="engine/download.php?id="]')
    count = await original_links.count()

    links = []
    for i in range(count):
        links.insert(0, original_links.nth(i))
    return links


async def download_files(save_folder: Path, url: str, start_chapter, end_chapter, skip_chapters):
    """Скачивает только указанные главы."""
    existing_files = prepare_environment(save_folder)

    async with init_browser(url, headless=False) as page:
        await page.goto(url, wait_until="networkidle")

        links = await pars_links(page)
        total_links = len(links)
        print(f"Общее количество глав: {total_links}")

        chapters_to_download = generate_chapter_list(start_chapter, end_chapter,
                                                     total_links, skip_chapters)

        # фильтруем ссылки по списку глав
        filtered = [(idx, link) for idx, link in enumerate(links, 1) if idx in chapters_to_download]

        progress, task_id = create_progress(len(filtered))

        with progress:
            for chapter_number, link in filtered:
                try:
                    filename = await link.inner_text()
                    update_progress_filename(progress, task_id, chapter_number, len(filtered), filename)

                    if filename in existing_files:
                        continue

                    await download_one_file(page, link, save_folder, existing_files)

                except Exception as e:
                    print(f"[Глава {chapter_number}] ❌ Ошибка: {e}")

                finally:
                    advance_progress(progress, task_id)



async def download_one_file(page, link, save_folder: Path, existing_files: set[str]) -> str | None:
    filename = await link.inner_text()
    href = await link.get_attribute("href")

    if filename in existing_files:
        return None

    async with page.expect_download() as download_info:
        await link.click()

    download = await download_info.value
    await download.save_as(save_folder / filename)

    existing_files.add(filename)
    return filename


async def manga_downloader_main(manga_page_url: str, save_folder: Path,
                                start_chapter=None, end_chapter=None, skip_chapters=None):
    """Главная функция."""
    page_url = await validate_download_url(manga_page_url)
    await download_files(save_folder, page_url, start_chapter, end_chapter, skip_chapters)


if __name__ == "__main__":
    manga_page = "https://im.manga-chan.me/manga/105000-chainsaw-man.html"
    folder = Path(r"D:\Библиотека kindle\Загрузки")

    asyncio.run(manga_downloader_main(manga_page, folder))
