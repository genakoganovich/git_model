from git_sim.domain.working_directory import WorkingDirectory
from git_sim.domain.index import Index
from git_sim.domain.commit import Commit
from git_sim.domain.repository import Repository
from git_sim.domain.exceptions import NothingToCommitError

class GitService:
    def __init__(self):
        self.working_dir = WorkingDirectory()
        self.index = Index()
        self.repo = Repository()

    def init(self):
        self.repo = Repository()

    def add(self, filename: str):
        content = self.working_dir.read(filename)
        self.index.add(filename, content)

    def commit(self):
        snapshot = self.index.snapshot()

        if not snapshot:
            raise NothingToCommitError("nothing to commit")

        if self.repo.head and snapshot == self.repo.head.snapshot:
            raise NothingToCommitError("nothing to commit")

        commit = Commit(snapshot, self.repo.head)
        self.repo.add_commit(commit)