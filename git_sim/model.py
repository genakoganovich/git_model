# git_sim/model.py

class WorkingDirectory:
    def __init__(self):
        self._files = {}

    def write(self, filename: str, content: str):
        self._files[filename] = content

    def read(self, filename: str) -> str:
        return self._files[filename]

    def list_files(self):
        return dict(self._files)

class Index:
    def __init__(self):
        self._files = {}

    def add(self, filename: str, content: str):
        self._files[filename] = content

    def list_files(self):
        return dict(self._files)

    def clear(self):
        self._files.clear()

import uuid
from copy import deepcopy


class Commit:
    def __init__(self, snapshot: dict, parent=None):
        self.id = str(uuid.uuid4())
        self.snapshot = deepcopy(snapshot)
        self.parent = parent

class Repository:
    def __init__(self):
        self._commits = []
        self.head = None

    def add_commit(self, commit: Commit):
        self._commits.append(commit)
        self.head = commit

    def list_commits(self):
        return list(self._commits)