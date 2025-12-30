import asyncio

import customtkinter as ctk
from PIL import Image
import tkinter as tk
from loguru import logger

from gui.buttons_click import choose_folder, get_delete_configs
from manga_chan_downloader import validate_download_url, len_links

# Настройки
BG = "#2D2D2D"
SECOND_BG = "#64513C"
ACCENT = "#FF8800"
TEXT_COLOR = "#FFFFFF"
FONT_TITLE = ("Georgia", 50, "bold")
FONT_TEXT = ("Arial", 14)

class MangaToolGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        # --- Окно ---
        self.title("Manga tool")
        self.geometry("890x570") #570
        self.resizable(False, False)
        self.configure(fg_color=BG)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0, sticky="ew", padx=25, pady=25)

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


if __name__ == "__main__":
    app = MangaToolGUI()
    app.mainloop()