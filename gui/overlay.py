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

        # фон оверлея
        self.overlay = ctk.CTkFrame(self.app, fg_color=self.bg_color)
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.overlay.lift()

        # центрируем прогресс и текст
        center = ctk.CTkFrame(self.overlay, fg_color=self.bg_color, corner_radius=10)
        center.place(relx=0.5, rely=0.5, anchor="center")

        # текст сверху
        self.status_label = ctk.CTkLabel(center, text=text, font=("Arial", 14))
        self.status_label.pack(padx=20, pady=(0, 10))

        # прогресс бар
        self.progress = ctk.CTkProgressBar(center, width=300, corner_radius=4, progress_color=self.progress_color)
        self.progress.pack(padx=20, pady=(0, 5))
        self.progress.set(0)

    def start_timed_progress(self, min_sec=5, max_sec=15):
        """Плавно движет прогресс до ~85% за случайное время от min_sec до max_sec"""
        self._start_time = time.time()
        self._finished = False
        duration = max(min_sec, min(max_sec, max_sec))  # гарантируем, что в диапазоне

        def run():
            while not self._finished:
                elapsed = time.time() - self._start_time
                progress = min(elapsed / duration, 1.0) * self._progress_target
                self.app.after(0, self.progress.set, progress)
                time.sleep(0.03)  # 30ms для плавного обновления

        threading.Thread(target=run, daemon=True).start()

    def finish(self, count:int):
        """Доводит прогресс до 100%, показывает текст результата и кнопку OK"""
        self._finished = True

        def smooth_finish():
            current = self.progress.get()
            steps = 20
            step = (1.0 - current) / steps
            for _ in range(steps):
                current += step
                self.app.after(0, self.progress.set, current)
                time.sleep(0.03)
            self.app.after(0, self.progress.set, 1.0)

            # текст результата
            self.app.after(0, lambda: self.status_label.configure(text=f"Найдено {count} глав"))

            # кнопка OK под прогрессбаром
            def close_overlay():
                self.hide()

            self.ok_button = ctk.CTkButton(
                self.overlay,
                text="OK",
                width=100,
                fg_color=self.accent_color,
                hover_color="#FFA733",
                command=close_overlay
            )
            self.ok_button.place(relx=0.5, rely=0.62, anchor="center")

        threading.Thread(target=smooth_finish, daemon=True).start()

    def hide(self):
        if self.overlay:
            self.overlay.destroy()
        self.overlay = None
        self.progress = None
        self.status_label = None
        self.ok_button = None