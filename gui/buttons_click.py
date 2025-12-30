import os
from tkinter import filedialog


def choose_folder(label_widget):
    folder_path = filedialog.askdirectory()
    if folder_path:
        label_widget.configure(text="   " + folder_path)


def get_delete_configs():
    folder_path = os.path.join(os.path.dirname(__file__), "../delete_configs")

    if not os.path.exists(folder_path):
        return ["(Создать новый конфиг)                                            "]

    files = [
        os.path.splitext(f)[0]
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and f.lower() != "template.txt"
    ]

    return ["(Создать новый конфиг)                                            "] + files


def search():
    ...