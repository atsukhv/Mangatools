import customtkinter as ctk
from PIL import Image

from gui.buttons_click import choose_folder, get_delete_configs

#----------- Настройки ----------
BG = "#2D2D2D"
SECOND_BG = "#64513C"
ACCENT = "#FF8800"
TEXT_COLOR = "#FFFFFF"

FONT_TITLE = ("Georgia", 50, "bold")
FONT_TEXT = ("Arial", 14)


#----------- Окно -----------
app = ctk.CTk()
app.title("Manga on Kindle tool")
app.geometry("890x500")
app.resizable(False, True) #TODO заменить на false
app.configure(fg_color=BG)

#----------- Контейнер -----------
container = ctk.CTkFrame(app, fg_color="transparent")
container.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

container.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
container.grid_columnconfigure(0, weight=1)
container.grid_columnconfigure(1, weight=1)





#----------- Фреймы -----------
header_frame = ctk.CTkFrame(container,fg_color="transparent")
header_frame.grid(row=0,column=0,sticky="ew",pady=(0, 24))

search_frame = ctk.CTkFrame(container, fg_color="transparent")
search_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 24))

folder_frame = ctk.CTkFrame(container, fg_color="transparent")
folder_frame.grid(row=2, column=0, sticky="ew", padx=(0, 20))
folder_frame.grid_columnconfigure(0, weight=0)
folder_frame.grid_columnconfigure(1, weight=1)


config_frame = ctk.CTkFrame(container, fg_color="transparent")
config_frame.grid(row=2, column=1, sticky="ew", padx=(0, 0))





progress_frame = ctk.CTkFrame(app, fg_color="transparent")
progress_frame.grid(row=1, column=0, sticky="ew")

#----------- Заголовок -----------
title = ctk.CTkLabel(header_frame, text="Manga on Kindle tool", font=FONT_TITLE, text_color=ACCENT)
title.grid(row=0, column=0, sticky="w")

#----------- Поле для ввода ссылки -----------
# Поле для ввода ссылки
url_entry = ctk.CTkEntry(search_frame,
                         width=707, height=40,
                         corner_radius=0, fg_color=SECOND_BG, border_width=0,
                         text_color=TEXT_COLOR, font=FONT_TEXT,
                         placeholder_text="https://im.manga-chan.me/...")
url_entry.grid(row=0, column=0, sticky="ew")  # растягиваем по ширине

# Кнопка поиска
search_btn = ctk.CTkButton(search_frame, text="Найти",
                           width=120, height=40,
                           fg_color=ACCENT, hover_color="#FFA733",
                           corner_radius=0, border_width=0,
                           anchor="center",
                           command=lambda: choose_folder(selected_folder_label))
search_btn.grid(row=0, column=1)  # рядом с entry

# Описание ссылки
url_discription = ctk.CTkLabel(search_frame,
                               text="Вставьте ссылку на мангу с сайта manga-chan - https://im.manga-chan.me/",
                               font=FONT_TEXT, text_color=TEXT_COLOR)
url_discription.grid(row=1, column=0, columnspan=2, sticky="w", pady=(4,0))

# Растяжка колонок
search_frame.grid_columnconfigure(0, weight=1)  # entry растягивается
search_frame.grid_columnconfigure(1, weight=0)  # кнопка фиксированная

#----------- Выбор папки (grid) -----------
folder_icon = ctk.CTkImage(Image.open("icons/folder_icon.png"), size=(20, 21))

# Верхняя подпись
folder_discription = ctk.CTkLabel(folder_frame, text="Выберите папку для загрузки файлов",
                                  font=FONT_TEXT, text_color=TEXT_COLOR)
folder_discription.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0,4))

# Кнопка слева и поле пути справа
folder_btn = ctk.CTkButton(folder_frame, image=folder_icon, text="",
                           width=20, height=21,
                           fg_color=ACCENT, hover_color="#FFA733",
                           corner_radius=0, border_width=0,
                           anchor="center",
                           command=lambda: choose_folder(selected_folder_label))
folder_btn.grid(row=1, column=0, sticky="w")

selected_folder_label = ctk.CTkLabel(folder_frame, text="   Папка не выбрана",
                                     width=366, height=30,
                                     fg_color=SECOND_BG, text_color=TEXT_COLOR,
                                     corner_radius=0, anchor="w")
selected_folder_label.grid(row=1, column=1, sticky="w", padx=(5,0))

# Растяжка колонок
folder_frame.grid_columnconfigure(0, weight=0)
folder_frame.grid_columnconfigure(1, weight=1)


#----------- Выбор конфига -----------
open_folder_icon = ctk.CTkImage(Image.open("icons/open_folder_icon.png"), size=(20, 21))

# Верхние подписи
open_folder_discription = ctk.CTkLabel(config_frame, text="Открыть конфиг",
                                       font=FONT_TEXT, text_color=TEXT_COLOR)
folder_discription.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0,4))

combo_label = ctk.CTkLabel(config_frame, text="Выбрать конфиг",
                           font=FONT_TEXT, text_color=TEXT_COLOR)
combo_label.grid(row=0, column=1, sticky="w")

# Кнопка слева и ComboBox справа в одной строке
button_combo_frame = ctk.CTkFrame(config_frame, fg_color="transparent")  # вложенный фрейм для "склеивания"
button_combo_frame.grid(row=1, column=0, columnspan=2, sticky="w")

