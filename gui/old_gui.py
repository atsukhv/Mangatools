import customtkinter as ctk
from PIL import Image
from gui.buttons_click import choose_folder, get_delete_configs

# ---------- Настройки ----------
BG = "#2D2D2D"
SECOND_BG = "#64513C"
ACCENT = "#FF8800"
TEXT_COLOR = "#FFFFFF"

FONT_TITLE = ("Georgia", 50, "bold")
FONT_TEXT = ("Arial", 14)

# ---------- Окно ----------
app = ctk.CTk()
app.title("Manga on Kindle tool")
app.geometry("890x500")
app.configure(fg_color=BG)

# ---------- Контейнер ----------
container = ctk.CTkFrame(app, fg_color="transparent")
container.pack(expand=True, fill="both", padx=30, pady=30)

# ---------- Заголовок ----------
title = ctk.CTkLabel(container, text="Manga on Kindle tool", font=FONT_TITLE, text_color=ACCENT)
title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 20))

# ---------- Поле для ввода ссылки + кнопка Найти ----------
url_entry = ctk.CTkEntry(container, width=707, height=40, corner_radius=0,
                         fg_color=SECOND_BG, border_width=0, text_color=TEXT_COLOR,
                         font=FONT_TEXT, placeholder_text="https://im.manga-chan.me/...")
url_entry.grid(row=1, column=0, sticky="w")

search_btn = ctk.CTkButton(container, text="Найти", width=120, height=40,
                           fg_color=ACCENT, hover_color="#FFA733", corner_radius=0,
                           border_width=0, anchor="center",
                           command=lambda: choose_folder(None))
search_btn.grid(row=1, column=1, sticky="w", padx=(10,0))

url_discription = ctk.CTkLabel(container, text="Вставьте ссылку на мангу с сайта manga-chan - https://im.manga-chan.me/",
                               font=FONT_TEXT, text_color=TEXT_COLOR, wraplength=827, justify="left")
url_discription.grid(row=2, column=0, columnspan=2, sticky="w", pady=(5,20))

# ---------- Выбор диапазона глав ----------
select_label = ctk.CTkLabel(container, text="Выберите главы:", font=FONT_TEXT, text_color=TEXT_COLOR)
select_label.grid(row=3, column=0, sticky="w", pady=(0,5))

from_label = ctk.CTkLabel(container, text="От:", font=FONT_TEXT, text_color=TEXT_COLOR)
from_label.grid(row=3, column=0, sticky="w", padx=(100,0))

from_entry = ctk.CTkEntry(container, width=50, height=30, corner_radius=0,
                          fg_color=SECOND_BG, border_width=0, text_color=TEXT_COLOR,
                          font=FONT_TEXT, placeholder_text="1")
from_entry.grid(row=3, column=0, sticky="w", padx=(130,0))

to_label = ctk.CTkLabel(container, text="До:", font=FONT_TEXT, text_color=TEXT_COLOR)
to_label.grid(row=3, column=0, sticky="w", padx=(190,0))

to_entry = ctk.CTkEntry(container, width=50, height=30, corner_radius=0,
                        fg_color=SECOND_BG, border_width=0, text_color=TEXT_COLOR,
                        font=FONT_TEXT, placeholder_text="10")
to_entry.grid(row=3, column=0, sticky="w", padx=(220,0))

skip_label = ctk.CTkLabel(container, text="Пропустить:", font=FONT_TEXT, text_color=TEXT_COLOR)
skip_label.grid(row=3, column=0, sticky="w", padx=(280,0))

skip_entry = ctk.CTkEntry(container, width=100, height=30, corner_radius=0,
                          fg_color=SECOND_BG, border_width=0, text_color=TEXT_COLOR,
                          font=FONT_TEXT, placeholder_text="3,7,12")
skip_entry.grid(row=3, column=0, sticky="w", padx=(360,0))

download_btn = ctk.CTkButton(container, text="Скачать", width=120, height=30,
                             fg_color=ACCENT, hover_color="#FFA733", corner_radius=0,
                             border_width=0, font=FONT_TEXT)
download_btn.grid(row=3, column=1, sticky="w", padx=(10,0))

