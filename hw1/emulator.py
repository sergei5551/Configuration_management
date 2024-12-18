import os
import sys
import tarfile
from colorama import Fore, Style, init

# Инициализация Colorama
init(autoreset=True)

class VirtualFileSystem:
    def __init__(self, archive_file):
        if not os.path.exists(archive_file):
            raise FileNotFoundError(f"Файл архива {archive_file} не найден.")

        self.archive = tarfile.open(archive_file, mode='r')
        self.root_prefix = self.archive.getnames()[0]
        self.current_dir = '/'

    def list_files(self, directory=None):
        """Список файлов в указанной директории."""
        if not directory:
            directory = self.current_dir
        else:
            if self.current_dir == "/":
                directory = self.current_dir + directory.replace("./", "")
            else:
                directory = os.path.join(self.current_dir, directory.replace("./", ""))

            for member in self.archive.getmembers():  # Проверка на наличие каталога
                if member.path == self.root_prefix + directory:
                    break
            else:
                return

        # Учитываем корень архива
        file_list = []
        for member in self.archive.getmembers():
            if member.path.startswith(self.root_prefix + directory):
                relative_path = member.path[len(self.root_prefix + directory):].lstrip('/')
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
            cur_str = new_dir.lstrip('./')
            full_path = os.path.join(self.root_prefix, self.current_dir, cur_str)
            # Проверяем, существует ли такая директория в архиве

            for member in self.archive.getmembers():
                if member.path == full_path:
                    self.current_dir = os.path.join(self.current_dir, cur_str)
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
            print(Fore.RED + f"Ошибка при выполнении команды ls: {e}")

    def handle_cd(self, new_dir):
        if len(new_dir) > 2:
            print("Введено слишком много аргументов")
        elif len(new_dir) == 1:
            self.change_directory('')
        elif len(new_dir) == 2:
            self.change_directory(new_dir[1])

    def handle_cat(self, filename):
        try:
            member = self.archive.getmember(os.path.join(self.root_prefix, self.current_dir, filename))
            if member.isfile():
                with self.archive.extractfile(member) as file_obj:
                    content = file_obj.read().decode('utf-8', errors='ignore')
                    print(content)
            else:
                print(Fore.RED + f"{filename} не является файлом.")
        except KeyError:
            print(Fore.RED + f"Файл {filename} не найден.")

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

        elif args[0] == 'cat':
            if len(args) != 2:
                print("Неверный формат команды cat. Используйте: cat <имя_файла>")
            else:
                self.handle_cat(args[1])

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

def execute_startup_script(vfs, script_path):
    """Выполнение стартового скрипта."""
    try:
        member = vfs.archive.getmember(script_path)
        if member.isfile():
            with vfs.archive.extractfile(member) as file_obj:
                commands = file_obj.read().decode('utf-8').splitlines()
                for cmd in commands:
                    vfs.run_command(cmd.strip())
        else:
            print(Fore.RED + f"Сценарий {script_path} не является файлом.")
    except KeyError:
        print(Fore.RED + f"Сценарий {script_path} не найден.")

def main(username, archive_file, startup_script):
    try:
        vfs = VirtualFileSystem(archive_file)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    execute_startup_script(vfs, startup_script)

    while True:
        prompt = f'{Style.BRIGHT}{Fore.GREEN}{username}:{vfs.current_dir}$ '
        command = input(prompt)
        vfs.run_command(command)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Необходимо указать имя пользователя, файл образа виртуальной файловой системы и стартовый скрипт.")
        sys.exit(1)

    username = sys.argv[1]
    archive_file = sys.argv[2]
    startup_script = sys.argv[3]
    main(username, archive_file, startup_script)