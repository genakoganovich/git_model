1️⃣ Концептуальная модель Git (что именно визуализировать)
Рабочая директория (Working Directory)

Git — это три состояния данных (three trees model):

| Компонент            | Что это                             | Где живёт        |
|----------------------|-------------------------------------|------------------|
| Working Directory    | обычные файлы на диске              | файловая система |
| Index (Staging Area) | снимок, который готовится к коммиту | .git/index       |
| Repository           | история коммитов (объекты)          | .git/objects     |

Твоя симуляция должна отражать переходы состояния между этими тремя сущностями.

2️⃣ Минимальный функционал (первая версия)
Команды для реализации
git init
* создаётся .git
* создаётся пустой repository
* индекс пустой

Визуально:
```
Working Dir:  [ files ]
Index:        [ empty ]
Repository:   [ empty ]
```

git add file.txt

Что происходит:
* содержимое файла копируется в Index
* если файл изменится после add → index не меняется

Визуально:
```
Working Dir:  file.txt (v2)
Index:        file.txt (v1 snapshot)
Repository:   empty
```

Важно: индекс — это снимок, а не ссылка.

git commit
Что происходит:
* создаётся commit object
* commit указывает на tree
* tree указывает на blobs
* HEAD двигается

В упрощённой модели:
```
Repository:
Commit #1
└── file.txt (v1)
```

Index очищается?
Нет. Он остаётся, но совпадает с HEAD.

3️⃣ Архитектура симулятора
Ты можешь реализовать это как чистую модель + визуализатор.

🧠 Model layer

```
class WorkingDirectory:
    files: dict[str, str]  # filename -> content


class Index:
    files: dict[str, str]


class Commit:
    id: str
    snapshot: dict[str, str]
    parent: Optional["Commit"]


class Repository:
    commits: list[Commit]
    head: Optional[Commit]
```

🛠 Git Engine

```
class GitSimulator:
    def init(self): ...
    def add(self, filename): ...
    def commit(self, message): ...
```

4️⃣ Визуализация
🔹 Консольная ASCII-визуализация (быстро)
Для первого этапа:
```
+-------------------+
| Working Directory |
| file.txt (v2)     |
+-------------------+

+-------------------+
| Index             |
| file.txt (v1)     |
+-------------------+

+-------------------+
| Repository        |
| commit 1          |
+-------------------+
```

🔷 Как устроен настоящий Git
📦 Объектная модель Git

Git хранит всё как объекты:

1️⃣ Blob
* хранит содержимое файла
* это просто "байты файла"
* blob НЕ знает имя файла

2️⃣ Tree

* структура каталогов
* хранит:
  * имя файла
  * ссылку на blob
  * права доступа
* tree указывает на blobs и другие trees

3️⃣ Commit
* указывает на один tree
* указывает на родительский commit
* содержит метаданные (author, date, message)

Что происходит при git commit
1. Git берёт содержимое Index
2. Создаёт blob для каждого файла
3. Создаёт tree, который указывает на эти blobs
4. Создаёт commit, который указывает на tree
5. HEAD начинает указывать на новый commit

Это полноценный DAG объектов.