# ---------- Выбор папки ----------
folder_icon = ctk.CTkImage(Image.open("icons/folder_icon.png"), size=(20,21))
folder_discription = ctk.CTkLabel(container, text="Выберите папку для загрузки файлов",
                                  font=FONT_TEXT, text_color=TEXT_COLOR)
folder_discription.grid(row=4, column=0, sticky="w", pady=(20,5))

folder_btn = ctk.CTkButton(container, image=folder_icon, text="", width=20, height=21,
                           fg_color=ACCENT, hover_color="#FFA733", corner_radius=0,
                           border_width=0, anchor="center", command=lambda: choose_folder(None))
folder_btn.grid(row=5, column=0, sticky="w")

selected_folder_label = ctk.CTkLabel(container, text="   Папка не выбрана", width=366, height=30,
                                     fg_color=SECOND_BG, text_color=TEXT_COLOR, corner_radius=0, anchor="w")
selected_folder_label.grid(row=5, column=1, sticky="w", padx=(10,0))

# ---------- Выбор конфига ----------
open_folder_icon = ctk.CTkImage(Image.open("icons/open_folder_icon.png"), size=(20,21))
open_folder_discription = ctk.CTkLabel(container, text="Открыть конфиг", font=FONT_TEXT, text_color=TEXT_COLOR)
open_folder_discription.grid(row=6, column=0, sticky="w", pady=(20,5))

open_folder_btn = ctk.CTkButton(container, image=open_folder_icon, text="", width=20, height=21,
                                fg_color=ACCENT, hover_color="#FFA733", corner_radius=0,
                                border_width=0, anchor="center", command=lambda: choose_folder(None))
open_folder_btn.grid(row=7, column=0, sticky="w")

combo_box = ctk.CTkComboBox(container, values=get_delete_configs(), width=366, height=30,
                            corner_radius=0, fg_color=SECOND_BG, button_color=ACCENT,
                            button_hover_color="#FFA733", dropdown_fg_color=SECOND_BG,
                            text_color=TEXT_COLOR, border_width=0)
combo_box.grid(row=7, column=1, sticky="w", padx=(10,0))

# ---------- Название манги ----------
name_text = ctk.CTkLabel(container, text="Задайте название для манги", font=FONT_TEXT, text_color=TEXT_COLOR)
name_text.grid(row=8, column=0, sticky="w", pady=(20,5))

name_entry = ctk.CTkEntry(container, width=396, height=40, corner_radius=0,
                          fg_color=SECOND_BG, border_width=0, text_color=TEXT_COLOR,
                          font=FONT_TEXT, placeholder_text="Например: Berserk", justify="left")
name_entry.grid(row=9, column=0, sticky="w")

start_sorting = ctk.CTkButton(container, text="Запустить сортировку файлов",
                               width=396, height=40, fg_color=ACCENT, hover_color="#FFA733",
                               corner_radius=0, border_width=0, anchor="center", command=lambda: choose_folder(None))
start_sorting.grid(row=9, column=1, sticky="w", padx=(10,0))

# ---------- Инструкция ----------
info_text = ctk.CTkLabel(container, text="После загрузки посмотрите есть ли какие либо паттерны мусорных файлов, "
                                         "которые вы хотели бы удалить, например обложки или доп. рисуноки. "
                                         "Выпишите нзавания этих файлов в конфиг и на следующем этапе они будут "
                                         "удалены из всех томов и глав.", font=FONT_TEXT,
                         text_color=TEXT_COLOR, wraplength=827, justify="left")
info_text.grid(row=10, column=0, columnspan=2, sticky="w", pady=(20,0))

# ---------- Прогресс-бар ----------
progress_text = ctk.CTkLabel(app, text="Прогрессирую", font=FONT_TEXT, text_color=TEXT_COLOR, anchor="w", padx=5)
progress_text.pack(side="bottom", fill="x")

progress = ctk.CTkProgressBar(app, height=15, corner_radius=0, fg_color=SECOND_BG, progress_color=ACCENT)
progress.pack(side="bottom", fill="x")
progress.set(0)

app.mainloop()