open_folder_btn = ctk.CTkButton(button_combo_frame,
                                image=open_folder_icon,
                                text="",
                                width=20,
                                height=21,
                                fg_color=ACCENT,
                                hover_color="#FFA733",
                                corner_radius=0,
                                border_width=0,
                                anchor="center",
                                command=lambda: choose_folder(selected_folder_label))
open_folder_btn.pack(side="left")  # слева

combo_box = ctk.CTkComboBox(button_combo_frame,
                            values=get_delete_configs(),
                            width=366,
                            height=30,
                            corner_radius=0,
                            fg_color=SECOND_BG,
                            button_color=ACCENT,
                            button_hover_color="#FFA733",
                            dropdown_fg_color=SECOND_BG,
                            text_color=TEXT_COLOR,
                            border_width=0)
combo_box.pack(side="left", padx=(0,0))  # прямо к кнопке, без промежутка

# Колонки config_frame
config_frame.grid_columnconfigure(0, weight=0)
config_frame.grid_columnconfigure(1, weight=1)

#----------- Инструкция -----------
info_text = ctk.CTkLabel(
    container,
    text="После загрузки посмотрите есть ли какие либо паттерны мусорных файлов, которые вы хотели бы удалить, "
         "например обложки или доп. рисуноки. Выпишите нзавания этих файлов в конфиг и на следующем этапе они будут "
         "удалены из всех томов и глав.",
    font=FONT_TEXT,
    text_color=TEXT_COLOR,
    wraplength=827,
    justify="left"
)
info_text.place(x=0, y=250)


#----------- Название -----------
name_text = ctk.CTkLabel(
    container,
    text="Задайте название для манги",
    font=FONT_TEXT,
    text_color=TEXT_COLOR
)
name_text.place(x=0, y=324)

name_entry = ctk.CTkEntry(
    container,
    width=396,
    height=40,
    corner_radius=0,
    fg_color=SECOND_BG,
    border_width=0,
    text_color=TEXT_COLOR,
    font=FONT_TEXT,
    placeholder_text="Например: Berserk",
    justify="left"
)
name_entry.place(x=0, y=354)

#----------- Сортировка -----------
start_sorting = ctk.CTkButton(
    container,
    text="Запустить сортировку файлов",
    width=396,
    height=40,
    fg_color=ACCENT,
    hover_color="#FFA733",
    corner_radius=0,
    border_width=0,
    anchor="center",
    command=lambda: choose_folder(selected_folder_label)
)
start_sorting.place(x=434, y=354)

#----------- Прогресс-бар -----------
progress = ctk.CTkProgressBar(
    progress_frame,
    height=15,
    corner_radius=0,
    fg_color=SECOND_BG,
    progress_color=ACCENT
)
progress.pack(side="bottom", fill="x")
progress.set(0)

progress_text = ctk.CTkLabel(
    progress_frame,
    text="Прогрессирую",
    font=FONT_TEXT,
    text_color=TEXT_COLOR,
    anchor="w",
    padx=5
)
progress_text.pack(side="bottom", fill="x")


# ---------- Надпись ----------
select_label = ctk.CTkLabel(
    container,
    text="Выберите главы:",
    font=FONT_TEXT,
    text_color=TEXT_COLOR
)
select_label.place(x=0, y=370)  # чуть выше строки с полями

# ---------- Выбор диапазона глав ----------
from_label = ctk.CTkLabel(
    container,
    text="От:",
    font=FONT_TEXT,
    text_color=TEXT_COLOR
)
from_label.place(x=0, y=400)

from_entry = ctk.CTkEntry(
    container,
    width=50,
    height=30,
    corner_radius=0,
    fg_color=SECOND_BG,
    border_width=0,
    text_color=TEXT_COLOR,
    font=FONT_TEXT,
    placeholder_text="1"
)
from_entry.place(x=30, y=400)

to_label = ctk.CTkLabel(
    container,
    text="До:",
    font=FONT_TEXT,
    text_color=TEXT_COLOR
)
to_label.place(x=90, y=400)

to_entry = ctk.CTkEntry(
    container,
    width=50,
    height=30,
    corner_radius=0,
    fg_color=SECOND_BG,
    border_width=0,
    text_color=TEXT_COLOR,
    font=FONT_TEXT,
    placeholder_text="10"
)
to_entry.place(x=120, y=400)

skip_label = ctk.CTkLabel(
    container,
    text="Пропустить:",
    font=FONT_TEXT,
    text_color=TEXT_COLOR
)
skip_label.place(x=180, y=400)

skip_entry = ctk.CTkEntry(
    container,
    width=100,
    height=30,
    corner_radius=0,
    fg_color=SECOND_BG,
    border_width=0,
    text_color=TEXT_COLOR,
    font=FONT_TEXT,
    placeholder_text="3,7,12"
)
skip_entry.place(x=260, y=400)

# ---------- Кнопка Скачать ----------
download_btn = ctk.CTkButton(
    container,
    text="Скачать",
    width=120,
    height=30,
    fg_color=ACCENT,
    hover_color="#FFA733",
    corner_radius=0,
    border_width=0,
    font=FONT_TEXT,
    anchor="center",
)
download_btn.place(x=380, y=400)




if __name__ == "__main__":
    app.mainloop()