import asyncio
import threading

import customtkinter as ctk
from PIL import Image
import tkinter as tk
from loguru import logger

from gui.buttons_click import choose_folder, get_delete_configs
from gui.overlay import OverlayManager
from gui.theme import BG, FONT_TITLE, ACCENT, SECOND_BG, TEXT_COLOR, FONT_TEXT
from manga_chan_downloader import validate_download_url, len_links

#----------- Окно -----------
app = ctk.CTk()
app.title("Manga tool")
app.geometry("890x500") #570
app.resizable(False, False)
app.configure(fg_color=BG)

overlay = OverlayManager(app)


#----------- Контейнер -----------
container = ctk.CTkFrame(app, fg_color="transparent")
container.grid(row=0, column=0, sticky="ew", padx=25, pady=25)


#----------- Фреймы -----------
header_frame = ctk.CTkFrame(container,fg_color="transparent")
header_frame.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))

search_frame = ctk.CTkFrame(container, fg_color="transparent") # TODO изменить длинну поисковой строки что бы не выходило за пределы других фрэймов
search_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))

folder_frame = ctk.CTkFrame(container, fg_color="transparent")
folder_frame.grid(row=2, column=0, sticky="w", padx=(0, 20))

name_frame = ctk.CTkFrame(container, fg_color="transparent")
name_frame.grid(row=2, column=1, sticky="w", pady=(0, 0))

select_chapters_frame = ctk.CTkFrame(container, fg_color="transparent")
select_chapters_frame.grid(row=3, column=0, sticky="w", pady=(0, 20))

downloads_frame = ctk.CTkFrame(container, fg_color="transparent")
downloads_frame.grid(row=3, column=1, sticky="w", pady=(0, 20))

info_frame = ctk.CTkFrame(container, fg_color="transparent")
info_frame.grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 0))

config_frame = ctk.CTkFrame(container, fg_color="transparent")
config_frame.grid(row=5, column=0, sticky="w", pady=(0, 0))

sorting_frame = ctk.CTkFrame(container, fg_color="transparent")
sorting_frame.grid(row=5, column=1, sticky="w", pady=(0, 20))

# progress_frame = ctk.CTkFrame(app, fg_color="transparent")
# progress_frame.grid(row=2, column=0, sticky="ew", pady=(0, 0))

app.grid_rowconfigure(0, weight=0)     # container сверху
app.grid_rowconfigure(1, weight=1)     # пустое место для растяжки
app.grid_rowconfigure(2, weight=0)     # progress_frame снизу
app.grid_columnconfigure(0, weight=1)

#----------- Заголовок -----------
title = ctk.CTkLabel(header_frame, text="Manga tool", font=FONT_TITLE, text_color=ACCENT)
title.grid(row=0, column=0, columnspan=2, sticky="w")



#----------- Поле для ввода ссылки -----------
# Поле для ввода ссылки
url_entry = ctk.CTkEntry(search_frame,
                         width=707, height=40,
                         corner_radius=0, fg_color=SECOND_BG, border_width=0,
                         text_color=TEXT_COLOR, font=FONT_TEXT,
                         placeholder_text="https://im.manga-chan.me/...")
url_entry.grid(row=0, column=0, sticky="ew")

# Кнопка поиска
search_btn = ctk.CTkButton(search_frame, text="Найти",
                           width=120, height=40,
                           fg_color=ACCENT, hover_color="#FFA733",
                           corner_radius=0, border_width=0,
                           anchor="center",
                           command=lambda: search())
search_btn.grid(row=0, column=1)

# Описание ссылки
url_discription = ctk.CTkLabel(search_frame,
                               text="Вставьте ссылку на мангу с сайта manga-chan - https://im.manga-chan.me/",
                               font=FONT_TEXT, text_color=TEXT_COLOR)
url_discription.grid(row=1, column=0, columnspan=2, sticky="w", pady=(4,0))

# Растяжка колонок
search_frame.grid_columnconfigure(0, weight=1)  # entry растягивается
search_frame.grid_columnconfigure(1, weight=0)  # кнопка фиксированная



#----------- Выбор папки -----------
folder_icon = ctk.CTkImage(Image.open("icons/folder_icon.png"), size=(20, 21))

