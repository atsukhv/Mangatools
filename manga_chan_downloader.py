import asyncio
from pathlib import Path

from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

from browser import init_browser


def file_exists(filename: str, existing_files: set) -> bool:
    """Проверяет, существует ли файл в папке."""
    return filename in existing_files


async def download_files(page, links, save_folder: Path):
    save_folder.mkdir(parents=True, exist_ok=True)
    existing_files = set(f.name for f in save_folder.iterdir() if f.is_file())

    with Progress(
            TextColumn("[bold blue]{task.fields[filename]}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
    ) as progress:

        task = progress.add_task("Скачивание файлов", total=len(links), filename="")

        for i, link in enumerate(links, 1):
            try:
                filename = await link.inner_text()
                progress.update(task, filename=f"[{i}/{len(links)}] {filename}")

                if file_exists(filename, existing_files):
                    progress.update(task, advance=1)
                    continue

                async with page.expect_download() as download_info:
                    await link.click()

                download = await download_info.value
                path = save_folder / filename
                await download.save_as(path)
                existing_files.add(filename)

                progress.update(task, advance=1)

            except Exception as e:
                print(f"[{i}/{len(links)}] ❌ Ошибка с файлом {filename}: {e}")
                progress.update(task, advance=1)


async def download_all_manga(manga_page_url: str, save_folder: Path):
    """
    Получает ссылку на страницу манги, переделывает её в ссылку на скачивание,
    и скачивает все файлы в указанную папку.
    """
    # Преобразуем ссылку на /download/
    if "/manga/" in manga_page_url:
        download_url = manga_page_url.replace("/manga/", "/download/")
    else:
        download_url = manga_page_url

    save_folder = Path(save_folder)
    save_folder.mkdir(parents=True, exist_ok=True)

    async with init_browser(download_url, headless=False) as page:
        await page.goto(download_url, wait_until="networkidle")

        links = await page.locator('a[href*="engine/download.php?id="]').all()
        print(f"Найдено ссылок: {len(links)}")

        await download_files(page, links, save_folder)


if __name__ == "__main__":
    # ссылка на мангу (можно передавать динамически)
    manga_page = "https://im.manga-chan.me/manga/4093-vagabond.html"
    folder = r"D:\Библиотека kindle\Загрузки"

    asyncio.run(download_all_manga(manga_page, folder))
