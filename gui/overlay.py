import threading
import customtkinter as ctk


class OverlayManager:
    def __init__(self, app, bg_color="#2D2D2D"):
        self.app = app
        self.bg_color = bg_color

        self.overlay = None
        self.progress = None
        self.spinner = None

        self.stop_event = threading.Event()

    def show(self, text="Загрузка..."):
        if self.overlay:
            return

        self.stop_event.clear()

        # 🔲 затемнённый слой (эмуляция прозрачности)
        self.overlay = ctk.CTkFrame(
            self.app,
            fg_color="#1F1F1F"  # чуть темнее BG
        )
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.overlay.lift()

        # 📦 центральная карточка
        center = ctk.CTkFrame(
            self.overlay,
            fg_color=self.bg_color,
            corner_radius=10
        )
        center.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            center,
            text=text,
            font=("Arial", 14)
        ).pack(padx=20, pady=(20, 10))

        row = ctk.CTkFrame(center, fg_color="transparent")
        row.pack(padx=20, pady=10)

        # ⭕ индикатор (кружок)
        self.spinner = ctk.CTkProgressBar(
            row,
            width=26,
            height=26,
            mode="indeterminate",
            corner_radius=13
        )
        self.spinner.pack(side="left", padx=(0, 12))
        self.spinner.start()

        # 📊 прогресс
        self.progress = ctk.CTkProgressBar(
            row,
            width=220,
            corner_radius=4
        )
        self.progress.pack(side="left")
        self.progress.set(0)

        # ⛔ кнопка стоп
        ctk.CTkButton(
            center,
            text="Остановить",
            fg_color="#AA3333",
            hover_color="#CC4444",
            command=self.stop
        ).pack(pady=(10, 20))

    def hide(self):
        if self.spinner:
            self.spinner.stop()

        if self.overlay:
            self.overlay.destroy()

        self.overlay = None
        self.spinner = None
        self.progress = None

    def stop(self):
        self.stop_event.set()

    def set_progress(self, value: float):
        if self.progress:
            self.app.after(0, self.progress.set, value)
