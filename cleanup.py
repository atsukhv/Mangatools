from pathlib import Path
import imageio.v3 as iio
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn


def clean_files(folder: Path, progress: Progress, files_to_delete_patterns: list[str]):
    """
    Удаляет все файлы из списка files_to_delete_patterns.
    """
    files = [f for f in folder.rglob("*") if f.is_file() and f.name in files_to_delete_patterns]
    task = progress.add_task("Удаление лишних файлов", total=len(files))

    for file in files:
        file.unlink()
        progress.update(task, advance=1)
    progress.remove_task(task)


def convert_avif_to_png(folder: Path, progress: Progress):
    """
    Конвертирует все .avif файлы в .png и удаляет исходники.
    """
    avif_files = list(folder.rglob("*.avif"))
    task = progress.add_task("Конвертация AVIF → PNG", total=len(avif_files))

    for avif_file in avif_files:
        output_png = avif_file.with_suffix(".png")
        try:
            img = iio.imread(avif_file)  # читаем avif
            iio.imwrite(output_png, img)  # сохраняем в png без потерь
            avif_file.unlink()  # удаляем исходник
        except Exception as e:
            print(f"Ошибка при конвертации {avif_file.name}: {e}")
        finally:
            progress.update(task, advance=1)
    progress.remove_task(task)

def clean_and_convert(folder: Path, files_to_delete_patterns: list[str]):
    with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn()
    ) as progress:
        clean_files(folder, progress)
        convert_avif_to_png(folder, progress)

if __name__ == "__main__":
    manga_folder = Path(r"D:\Библиотека kindle\Загрузки\Berserk_Sorted")

    clean_and_convert(manga_folder)