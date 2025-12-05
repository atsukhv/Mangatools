import asyncio
from pathlib import Path

from cleanup import clean_and_convert
from extract_and_sort import sort_manga
from manga_chan_downloader import download_all_manga as mc_downloader
from fetch_chapters_name import get_chapters_name

PATTERNS_FILE = Path("files_to_delete.txt")
files_to_delete_patterns = [
    line.strip() for line in PATTERNS_FILE.read_text(encoding="utf-8").splitlines() if line.strip()
]

async def main(url: str, source_folder: Path, output_folder: Path, files_to_delete_patterns: list[str]):
    print("Начало загрузки")
    await mc_downloader(url, source_folder)
    await get_chapters_name(url)
    await sort_manga(source_folder, output_folder)
    await clean_and_convert(output_folder, files_to_delete_patterns)



if __name__ == "__main__":
    url = "https://im.manga-chan.me/manga/3624-solanin.html"
    source_folder = Path(r"D:\Библиотека kindle\Загрузки")
    output_folder = Path(r"D:\Библиотека kindle\Загрузки")

    asyncio.run(main(url, source_folder, output_folder, files_to_delete_patterns))