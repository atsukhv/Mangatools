import os
from pathlib import Path

# Папка с файлами
folder = r"D:\Библиотека kindle\Загрузки"

for file_path in Path(folder).rglob("*"):
    if file_path.is_file() and "_manga-chan.me" in file_path.name:
        new_name = file_path.name.replace("_manga-chan.me", "")
        new_path = file_path.with_name(new_name)
        os.rename(file_path, new_path)
        print(f"{file_path.name} → {new_name}")
