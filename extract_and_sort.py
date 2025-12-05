import json
import re
import zipfile
from pathlib import Path

from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn


# ---------- ЗАГРУЗКА НАЗВАНИЙ (НЕОБЯЗАТЕЛЬНАЯ) ----------

def load_chapters(json_path: Path | None) -> dict:
    """Загружает JSON с информацией о главах, если он существует."""
    if not json_path or not json_path.exists():
        return {}

    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


# ---------- ПАРСИНГ ИМЕНИ ФАЙЛА ----------

def parse_filename(file_name: str) -> tuple[int, str] | None:
    """
    Универсально извлекает номер тома и главы из имени архива.
    Пример: solanin_v1_ch10.zip → (1, "10")
    """
    pattern = re.compile(
        r".+?_v(\d+)_ch(\d+)(?:_.*)?\.zip$",
        re.IGNORECASE
    )

    match = pattern.match(file_name)
    if not match:
        return None

    return int(match.group(1)), match.group(2)


# ---------- ПОЛУЧЕНИЕ НАЗВАНИЯ ГЛАВЫ ----------

def get_chapter_title(chapters_json: dict, volume_num: int, chapter_num: str) -> str:
    """
    Получает название главы из JSON.
    Если данных нет — возвращает номер главы.
    """
    volume_key = f"Volume {volume_num}"

    for chap in chapters_json.get(volume_key, []):
        if chap.get("Chapter") == chapter_num:
            return chap.get("Title", chapter_num)

    return chapter_num  # fallback


# ---------- СОЗДАНИЕ ПАПОК ----------

def create_chapter_folder(
    output_folder: Path,
    volume_num: int,
    chapter_num: str,
    title: str
) -> Path:
    """
    Создаёт безопасную папку для главы, совместимую с Windows.
    """

    volume_folder = output_folder / f"Том {volume_num}"
    volume_folder.mkdir(parents=True, exist_ok=True)

    # --- ЖЁСТКАЯ ЗАЩИТА ИМЕНИ ПАПКИ ---
    safe_title = title.strip()

    if not safe_title:
        safe_title = f"Chapter {chapter_num}"

    # удаляем запрещённые символы Windows
    safe_title = re.sub(r'[<>:"/\\|?*]', "_", safe_title)

    # убираем точку и пробел в конце
    safe_title = safe_title.rstrip(" .")

    chapter_folder = volume_folder / f"{chapter_num}. {safe_title}"
    chapter_folder.mkdir(parents=True, exist_ok=True)

    return chapter_folder



# ---------- РАСПАКОВКА ----------

def extract_file(file_path: Path, chapter_folder: Path):
    """Распаковывает zip-архив в указанную папку."""
    if file_path.suffix.lower() != ".zip":
        return

    try:
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(chapter_folder)
    except zipfile.BadZipFile:
        print(f"❌ Битый архив: {file_path.name}")


# ---------- ОСНОВНАЯ СОРТИРОВКА ----------

def sort_manga(source_folder: Path, output_folder: Path, names_json: Path | None = None):
    """
    Универсальная сортировка манги:
    - работает с любой мангой
    - поддерживает names.json, но не требует его
    """

    output_folder.mkdir(parents=True, exist_ok=True)
    files = [f for f in source_folder.iterdir() if f.is_file()]

    chapters_json = load_chapters(names_json)

    with Progress(
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
    ) as progress:

        task = progress.add_task("Сортировка манги", total=len(files))

        for file in files:
            parsed = parse_filename(file.name)

            if not parsed:
                progress.update(task, advance=1)
                continue

            volume_num, chapter_num = parsed
            title = get_chapter_title(chapters_json, volume_num, chapter_num)

            chapter_folder = create_chapter_folder(
                output_folder,
                volume_num,
                chapter_num,
                title
            )

            extract_file(file, chapter_folder)
            progress.update(task, advance=1)


# ---------- ЗАПУСК ----------

if __name__ == "__main__":
    SOURCE_FOLDER = Path(r"D:\Библиотека kindle\Загрузки")
    OUTPUT_FOLDER = Path(r"D:\Библиотека kindle\Загрузки")

    NAMES_JSON = Path("names.json")  # можно удалить вообще

    sort_manga(SOURCE_FOLDER, OUTPUT_FOLDER, NAMES_JSON)
