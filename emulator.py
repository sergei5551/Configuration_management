import os
import sys
import tarfile
from pathlib import Path

from colorama import Fore, Style, init

# Инициализация Colorama
init(autoreset=True)

class VirtualFileSystem:
    def __init__(self, archive_file):
        self.archive = tarfile.open(archive_file, mode='r')
        self.current_dir = '/'

    def list_files(self, directory):
        """Список файлов в указанной директории."""
        root_prefix = self.archive.getnames()[0]

        if not directory:
            directory = self.current_dir
        else:
            if self.current_dir == "/":
                directory = self.current_dir + directory.replace("./", "")
            else:
                directory = self.current_dir + "/" + directory.replace("./", "")

            for member in self.archive.getmembers(): # Проверка на содержание каталога
                if member.path == root_prefix + directory:
                    break
            else:
                return

        # Учитываем корень архива
        file_list = []
        for member in self.archive.getmembers():
            if member.path.startswith(root_prefix + directory):
                relative_path = member.path[len(root_prefix + directory):].lstrip('/')
                if relative_path.count('/') == 0:  # Убедимся, что элемент находится прямо в текущей директории
                    file_list.append((member, relative_path))

        return sorted(file_list, key=lambda x: x[1])  # Возвращаем отсортированный список

    def change_directory(self, new_dir):
        """Переход в указанную директорию."""

        if new_dir in ('.', '/', './'):
            return
        elif new_dir == "":
            self.current_dir = "/"
        elif new_dir == '..':
            parent_dir = os.path.dirname(self.current_dir)
            self.current_dir = parent_dir

        else:
            # Формируем полный путь к новой директории, учитывая текущую директорию
            root_prefix = self.archive.getnames()[0]
            cur_str = new_dir.lstrip('./')
            full_path = root_prefix + os.path.join(self.current_dir, cur_str)
            # Проверяем, существует ли такая директория в архиве

            for member in self.archive.getmembers():
                if member.path == full_path:
                    self.current_dir += cur_str
                    break
            else:
                print(Fore.RED + f"Директория {new_dir} не найдена.")


def clear_screen():
    """Очистка экрана."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def main(archive_file):
    if not os.path.exists(archive_file):
        print(Fore.RED + "Архивный файл не найден!")
        sys.exit(1)

    vfs = VirtualFileSystem(archive_file)

    while True:
        prompt = f'{Fore.GREEN}{vfs.current_dir}> '
        command = input(prompt)
        args = command.split()

        if len(args) == 0:
            continue

        elif args[0] == 'ls':
            if len(args) > 1:
                directory = args[1]
            else:
                directory = None

            try:
                files = vfs.list_files(directory)
                for member, relative_path in files:
                    if member.isdir():  # Если это папка, выведем её синим цветом
                        print(Fore.BLUE + relative_path)
                    else:  # Иначе выведем обычным цветом
                        print(relative_path)
            except Exception as e:
                print(Fore.RED + f"Директория {directory} не найдена.")

        elif args[0] == 'cd':
            if len(args) > 2:
                print("Введено слишком много аргументов")
            elif len(args) == 1:
                vfs.change_directory('')
            elif len(args) == 2:
                vfs.change_directory(args[1])

        elif args[0] == 'clear' or args[0] == 'clr':
            clear_screen()

        elif args[0] == 'echo':
            print(end="")
            if len(args) > 1:
                for word in args[1:]:
                    print(word, end=" ")
            print()

        elif args[0] == 'exit' or args[0] == 'quit':
            print("Выход из программы...")
            sys.exit(0)

        else:
            print(f"Команда '{command}' не найдена.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Необходимо указать файл образа виртуальной файловой системы.")
        sys.exit(1)

    archive_file = sys.argv[1]
    main(archive_file)