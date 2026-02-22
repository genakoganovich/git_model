class Repository:
    def __init__(self):
        self._commits = []
        self._head = None

    @property
    def head(self):
        return self._head

    def add_commit(self, commit):
        self._commits.append(commit)
        self._head = commit

    def list_commits(self):
        return list(self._commits)