from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TaskID
from typing import Optional

progress: Optional[Progress] = None
current_task: Optional[TaskID] = None

def init_progress():
    """Инициализация глобального прогресс-бара"""
    global progress
    progress = Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn()
    )
    progress.start()
    return progress

def add_task(description: str, total: int):
    """Добавляет задачу в прогресс-бар"""
    global current_task
    if progress is None:
        raise RuntimeError("Progress not initialized. Call init_progress() first.")
    current_task = progress.add_task(description, total=total)
    return current_task

def advance_task(steps: int = 1):
    """Продвигает текущую задачу"""
    if progress is None or current_task is None:
        raise RuntimeError("No active task.")
    progress.update(current_task, advance=steps)

def stop_progress():
    """Останавливает прогресс-бар"""
    if progress:
        progress.stop()


def create_progress(total: int) -> tuple[Progress, int]:
    progress = Progress(
        TextColumn("[bold blue]{task.fields[filename]}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
    )
    task_id = progress.add_task(
        "Скачивание файлов",
        total=total,
        filename=""
    )
    return progress, task_id


def update_progress_filename(progress: Progress, task_id: int,index: int,total: int,filename: str):
    progress.update(task_id, filename=f"[{index}/{total}] {filename}")

def advance_progress(progress: Progress, task_id: int):
    progress.update(task_id, advance=1)