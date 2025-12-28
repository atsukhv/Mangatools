import flet as ft
from tkinter import Tk, filedialog
from pathlib import Path


def pick_directory():
    root = Tk()
    root.withdraw()
    return filedialog.askdirectory()


def main(page: ft.Page):
    page.title = "Manga on Kindle tool"
    page.window_width = 900
    page.window_height = 650
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.bgcolor = ft.Colors.BLACK

    ACCENT = ft.Colors.ORANGE
    CARD_BG = ft.Colors.GREY_800
    SUBTEXT = ft.Colors.GREY_300

    selected_folder: Path | None = None

    status_text = ft.Text("Что тут происходит", size=13, color=SUBTEXT)
    progress = ft.ProgressBar(value=0)

    def set_status(text: str, value: float | None = None):
        status_text.value = text
        if value is not None:
            progress.value = value
        page.update()

    def choose_folder(e):
        nonlocal selected_folder
        path = pick_directory()
        if path:
            selected_folder = Path(path)
            folder_label.value = f"Папка: {selected_folder}"
            set_status("Папка выбрана", 0.1)

    # ===== UI =====

    title = ft.Text(
        "Manga on Kindle tool",
        size=42,
        weight=ft.FontWeight.BOLD,
        color=ACCENT,
        font_family="Georgia",
    )

    desc = ft.Text(
        "Вставьте ссылку на мангу с сайта manga-chan – https://im.manga-chan.me/",
        color=SUBTEXT,
        size=14,
    )

    url_input = ft.TextField(
        hint_text="https://im.manga-chan.me/...",
        filled=True,
        bgcolor=ft.Colors.GREY_700,
        border_radius=12,
        height=54,
        text_size=15,
    )

    folder_btn = ft.ElevatedButton(
        "Выбрать папку для загрузки",
        bgcolor=ACCENT,
        color=ft.Colors.BLACK,
        height=50,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=24)
        ),
        on_click=choose_folder,
    )

    folder_label = ft.Text(
        "Папка не выбрана",
        size=13,
        color=SUBTEXT,
    )

    info_text = ft.Text(
        "После загрузки посмотрите есть ли какие либо паттерны мусорных файлов,\n"
        "которые вы хотели бы удалить, например обложки или доп. рисунки.\n"
        "Выпишите названия этих файлов в конфиг и на следующем этапе они будут\n"
        "удалены из всех томов и глав.",
        color=SUBTEXT,
        size=14,
    )

    config_btn = ft.ElevatedButton(
        "Открыть конфиг",
        bgcolor=ACCENT,
        color=ft.Colors.BLACK,
        height=48,
        width=260,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=22)
        ),
    )

    sort_btn = ft.ElevatedButton(
        "Запустить сортировку файлов",
        bgcolor=ACCENT,
        color=ft.Colors.BLACK,
        height=48,
        width=320,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=22)
        ),
        on_click=lambda e: set_status("Готово", 1.0),
    )

    card = ft.Container(
        width=720,
        padding=40,
        bgcolor=CARD_BG,
        border_radius=20,
        content=ft.Column(
            [
                title,
                desc,
                url_input,
                folder_btn,
                folder_label,
                info_text,
                ft.Row(
                    [config_btn, sort_btn],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Column(
                    [
                        progress,
                        status_text,
                    ],
                    spacing=6,
                ),
            ],
            spacing=26,
        ),
    )

    page.add(
        ft.Row(
            [card],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
    )


ft.run(main)
