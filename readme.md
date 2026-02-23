📦 PROJECT CONTEXT — Git Simulation (Python)
🎯 Цель проекта
Создать учебную симуляцию Git, чтобы:
* глубоко понять внутреннюю модель Git
* визуализировать состояние:
  * Working Directory
  * Index (Staging Area)
  * Repository
* отображать изменения после команд:
  * git init
  * git add
  * git commit
* позже — добавить ветки, checkout, merge
* рендерить состояние в ASCII
Проект ориентирован на понимание Git как DAG-модели, а не как набора CLI-команд.

🏗 Архитектура проекта
Проект разделён по принципу Domain / Application.

`git_simulator/
│
├── domain/
│   ├── working_directory.py
│   ├── index.py
│   ├── commit.py
│   └── repository.py
│
├── application/
│   └── git_service.py
│
├── rendering/
│   └── ascii_renderer.py
│
└── tests/`

🧠 Domain Model (текущее состояние)
1️⃣ WorkingDirectory
* хранит файлы как dict[str, str]
* операции:
  * create_file(name, content)
  * modify_file(name, content)
  * delete_file(name)
  * list_files()
Это просто модель файловой системы.

2️⃣ Index

хранит staged файлы
* операции:
  * add(filename, content)
  * clear()
  * snapshot()
  
Index — это staging area.

3️⃣ Commit
`from copy import deepcopy
import uuid


class Commit:
    def __init__(self, snapshot: dict, parent=None):
        self.id = str(uuid.uuid4())
        self.snapshot = deepcopy(snapshot)
        self.parent = parent`

Модель:
commit содержит snapshot (tree в упрощённой форме)
commit знает своего parent
история — это связанный список (будущий DAG)
⚠ Сейчас нет отдельной модели tree/blob — это запланировано.

4️⃣ Repository (новая версия)

`
class Repository:
    def __init__(self):
        # branch_name -> Commit
        self._branches = {"main": None}
        self._current_branch = "main"

    @property
    def current_branch(self):
        return self._current_branch

    @property
    def head(self):
        return self._branches[self._current_branch]

    def add_commit(self, commit):
        self._branches[self._current_branch] = commit

    def create_branch(self, name: str):
        if name in self._branches:
            raise ValueError("Branch already exists")

        self._branches[name] = self.head

    def checkout(self, name: str):
        if name not in self._branches:
            raise ValueError("Branch does not exist")

        self._current_branch = name

    def list_branches(self):
        return dict(self._branches)

    def list_commits(self):
        commits = []
        current = self.head

        while current is not None:
            commits.append(current)
            current = current.parent

        return commits
`

🧩 Важные архитектурные решения
❌ Мы больше не используем _commits
Причина:
Git — это DAG, а не список.
История строится через parent.

✅ HEAD — это указатель ветки
HEAD = _branches[_current_branch]
Мы реализуем модель реального Git:
branch -> commit -> parent -> parent

⚙ Application Layer (концепция)
GitService отвечает за orchestration:
init()
add()
commit()
branch()
checkout()
Domain не знает о CLI.

🖥 ASCII Renderer
Есть ASCII-визуализация состояния:
Working Directory
Index
Repository
стрелки переходов:
WD → Index
Index → Repo
Событие передаётся в render_state(event).

🧪 Тестирование
После каждого этапа добавляются pytest-тесты.
Текущий фокус:
тесты Repository после перехода на branch-based модель
запрет пустого commit (если index пуст → nothing to commit)
корректное движение HEAD
корректная parent-связь

📍 Текущий этап разработки

Мы:
перешли с list-based Repository на branch-based
удалили _commits
добавили list_commits() traversal
обсуждаем корректные тесты
планируем добавить:
полноценную DAG-модель
merge
detached HEAD
визуализацию графа

🚀 Долгосрочная цель
Симуляция должна позволять:
визуально понимать Git
видеть движение HEAD
видеть структуру DAG
руками перетаскивать файлы
видеть соответствующую git-команду

📌 ВАЖНО ДЛЯ НОВОГО ЧАТА
Проект — учебный.
Приоритеты:
Архитектурная корректность
Соответствие реальной модели Git
Маленькие итерации + pytest после каждой
Domain logic отделена от Application
Без избыточной сложности