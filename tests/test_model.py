# tests/test_model.py

import pytest
from src.model import GitModel, GitError


class TestGitModelInit:

    def test_initial_state(self):
        """Проверяем, что модель создается в неинициализированном состоянии."""
        model = GitModel()
        assert model.repository is None
        assert model.working_directory == {}
        assert model.index == {}

    def test_init_creates_repository(self):
        """Проверяем, что 'init' успешно создает структуру репозитория."""
        model = GitModel()
        model.init()
        assert model.repository is not None
        assert 'commits' in model.repository
        assert 'branches' in model.repository
        assert model.repository['branches']['master'] is None

    def test_init_on_existing_repo_raises_error(self):
        """Проверяем, что повторный вызов 'init' вызывает ошибку."""
        model = GitModel()
        model.init()

        # pytest.raises проверяет, что код внутри 'with' вызвал указанное исключение
        with pytest.raises(GitError, match="Репозиторий уже существует."):
            model.init()


class TestGitModelAdd:

    @pytest.fixture
    def initialized_model(self):
        """Фикстура, которая создает и инициализирует модель перед каждым тестом."""
        model = GitModel()
        model.init()
        return model

    def test_add_before_init_raises_error(self):
        """Проверяем, что 'add' до 'init' вызывает ошибку."""
        model = GitModel()
        with pytest.raises(GitError, match="Это не Git-репозиторий."):
            model.add("file.txt")

    def test_add_non_existent_file_raises_error(self, initialized_model):
        """Проверяем, что 'add' несуществующего файла вызывает ошибку."""
        with pytest.raises(FileNotFoundError, match="Файл 'file.txt' не существует."):
            initialized_model.add("file.txt")

    def test_add_new_file_to_index(self, initialized_model):
        """Проверяем успешное добавление нового файла в индекс."""
        model = initialized_model

        # 1. Создаем файл
        model.create_file("task.md", "Первая задача")
        assert "task.md" in model.working_directory
        assert "task.md" not in model.index  # Убедимся, что в индексе его еще нет

        # 2. Добавляем его
        model.add("task.md")

        # 3. Проверяем результат
        assert "task.md" in model.index
        # Проверяем, что в индексе правильный хеш
        content_hash = model._hash_object("Первая задача", write=False)
        assert model.index["task.md"] == content_hash
        # Проверяем, что объект сохранился в "базе"
        assert content_hash in model._object_database

    def test_add_updates_existing_file_in_index(self, initialized_model):
        """Проверяем, что 'add' обновляет хеш для уже добавленного файла."""
        model = initialized_model

        # 1. Создаем и добавляем первую версию
        model.create_file("readme.txt", "Версия 1")
        model.add("readme.txt")
        hash_v1 = model.index["readme.txt"]

        # 2. Изменяем файл и добавляем снова
        model.edit_file("readme.txt", "Версия 2")
        model.add("readme.txt")
        hash_v2 = model.index["readme.txt"]

        # 3. Проверяем, что хеш в индексе изменился и не равен старому
        assert hash_v1 != hash_v2
        assert model._hash_object("Версия 2", write=False) == hash_v2