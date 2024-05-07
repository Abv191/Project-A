import os
import sys
from concurrent.futures import ThreadPoolExecutor
from shutil import copy2

def get_files_in_directory(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

def move_file(file_path, destination):
    try:
        copy2(file_path, os.path.join(destination, os.path.basename(file_path)))
        print(f"Файл {file_path} скопійовано до {destination}")
    except Exception as e:
        print(f"Помилка під час копіювання файлу {file_path}: {e}")

def sort_files_by_extension(source_directory, destination_directory):
    files = get_files_in_directory(source_directory)

    for file in files:
        extension = os.path.splitext(file)[1]
        if not extension:
            extension_folder = os.path.join(destination_directory, "unknown")
        else:
            extension_folder = os.path.join(destination_directory, extension[1:])
        if not os.path.exists(extension_folder):
            os.makedirs(extension_folder)

    with ThreadPoolExecutor() as executor:
        for file in files:
            extension = os.path.splitext(file)[1]
            if not extension:
                extension_folder = os.path.join(destination_directory, "unknown")
            else:
                extension_folder = os.path.join(destination_directory, extension[1:])
            executor.submit(move_file, file, extension_folder)

def main():
    source_dir = input("Введіть шлях до початкової директорії: ").strip("'\"")
    destination_dir = input("Введіть шлях до цільової директорії: ").strip("'\"")

    if not os.path.isdir(source_dir) or not os.path.isdir(destination_dir):
        print("Вказані шляхи повинні бути директоріями.")
        sys.exit(1)

    sort_files_by_extension(source_dir, destination_dir)

if __name__ == "__main__":
    main()
