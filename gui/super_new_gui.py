import asyncio
import threading
import tkinter as tk
from pathlib import Path

import customtkinter as ctk
from PIL import Image
from loguru import logger

from gui.buttons_click import choose_folder, get_delete_configs
from gui.overlay import OverlayManager
from manga_chan_downloader import get_download_folder, download_files_with_overlay, len_links

# Настройки
BG = "#2D2D2D"
SECOND_BG = "#64513C"
ACCENT = "#FF8800"
HOVER_COLOR = "#FFA733"
TEXT_COLOR = "#FFFFFF"
FONT_TITLE = ("Georgia", 50, "bold")
FONT_TEXT = ("Arial", 14)


class MangaToolGUI(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = None
        self.name = None
        self.folder = None
        self.overlay = OverlayManager(self)

        # --- Окно ---
        self.title("Manga tool")
        self.geometry("890x500")
        self.resizable(False, False)
        self.configure(fg_color=BG)

        # --- Контейнер ---
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0, sticky="ew", padx=25, pady=25)

        # --- Фреймы ---
        self.header_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))

        self.search_frame = ctk.CTkFrame(self.container,
                                         fg_color="transparent")  # TODO изменить длинну поисковой строки что бы не выходило за пределы других фрэймов
        self.search_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))

        self.folder_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.folder_frame.grid(row=2, column=0, sticky="w", padx=(0, 20))

        self.name_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.name_frame.grid(row=2, column=1, sticky="w", pady=(0, 0))

        self.select_chapters_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.select_chapters_frame.grid(row=3, column=0, sticky="w", pady=(0, 20))

        self.downloads_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.downloads_frame.grid(row=3, column=1, sticky="w", pady=(0, 20))

        self.info_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.info_frame.grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 0))

        self.config_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.config_frame.grid(row=5, column=0, sticky="w", pady=(0, 0))

        self.sorting_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.sorting_frame.grid(row=5, column=1, sticky="w", pady=(0, 20))

        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.grid(row=2, column=0, sticky="ew", pady=(0, 0))

        # --- Заголовок ---
        self.title_label = ctk.CTkLabel(self.header_frame, text="Manga tool", font=FONT_TITLE, text_color=ACCENT)
        self.title_label.grid(row=0, column=0, columnspan=2, sticky="w")

        # --- Поле для ввода ссылки ---
        self.url_entry = ctk.CTkEntry(self.search_frame,
                                      width=707, height=40, corner_radius=0, fg_color=SECOND_BG, border_width=0,
                                      text_color=TEXT_COLOR, font=FONT_TEXT,
                                      placeholder_text="https://im.manga-chan.me/...")
        self.url_entry.grid(row=0, column=0, sticky="ew")

        self.search_btn = ctk.CTkButton(self.search_frame, text="Найти",
                                        width=120, height=40, fg_color=ACCENT, hover_color=HOVER_COLOR,
                                        corner_radius=0, border_width=0, anchor="center",
                                        command=lambda: self.search())
        self.search_btn.grid(row=0, column=1)

        self.url_discription = ctk.CTkLabel(self.search_frame,
                                            text="Вставьте ссылку на мангу с сайта manga-chan - https://im.manga-chan.me/",
                                            font=FONT_TEXT, text_color=TEXT_COLOR)
        self.url_discription.grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 0))

        self.menu = tk.Menu(self.url_entry, tearoff=0)
        self.menu.add_command(label="Вставить", command=lambda: self.paste_from_clipboard(self.url_entry))
        self.url_entry.bind("<KeyPress>", self.on_keypress)
        self.url_entry.bind("<Return>", self.on_enter)
        self.url_entry.bind("<KP_Enter>", self.on_enter)

        # --- Выбор папки ---
        self.folder_icon = ctk.CTkImage(Image.open("icons/folder_icon.png"), size=(20, 21))

        self.folder_discription = ctk.CTkLabel(self.folder_frame, text="Выберите папку для загрузки файлов",
                                               font=FONT_TEXT, text_color=TEXT_COLOR)
        self.folder_discription.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 0))

        # Кнопка слева и поле пути справа
        self.folder_btn = ctk.CTkButton(self.folder_frame, image=self.folder_icon, text="",
                                        width=30, height=30, fg_color=ACCENT, hover_color=HOVER_COLOR,
                                        corner_radius=0, border_width=0, anchor="center",
                                        command=lambda: choose_folder(self.selected_folder_label, self))
        self.folder_btn.grid(row=1, column=0, sticky="w")

        self.selected_folder_label = ctk.CTkLabel(self.folder_frame, text="   По умолчанию выбрана папка: Загрузки",
                                                  width=366, height=30, fg_color=SECOND_BG, text_color=TEXT_COLOR,
                                                  corner_radius=0, anchor="w")
        self.selected_folder_label.grid(row=1, column=1, sticky="w")

        # --- Инструкция ---
        self.info_text = ctk.CTkLabel(
            self.info_frame,
            text="После загрузки посмотрите есть ли какие либо паттерны мусорных файлов, которые вы хотели бы удалить, "
                 "например обложки или доп. рисуноки. Выпишите нзавания этих файлов в конфиг и на следующем этапе они будут "
                 "удалены из всех томов и глав.",
            font=FONT_TEXT, text_color=TEXT_COLOR, wraplength=827, justify="left"
        )
        self.info_text.grid(row=0, column=0, sticky="w")

        # --- Название ---
        self.name_text = ctk.CTkLabel(self.name_frame, text="Задайте название для манги",
                                      font=FONT_TEXT, text_color=TEXT_COLOR)
        self.name_text.grid(row=0, column=0, sticky="w")

        self.name_entry = ctk.CTkEntry(
            self.name_frame,
            width=396, height=30, corner_radius=0, fg_color=SECOND_BG, border_width=0,
            text_color=TEXT_COLOR, font=FONT_TEXT, justify="left",
            placeholder_text="Например: Berserk"
        )
        self.name_entry.grid(row=1, column=0, sticky="w")

        # --- Сортировка ---
        self.start_sorting = ctk.CTkButton(
            self.sorting_frame,
            text="Запустить сортировку файлов",
            width=396, height=30, fg_color=ACCENT, hover_color=HOVER_COLOR,
            corner_radius=0, border_width=0, anchor="center",
            command=lambda: choose_folder(self.selected_folder_label, self)
        )
        self.start_sorting.grid(row=0, column=1, sticky="w", pady=(50, 0))

        # --- Надпись ---
        self.select_label = ctk.CTkLabel(
            self.select_chapters_frame, text="Выберите главы:",
            font=FONT_TEXT, text_color=TEXT_COLOR
        )
        self.select_label.grid(row=0, column=0, pady=(20, 0), columnspan=4, sticky="w")

        # --- Выбор диапазона глав ---
        self.from_label = ctk.CTkLabel(
            self.select_chapters_frame,
            text="От:",
            font=FONT_TEXT, text_color=TEXT_COLOR
        )
        self.from_label.grid(row=1, column=0, )

        self.from_entry = ctk.CTkEntry(
            self.select_chapters_frame,
            width=50, height=30, corner_radius=0, fg_color=SECOND_BG,
            border_width=0, text_color=TEXT_COLOR, font=FONT_TEXT, placeholder_text="1"
        )
        self.from_entry.grid(row=1, column=1, padx=(10, 0))

        self.to_label = ctk.CTkLabel(
            self.select_chapters_frame,
            text="До:",
            font=FONT_TEXT, text_color=TEXT_COLOR
        )
        self.to_label.grid(row=1, column=2, padx=(20, 0))

        self.to_entry = ctk.CTkEntry(
            self.select_chapters_frame,
            width=50, height=30, corner_radius=0, fg_color=SECOND_BG, border_width=0,
            text_color=TEXT_COLOR, font=FONT_TEXT, placeholder_text="100"
        )
        self.to_entry.grid(row=1, column=3, padx=(10, 0))

        self.skip_label = ctk.CTkLabel(
            self.select_chapters_frame,
            text="Пропустить:",
            font=FONT_TEXT, text_color=TEXT_COLOR
        )
        self.skip_label.grid(row=1, column=4, padx=(20, 0))

        self.skip_entry = ctk.CTkEntry(
            self.select_chapters_frame,
            width=100, height=30, corner_radius=0, fg_color=SECOND_BG,
            border_width=0, text_color=TEXT_COLOR, font=FONT_TEXT,
            placeholder_text="3,7,12"
        )
        self.skip_entry.grid(row=1, column=5, padx=(10, 0))

        # --- Кнопка Скачать ---
        self.download_btn = ctk.CTkButton(
            self.downloads_frame,
            text="Скачать", width=396, height=30,
            fg_color=ACCENT, hover_color=HOVER_COLOR, corner_radius=0, border_width=0,
            font=FONT_TEXT, anchor="center",
            command=self.download_click
        )
        self.download_btn.grid(row=0, column=0, pady=(48, 0))

        # --- Выбор конфига ---
        self.open_folder_icon = ctk.CTkImage(Image.open("icons/open_folder_icon.png"), size=(20, 21))

        self.label_open = ctk.CTkLabel(
            self.config_frame,
            text="Открыть конфиг                                             Выбрать конфиг",
            font=FONT_TEXT,
            text_color=TEXT_COLOR
        )
        self.label_open.grid(row=0, column=0, sticky="w", columnspan=6)

        self.open_btn = ctk.CTkButton(
            self.config_frame, image=self.open_folder_icon,
            text="", width=30, height=30, fg_color=ACCENT,
            hover_color=HOVER_COLOR, corner_radius=0, border_width=0,
            command=lambda: choose_folder(self.selected_folder_label, self)
        )
        self.open_btn.grid(row=1, column=0, sticky="w")

        self.combo_box = ctk.CTkComboBox(
            self.config_frame,
            values=get_delete_configs(),
            width=366, height=30, corner_radius=0, fg_color=SECOND_BG,
            button_color=ACCENT, button_hover_color=HOVER_COLOR, dropdown_fg_color=SECOND_BG,
            text_color=TEXT_COLOR, border_width=0
        )
        self.combo_box.grid(row=1, column=1, sticky="w", )

    def search(self):
        url = self.url_entry.get().strip()
        if not url:
            return

        self.overlay.show("Поиск глав...")
        self.overlay.start_timed_progress(min_sec=5, max_sec=10)

        def task():
            try:
                count, name = asyncio.run(len_links(url))

                def update_ui():
                    self.name_entry.delete(0, "end")
                    self.name_entry.insert(0, name)
                    self.from_entry.delete(0, "end")
                    self.from_entry.insert(0, "1")
                    self.to_entry.delete(0, "end")
                    self.to_entry.insert(0, str(count))
                    self.url_discription.configure(text=f"Название: {name}, Найдено {count} глав")
                    self.overlay.finish(count)
                    self.name = name
                    self.url = url

                self.overlay.app.after(0, lambda: update_ui())

            except Exception as e:
                logger.error("Ошибка поиска:", e)
                self.overlay.app.after(0, lambda: self.overlay.finish(0))

        threading.Thread(target=task, daemon=True).start()

    def download_click(self):
        if not self.url:
            self.url_discription.configure(text="Сначала выполните поиск")
            return
        try:
            start_chapter = int(self.from_entry.get())
            end_chapter = int(self.to_entry.get())
            skip_chapters = self.skip_entry.get()
        except ValueError:
            self.url_discription.configure(text="Неверный диапазон глав")
            logger.warning("Неверный диапазон глав")
            return

        if self.folder is None:
            self.folder = Path(get_download_folder())
        else:
            self.folder = Path(self.folder)

        def task():
            try:
                asyncio.run(download_files_with_overlay(
                    save_folder=self.folder, url=self.url,
                    start_chapter=start_chapter, end_chapter=end_chapter, skip_chapters=skip_chapters,
                    overlay=self.overlay
                ))
            except Exception as e:
                logger.error(f"Ошибка при скачивании: {e}")
                self.overlay.app.after(0, lambda: self.overlay.finish(0))

        threading.Thread(target=task, daemon=True).start()

    def paste_from_clipboard(self, entry):
        try:
            text = entry.clipboard_get()
            entry.insert("insert", text)
        except tk.TclError:
            pass

    def show_context_menu(self, event):
        self.menu.tk_popup(event.x_root, event.y_root)

    def on_keypress(self, event):
        if event.state & 0x4:
            if event.keycode == 86:
                self.paste_from_clipboard(self.url_entry)
                return "break"
        return None

    def on_enter(self, event=None):
        self.search()


if __name__ == "__main__":
    app = MangaToolGUI()
    app.mainloop()
