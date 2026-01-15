import threading
import time
import asyncio
import customtkinter as ctk

class OverlayManager:
    def __init__(self, app, bg_color="#2D2D2D", progress_color="#FF8800", accent_color="#FF8800"):
        self.app = app
        self.bg_color = bg_color
        self.progress_color = progress_color
        self.accent_color = accent_color

        self.overlay = None
        self.progress = None
        self.status_label = None
        self.ok_button = None

        self._start_time = 0
        self._finished = False
        self._progress_target = 0.95  # пока задача не завершена, прогресс идёт до 95%

    def show(self, text="Загрузка..."):
        if self.overlay:
            return
        self._finished = False

        self.overlay = ctk.CTkFrame(self.app, fg_color=self.bg_color)
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.overlay.lift()

        center = ctk.CTkFrame(self.overlay, fg_color=self.bg_color, corner_radius=10)
        center.place(relx=0.5, rely=0.5, anchor="center")

        self.status_label = ctk.CTkLabel(center, text=text, font=("Arial", 14))
        self.status_label.pack(padx=20, pady=(0, 10))

        self.progress = ctk.CTkProgressBar(center, width=300, corner_radius=4, progress_color=self.progress_color)
        self.progress.pack(padx=20, pady=(0, 5))
        self.progress.set(0)

    def start_timed_progress(self, min_sec=5, max_sec=15):
        """Плавное движение до 85% за max_sec секунд"""
        self._finished = False
        start = time.time()

        def update():
            if self._finished:
                return
            elapsed = time.time() - start
            progress = min(elapsed / max_sec, 1.0) * self._progress_target
            self.progress.set(progress)
            self.app.after(50, update)

        update()

    def finish(self, count: int):
        self._finished = True
        if self.progress is None:
            return
        current = self.progress.get()
        steps = 30
        increment = (1.0 - current) / steps
        step_delay = 20

        def step(i=0):
            nonlocal current
            if i >= steps:
                if self.progress:  # защита
                    self.progress.set(1.0)
                if self.status_label:
                    self.status_label.configure(text=f"Найдено {count} глав")

                if self.overlay:
                    def close():
                        self.hide()

                    self.ok_button = ctk.CTkButton(
                        self.overlay,
                        text="OK",
                        width=100,
                        fg_color=self.accent_color,
                        hover_color="#FFA733",
                        command=close
                    )
                    self.ok_button.place(relx=0.5, rely=0.62, anchor="center")
                return

            current += increment
            if self.progress:
                self.progress.set(current)
            self.app.after(step_delay, lambda: step(i + 1))

        step()

    def hide(self):
        if self.overlay:
            self.overlay.destroy()
        self.overlay = None
        self.progress = None
        self.status_label = None
        self.ok_button = None