import json
import re
import zipfile
from pathlib import Path

from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn


def load_chapters(json_path: str) -> dict:
    """Загружает JSON с информацией о томах и главах."""
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def parse_filename(file_name: str) -> tuple[int, str] | None:
    """Извлекает номер тома и главы из имени файла."""
    FILENAME_PATTERN = re.compile(r"berserk_v(\d+)_ch(\d+)(?:_.*)?\.zip$", re.IGNORECASE)
    match = FILENAME_PATTERN.match(file_name)
    if not match:
        return None
    return int(match.group(1)), match.group(2)


def get_chapter_title(chapters_json: dict, volume_num: int, chapter_num: str) -> str:
    """Получает название главы из JSON по номеру тома и главы."""
    volume_key = f"Volume {volume_num}"
    for chap in chapters_json.get(volume_key, []):
        if chap["Chapter"] == chapter_num:
            return chap["Title"]
    return "Unknown"


def create_chapter_folder(output_folder: Path, volume_num: int, chapter_num: str, title: str) -> Path:
    """Создаёт папку для главы."""
    volume_folder = output_folder / f"Berserk - Том {volume_num}"
    volume_folder.mkdir(exist_ok=True)
    chapter_folder = volume_folder / f"{chapter_num}. {title}"
    chapter_folder.mkdir(exist_ok=True)
    return chapter_folder


def extract_file(file_path: Path, chapter_folder: Path):
    """Распаковывает архив в указанную папку."""
    if file_path.suffix.lower() == ".zip":
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(chapter_folder)
        except zipfile.BadZipFile:
            print(f"Ошибка при распаковке: {file_path.name}")
    elif file_path.suffix.lower() in [".rar", ".7z"]:
        print(f"Поддержка {file_path.suffix} пока не реализована: {file_path.name}")
    else:
        print(f"Неизвестный формат: {file_path.name}")


def sort_manga(source_folder: Path, output_folder: Path):
    """Проходит по всем файлам в папке, создаёт папки по томам/главам и распаковывает архивы с прогресс-баром."""

    output_folder.mkdir(parents=True, exist_ok=True)
    files = [f for f in source_folder.iterdir() if f.is_file()]

    chapters_json = load_chapters("names.json")

    with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
    ) as progress:

        task = progress.add_task("Сортировка манги", total=len(files))

        for file in files:
            parsed = parse_filename(file.name)
            if not parsed:
                print(f"Пропущен файл: {file.name}")
                progress.update(task, advance=1)
                continue

            volume_num, chapter_num = parsed
            title = get_chapter_title(chapters_json, volume_num, chapter_num)
            chapter_folder = create_chapter_folder(output_folder, volume_num, chapter_num, title)
            extract_file(file, chapter_folder)
            progress.update(task, advance=1)


if __name__ == "__main__":
    SOURCE_FOLDER = Path(r"D:\Библиотека kindle\Загрузки")
    OUTPUT_FOLDER = Path(r"D:\Библиотека kindle\Загрузки\Berserk_Sorted_2")

    sort_manga(SOURCE_FOLDER, OUTPUT_FOLDER)