# Верхняя подпись
folder_discription = ctk.CTkLabel(folder_frame, text="Выберите папку для загрузки файлов",
                                  font=FONT_TEXT, text_color=TEXT_COLOR)
folder_discription.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0,0))

# Кнопка слева и поле пути справа
folder_btn = ctk.CTkButton(folder_frame, image=folder_icon, text="",
                           width=30, height=30,
                           fg_color=ACCENT, hover_color="#FFA733",
                           corner_radius=0, border_width=0,
                           anchor="center",
                           command=lambda: choose_folder(selected_folder_label))
folder_btn.grid(row=1, column=0, sticky="w")

selected_folder_label = ctk.CTkLabel(folder_frame, text="   Папка не выбрана",
                                     width=366, height=30,
                                     fg_color=SECOND_BG, text_color=TEXT_COLOR,
                                     corner_radius=0, anchor="w")
selected_folder_label.grid(row=1, column=1, sticky="w")

# Растяжка колонок
folder_frame.grid_columnconfigure(0, weight=0)
folder_frame.grid_columnconfigure(1, weight=0)

#----------- Инструкция -----------
info_text = ctk.CTkLabel(
    info_frame,
    text="После загрузки посмотрите есть ли какие либо паттерны мусорных файлов, которые вы хотели бы удалить, "
         "например обложки или доп. рисуноки. Выпишите нзавания этих файлов в конфиг и на следующем этапе они будут "
         "удалены из всех томов и глав.",
    font=FONT_TEXT,
    text_color=TEXT_COLOR,
    wraplength=827,
    justify="left"
)
info_text.grid(row=0, column=0, sticky="w")


#----------- Название -----------
name_text = ctk.CTkLabel(name_frame, text="Задайте название для манги", font=FONT_TEXT,text_color=TEXT_COLOR)
name_text.grid(row=0, column=0, sticky="w")

name_entry = ctk.CTkEntry(
    name_frame,
    width=396,
    height=30,
    corner_radius=0,
    fg_color=SECOND_BG,
    border_width=0,
    text_color=TEXT_COLOR,
    font=FONT_TEXT,
    placeholder_text="Например: Berserk",
    justify="left"
)
name_entry.grid(row=1, column=0, sticky="w")

#----------- Сортировка -----------
start_sorting = ctk.CTkButton(
    sorting_frame,
    text="Запустить сортировку файлов",
    width=396,
    height=30,
    fg_color=ACCENT,
    hover_color="#FFA733",
    corner_radius=0,
    border_width=0,
    anchor="center",
    command=lambda: choose_folder(selected_folder_label)
)
start_sorting.grid(row=0, column=1, sticky="w", pady=(50, 0))


# ---------- Надпись ----------
select_label = ctk.CTkLabel(
    select_chapters_frame,
    text="Выберите главы:",
    font=FONT_TEXT,
    text_color=TEXT_COLOR
)
select_label.grid(row=0, column=0, pady=(20, 0), columnspan=4, sticky="w")

# ---------- Выбор диапазона глав ----------
from_label = ctk.CTkLabel(
    select_chapters_frame,
    text="От:",
    font=FONT_TEXT,
    text_color=TEXT_COLOR
)
from_label.grid(row=1, column=0,)

from_entry = ctk.CTkEntry(
    select_chapters_frame,
    width=50,
    height=30,
    corner_radius=0,
    fg_color=SECOND_BG,
    border_width=0,
    text_color=TEXT_COLOR,
    font=FONT_TEXT,
    placeholder_text="1"
)
from_entry.grid(row=1, column=1, padx=(10, 0))

to_label = ctk.CTkLabel(
    select_chapters_frame,
    text="До:",
    font=FONT_TEXT,
    text_color=TEXT_COLOR
)
to_label.grid(row=1, column=2, padx=(20, 0))

to_entry = ctk.CTkEntry(
    select_chapters_frame,
    width=50,
    height=30,
    corner_radius=0,
    fg_color=SECOND_BG,
    border_width=0,
    text_color=TEXT_COLOR,
    font=FONT_TEXT,
    placeholder_text="100"
)
to_entry.grid(row=1, column=3, padx=(10, 0))

skip_label = ctk.CTkLabel(
    select_chapters_frame,
    text="Пропустить:",
    font=FONT_TEXT,
    text_color=TEXT_COLOR
)
skip_label.grid(row=1, column=4, padx=(20, 0))

