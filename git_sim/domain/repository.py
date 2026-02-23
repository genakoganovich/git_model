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