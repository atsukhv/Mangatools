import asyncio
import os
import platform
import re
from pathlib import Path

from loguru import logger

from browser import init_browser
from gui.overlay import OverlayManager
from progress import create_progress, update_progress_filename, advance_progress


def file_exists(filename: str, existing_files: set) -> bool:
    """Проверяет, существует ли файл в папке."""
    return filename in existing_files


async def validate_url_for_download(manga_page_url):
    """Валидирует ссылку"""
    if "/manga/" in manga_page_url:
        return manga_page_url.replace("/manga/", "/download/")
    return manga_page_url


async def validate_download_url_for_info(manga_page_url: str) -> str:
    """Возвращает URL на /manga/ страницу для получения информации"""
    if "/download/" in manga_page_url:
        return manga_page_url.replace("/download/", "/manga/")
    return manga_page_url


async def len_links(url: str) -> tuple[int, str]:
    """
    Считает количество ссылок на скачивание (глав) и возвращает название манги.
    Возвращает кортеж: (count_links, manga_name)
    """
    info_url = await validate_download_url_for_info(url)
    async with init_browser(info_url, headless=True) as page:
        await page.goto(info_url, wait_until="networkidle")
        manga_name = await locate_name(page)

        try:
            item_locator = page.locator('td.item2 h2 b').first
            await item_locator.wait_for(state="visible", timeout=5000)
            text = await item_locator.inner_text()
            match = re.search(r'(\d+)', text)
            count = int(match.group(1)) if match else 0
        except Exception:
            logger.error("Не удалось найти количество глав")
            count = 0

        logger.info(f"Название: {manga_name}, Глав: {count}")
        return count, manga_name


async def locate_name(page) -> str:
    """Берёт текст из <a class='title_top_a'> и убирает скобки с содержимым"""
    try:
        locator = page.locator("a.title_top_a").first
        await locator.wait_for(state="visible", timeout=5000)
        name = (await locator.inner_text()).strip()
        # Убираем всё в скобках, включая сами скобки
        name = re.sub(r'\s*\(.*?\)\s*', '', name)
        return name
    except Exception:
        logger.error("Имя манги не найдено")
        return "Неизвестно"


def get_download_folder(subfolder: str = "MangaDownloads") -> str:
    """
    Возвращает путь к папке загрузки пользователя с дополнительной подпапкой.
    Если папка не существует — создаёт её.

    :param subfolder: название подпапки внутри стандартной папки "Загрузки"
    :return: абсолютный путь к папке загрузки
    """
    system = platform.system()

    if system == "Windows":
        download_path = Path(os.path.join(os.environ.get("USERPROFILE", ""), "Downloads"))
    elif system == "Darwin":  # macOS
        download_path = Path.home() / "Downloads"
    else:  # Linux и прочие
        download_path = Path.home() / "Загрузки"
        if not download_path.exists():  # иногда в Linux может быть "Downloads"
            download_path = Path.home() / "Downloads"

    final_path = download_path / subfolder
    final_path.mkdir(parents=True, exist_ok=True)

    return str(final_path)


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
        logger.info(f"Общее количество глав: {total_links}")

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
                    logger.info(f"[Глава {chapter_number}] ❌ Ошибка: {e}")

                finally:
                    advance_progress(progress, task_id)


async def download_one_file(page, link, save_folder: Path, existing_files: set[str]) -> str | None:
    filename = await link.inner_text()
    if filename in existing_files:
        return None

    async with page.expect_download() as download_info:
        await link.click()

    download = await download_info.value
    await download.save_as(save_folder / filename)

    existing_files.add(filename)
    return filename


async def download_files_with_overlay(save_folder: Path, url: str, start_chapter, end_chapter, skip_chapters,
                                      overlay: OverlayManager):
    """Скачивает главы и обновляет прогресс бар в OverlayManager."""
    try:
        url = await validate_url_for_download(url)
        existing_files = await prepare_environment(save_folder)

        async with init_browser(url, headless=False) as page:
            links = await pars_links(page)
            total_links = len(links)
            logger.info(f"Найдено {total_links} глав")

            chapters_to_download = generate_chapter_list(start_chapter, end_chapter, total_links, skip_chapters)
            filtered = [(idx, link) for idx, link in enumerate(links, 1) if idx in chapters_to_download]

            total_to_download = len(filtered)
            logger.info(f"К загрузке: {total_to_download} глав")

            overlay.app.after(0, lambda: overlay.show("Подготовка к скачиванию..."))
            overlay.app.after(0, lambda: overlay.progress.set(0))

            for i, (chapter_number, link) in enumerate(filtered, start=1):
                if overlay._finished:
                    logger.info("Загрузка остановлена пользователем")
                    break

                overlay.app.after(0, lambda c=chapter_number, t=total_to_download:
                overlay.status_label.configure(text=f"Глава {c}/{t}\nКачается..."))

                try:
                    filename = await link.inner_text()
                    if filename in existing_files:
                        continue

                    async with page.expect_download() as download_info:
                        await link.click()
                    download = await download_info.value
                    await download.save_as(save_folder / filename)

                    existing_files.add(filename)
                    logger.info(f"[Глава {chapter_number}] ✓ {filename}")

                except Exception as e:
                    logger.error(f"[Глава {chapter_number}] ❌ {e}")

                finally:
                    overlay.app.after(0, lambda idx=i, total=total_to_download: overlay.progress.set(idx / total))

            overlay.app.after(0, lambda: overlay.finish(total_to_download))
            logger.info("Загрузка завершена")

    except Exception as e:
        logger.error(f"Ошибка при скачивании: {e}")
        overlay.app.after(0, lambda: overlay.finish(0))
        raise


async def manga_downloader_main(manga_page_url: str, save_folder: Path,
                                start_chapter=None, end_chapter=None, skip_chapters=None):
    """Главная функция."""
    page_url = await validate_url_for_download(manga_page_url)
    await download_files(save_folder, page_url, start_chapter, end_chapter, skip_chapters)


if __name__ == "__main__":
    manga_page = "https://im.manga-chan.me/manga/105000-chainsaw-man.html"
    folder = Path(r"D:\Библиотека kindle\Загрузки")

    asyncio.run(manga_downloader_main(manga_page, folder))