skip_entry = ctk.CTkEntry(
    select_chapters_frame,
    width=100,
    height=30,
    corner_radius=0,
    fg_color=SECOND_BG,
    border_width=0,
    text_color=TEXT_COLOR,
    font=FONT_TEXT,
    placeholder_text="3,7,12"
)
skip_entry.grid(row=1, column=5, padx=(10, 0))

# ---------- Кнопка Скачать ----------
download_btn = ctk.CTkButton(
    downloads_frame,
    text="Скачать",
    width=396,
    height=30,
    fg_color=ACCENT,
    hover_color="#FFA733",
    corner_radius=0,
    border_width=0,
    font=FONT_TEXT,
    anchor="center",
)
download_btn.grid(row=0, column=0, pady=(48, 0))





#----------- Выбор конфига 2 -----------
open_folder_icon = ctk.CTkImage(Image.open("icons/open_folder_icon.png"), size=(20, 21))

# ----- Верхние подписи -----
label_open = ctk.CTkLabel(
    config_frame,
    text="Открыть конфиг                                             Выбрать конфиг",
    font=FONT_TEXT,
    text_color=TEXT_COLOR
)
label_open.grid(row=0, column=0, sticky="w", columnspan=6)


# ----- Кнопка открытия и ComboBox -----
open_btn = ctk.CTkButton(
    config_frame,
    image=open_folder_icon,
    text="",
    width=30,
    height=30,
    fg_color=ACCENT,
    hover_color="#FFA733",
    corner_radius=0,
    border_width=0,
    command=lambda: choose_folder(selected_folder_label)
)
open_btn.grid(row=1, column=0, sticky="w")

combo_box = ctk.CTkComboBox(
    config_frame,
    values=get_delete_configs(),
    width=366,
    height=30,
    corner_radius=0,
    fg_color=SECOND_BG,
    button_color=ACCENT,
    button_hover_color="#FFA733",
    dropdown_fg_color=SECOND_BG,
    text_color=TEXT_COLOR,
    border_width=0
)
combo_box.grid(row=1, column=1, sticky="w",)


def search():
    url = url_entry.get().strip()
    if not url:
        return

    overlay.show("Поиск глав...")
    overlay.start_timed_progress(min_sec=5, max_sec=10)

    def task():
        try:
            valid_url = asyncio.run(validate_download_url(url))
            count, name = asyncio.run(len_links(valid_url))
            print(f"Найдено ссылок: {count}")  # для консоли
            overlay.finish(count)  # передаем количество
        except Exception:
            overlay.finish(0)  # на случай ошибки

    threading.Thread(target=task, daemon=True).start()


# ---------- Функция вставки ----------
def paste_from_clipboard(entry):
    try:
        text = entry.clipboard_get()
        entry.insert("insert", text)
    except tk.TclError:
        pass

# ---------- Entry ----------
url_entry = ctk.CTkEntry(
    search_frame,
    width=707, height=40,
    corner_radius=0, fg_color=SECOND_BG, border_width=0,
    text_color=TEXT_COLOR, font=FONT_TEXT,
    placeholder_text="https://im.manga-chan.me/..."
)
url_entry.grid(row=0, column=0, sticky="ew")  # растягиваем по ширине

# ---------- Контекстное меню ----------
menu = tk.Menu(url_entry, tearoff=0)
menu.add_command(label="Вставить", command=lambda: paste_from_clipboard(url_entry))

def show_menu(event):
    menu.tk_popup(event.x_root, event.y_root)

url_entry.bind("<Button-3>", show_menu)  # ПКМ

# ---------- Ctrl+V на любой раскладке ----------
def on_keypress(event):
    # Проверка зажатого Ctrl
    if event.state & 0x4:
        # keycode 86 — физическая клавиша V на любой раскладке
        if event.keycode == 86:
            paste_from_clipboard(url_entry)
            return "break"  # предотвращаем дублирующую вставку

url_entry.bind("<KeyPress>", on_keypress)

# ---------- Поиск по Enter ----------
def on_enter(event=None):
    search()  # передаём текст из поля

url_entry.bind("<Return>", on_enter)
url_entry.bind("<KP_Enter>", on_enter)





if __name__ == "__main__":
    app.mainloop()