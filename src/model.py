# git_simulator/model.py
import hashlib


class GitError(Exception):
    """Специальное исключение для ошибок симуляции Git."""
    pass


class GitModel:
    def __init__(self):
        """Инициализирует симулятор в состоянии 'не является репозиторием'."""
        self.working_directory = {}
        self.index = {}
        self.repository = None  # None означает отсутствие папки .git
        self.head = None
        self._object_database = {}

    def _hash_object(self, content: str, write: bool = True) -> str:
        """Хеширует содержимое и, если нужно, сохраняет в "базу данных объектов"."""
        sha1 = hashlib.sha1(content.encode('utf-8')).hexdigest()
        if write:
            self._object_database[sha1] = content
        return sha1

    def init(self):
        """Симулирует команду 'git init'."""
        if self.repository is not None:
            raise GitError("Репозиторий уже существует.")

        # Создаем "папку .git"
        self.repository = {
            'commits': {},
            'branches': {'master': None},  # Ветка master создана, но ни на что не указывает
            'HEAD': 'ref: refs/heads/master'  # HEAD указывает на ветку master
        }
        print("Инициализирован пустой Git-репозиторий")

    def create_file(self, filename: str, content: str):
        """Создает новый файл в рабочей папке."""
        if filename in self.working_directory:
            raise FileExistsError(f"Файл '{filename}' уже существует в рабочей папке.")
        self.working_directory[filename] = content
        print(f"Файл '{filename}' создан.")

    def edit_file(self, filename: str, content: str):
        """Изменяет существующий файл в рабочей папке."""
        if filename not in self.working_directory:
            raise FileNotFoundError(f"Файл '{filename}' не найден в рабочей папке.")
        self.working_directory[filename] = content
        print(f"Файл '{filename}' изменен.")

    def add(self, filename: str):
        """Симулирует 'git add <filename>'."""
        if self.repository is None:
            raise GitError("Это не Git-репозиторий.")

        if filename not in self.working_directory:
            raise FileNotFoundError(f"Файл '{filename}' не существует.")

        content = self.working_directory[filename]
        # Хешируем и сохраняем контент в базу объектов
        content_hash = self._hash_object(content)

        # Добавляем файл и его хеш в индекс
        self.index[filename] = content_hash
        print(f"Файл '{filename}' добавлен в индекс.")