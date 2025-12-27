import customtkinter as ctk
from tkinter import filedialog

# =========================
# НАСТРОЙКИ
# =========================
ctk.set_appearance_mode("dark")

ACCENT = "#FF9500"
BG = "#3E3E3E"
INPUT_BG = "#5A5A5A"
TEXT = "#FFFFFF"
SUBTEXT = "#D0D0D0"

FONT_TITLE = ("Georgia", 36, "bold")
FONT_TEXT = ("Arial", 14)
FONT_BUTTON = ("Arial", 15, "bold")
FONT_SMALL = ("Arial", 12)

# =========================
# ПРИЛОЖЕНИЕ
# =========================
app = ctk.CTk()
app.title("Manga on Kindle tool")
app.geometry("900x620")
app.configure(fg_color=BG)

# =========================
# КОНТЕЙНЕР
# =========================
container = ctk.CTkFrame(
    app,
    fg_color="transparent"
)
container.pack(expand=True, fill="both", padx=40, pady=30)

# =========================
# ЗАГОЛОВОК
# =========================
title = ctk.CTkLabel(
    container,
    text="Manga on Kindle tool",
    font=FONT_TITLE,
    text_color=ACCENT
)
title.pack(pady=(20, 20))

# =========================
# ОПИСАНИЕ
# =========================
desc = ctk.CTkLabel(
    container,
    text="Вставьте ссылку на мангу с сайта manga-chan – https://im.manga-chan.me/",
    font=FONT_TEXT,
    text_color=SUBTEXT
)
desc.pack(pady=(0, 20))

# =========================
# ВВОД ССЫЛКИ
# =========================
url_entry = ctk.CTkEntry(
    container,
    height=52,
    corner_radius=10,
    fg_color=INPUT_BG,
    border_width=0,
    text_color=TEXT,
    font=FONT_TEXT,
    placeholder_text="https://im.manga-chan.me/..."
)
url_entry.pack(fill="x", padx=40, pady=(0, 30))

# =========================
# ВЫБОР ПАПКИ
# =========================
selected_folder = None

def choose_folder():
    global selected_folder
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        folder_label.configure(text=f"Папка: {selected_folder}")
        set_status("Папка выбрана", 0.1)

folder_btn = ctk.CTkButton(
    container,
    text="Выбрать папку для загрузки",
    height=48,
    corner_radius=12,
    fg_color=ACCENT,
    hover_color="#FFA733",
    text_color="black",
    font=FONT_BUTTON,
    command=choose_folder
)
folder_btn.pack(pady=(0, 10))

folder_label = ctk.CTkLabel(
    container,
    text="Папка не выбрана",
    font=FONT_SMALL,
    text_color=SUBTEXT
)
folder_label.pack(pady=(0, 30))

# =========================
# ИНФО ТЕКСТ
# =========================
info_text = (
    "После загрузки посмотрите есть ли какие либо паттерны мусорных файлов,\n"
    "которые вы хотели бы удалить, например обложки или доп. рисунки.\n"
    "Выпишите названия этих файлов в конфиг и на следующем этапе они будут\n"
    "удалены из всех томов и глав."
)

info = ctk.CTkLabel(
    container,
    text=info_text,
    font=FONT_TEXT,
    text_color=SUBTEXT,
    justify="left"
)
info.pack(pady=(0, 30))

# =========================
# КНОПКИ ДЕЙСТВИЙ
# =========================
buttons_frame = ctk.CTkFrame(container, fg_color="transparent")
buttons_frame.pack(pady=(0, 20))

def open_config():
    set_status("Открытие конфига...", 0.4)

def start_sorting():
    set_status("Сортировка файлов...", 0.7)
    app.after(1500, lambda: set_status("Готово", 1.0))

config_btn = ctk.CTkButton(
    buttons_frame,
    text="Открыть конфиг",
    width=260,
    height=48,
    corner_radius=12,
    fg_color=ACCENT,
    hover_color="#FFA733",
    text_color="black",
    font=FONT_BUTTON,
    command=open_config
)
config_btn.grid(row=0, column=0, padx=20)

sort_btn = ctk.CTkButton(
    buttons_frame,
    text="Запустить сортировку файлов",
    width=320,
    height=48,
    corner_radius=12,
    fg_color=ACCENT,
    hover_color="#FFA733",
    text_color="black",
    font=FONT_BUTTON,
    command=start_sorting
)
sort_btn.grid(row=0, column=1, padx=20)

# =========================
# ПРОГРЕСС / СТАТУС
# =========================
status_var = ctk.StringVar(value="Ожидание действий пользователя")

progress = ctk.CTkProgressBar(
    container,
    height=28,
    corner_radius=0,
    fg_color=INPUT_BG,
    progress_color=ACCENT
)
progress.set(0)
progress.pack(side="bottom", fill="x")

status_label = ctk.CTkLabel(
    progress,
    textvariable=status_var,
    font=FONT_SMALL,
    text_color="black"
)
status_label.place(relx=0.5, rely=0.5, anchor="center")

def set_status(text, value=None):
    status_var.set(text)
    if value is not None:
        progress.set(value)

# =========================
# START
# =========================
app.mainloop()
