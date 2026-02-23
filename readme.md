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