import tkinter as tk
from pathlib import Path
import customtkinter as ctk
from loguru import logger


class ConfigEditorWindow(ctk.CTkToplevel):
    """Окно для редактирования конфигов"""
    def __init__(self, parent, config_path: Path, accent_color="#FF8800", hover_color="#FFA733", **kwargs):
        super().__init__(parent, **kwargs)

        self.config_path = config_path
        self.accent_color = accent_color
        self.hover_color = hover_color
        self.saved_callback = None

        # Настройка окна
        self.title(f"Редактирование: {config_path.name}")
        self.geometry("600x500")
        self.resizable(True, True)
        self.configure(fg_color="#2D2D2D")

        # Делаем окно модальным
        self.transient(parent)
        self.grab_set()

        self._create_widgets()
        self._load_config()

    def _create_widgets(self):
        """Создаёт виджеты окна"""
        # Контейнер
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Заголовок
        title = ctk.CTkLabel(
            container,
            text=f"Конфиг: {self.config_path.name}",
            font=("Arial", 16, "bold"),
            text_color="#FFFFFF"
        )
        title.pack(pady=(0, 10))

        # Текстовое поле с прокруткой
        text_frame = ctk.CTkFrame(container, fg_color="transparent")
        text_frame.pack(fill="both", expand=True, pady=(0, 10))

        self.text_widget = ctk.CTkTextbox(
            text_frame,
            fg_color="#64513C",
            text_color="#FFFFFF",
            font=("Consolas", 12),
            wrap="word",
            corner_radius=0
        )
        self.text_widget.pack(fill="both", expand=True)

        # Кнопка Сохранить
        self.save_btn = ctk.CTkButton(
            container,
            text="Сохранить",
            width=200,
            height=40,
            fg_color=self.accent_color,
            hover_color=self.hover_color,
            corner_radius=0,
            font=("Arial", 14),
            command=self._save_config
        )
        self.save_btn.pack(pady=(0, 0))

    def _load_config(self):
        """Загружает содержимое конфига в текстовое поле"""
        try:
            if self.config_path.exists():
                content = self.config_path.read_text(encoding="utf-8")
                self.text_widget.delete("1.0", "end")
                self.text_widget.insert("1.0", content)
            else:
                self.text_widget.delete("1.0", "end")
                self.text_widget.insert("1.0", "# Конфиг пуст\n")
                logger.warning(f"Файл конфига не найден: {self.config_path}")
        except Exception as e:
            logger.error(f"Ошибка при загрузке конфига: {e}")
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", f"# Ошибка загрузки: {e}\n")

    def _save_config(self):
        """Сохраняет содержимое текстового поля в файл"""
        try:
            content = self.text_widget.get("1.0", "end-1c")  # end-1c убирает последний \n

            # Создаём папку, если её нет
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            # Сохраняем файл
            self.config_path.write_text(content, encoding="utf-8")
            logger.info(f"Конфиг сохранён: {self.config_path}")

            # Вызываем callback, если он установлен
            if self.saved_callback:
                # Передаём имя файла без расширения
                config_name = self.config_path.stem
                self.saved_callback(config_name)

            # Закрываем окно
            self.destroy()

        except Exception as e:
            logger.error(f"Ошибка при сохранении конфига: {e}")
            # Можно добавить всплывающее окно с ошибкой
            error_window = ctk.CTkToplevel(self)
            error_window.title("Ошибка")
            error_window.geometry("300x100")
            error_label = ctk.CTkLabel(
                error_window,
                text=f"Не удалось сохранить:\n{e}",
                wraplength=280
            )
            error_label.pack(pady=20)

    def set_save_callback(self, callback):
        self.saved_callback = callback


def open_config_editor(parent, config_path: str | Path, on_save_callback=None):

    config_path = Path(config_path)
    editor = ConfigEditorWindow(parent, config_path)

    if on_save_callback:
        editor.set_save_callback(on_save_callback)

    return editor