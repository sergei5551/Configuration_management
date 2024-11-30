import os
import sys
import tarfile
from colorama import Fore, init

# Инициализация Colorama
init(autoreset=True)

class VirtualFileSystem:
    def __init__(self, archive_file):
        self.archive = tarfile.open(archive_file, mode='r')
        self.current_dir = '/'

    def list_files(self, directory=None):
        """Список файлов в указанной директории."""
        root_prefix = self.archive.getnames()[0]

        if not directory:
            directory = self.current_dir
        else:
            if self.current_dir == "/":
                directory = self.current_dir + directory.replace("./", "")
            else:
                directory = self.current_dir + "/" + directory.replace("./", "")

            for member in self.archive.getmembers():  # Проверка на наличие каталога
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

    def handle_ls(self, directory=None):
        try:
            files = self.list_files(directory)
            for member, relative_path in files:
                if member.isdir():  # Если это папка, выведем её синим цветом
                    print(Fore.BLUE + relative_path)
                else:  # Иначе выведем обычным цветом
                    print(relative_path)
        except Exception as e:
            print(Fore.RED + f"Директория {directory} не найдена.")

    def handle_cd(self, new_dir):
        if len(new_dir) > 2:
            print("Введено слишком много аргументов")
        elif len(new_dir) == 1:
            self.change_directory('')
        elif len(new_dir) == 2:
            self.change_directory(new_dir[1])

    def handle_clear(self):
        clear_screen()

    def handle_echo(self, words):
        print(end="")
        if len(words) > 1:
            for word in words[1:]:
                print(word, end=" ")
        print()

    def handle_exit(self):
        print("Выход из программы...")
        sys.exit(0)

    def run_command(self, command):
        args = command.split()

        if len(args) == 0:
            return

        elif args[0] == 'ls':
            if len(args) > 1:
                directory = args[1]
            else:
                directory = None
            self.handle_ls(directory)

        elif args[0] == 'cd':
            self.handle_cd(args)

        elif args[0] == 'clear' or args[0] == 'clr':
            self.handle_clear()

        elif args[0] == 'echo':
            self.handle_echo(args)

        elif args[0] == 'exit' or args[0] == 'quit':
            self.handle_exit()

        else:
            print(f"Команда '{command}' не найдена.")

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
        vfs.run_command(command)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Необходимо указать файл образа виртуальной файловой системы.")
        sys.exit(1)

    archive_file = sys.argv[1]
    main(archive_file)