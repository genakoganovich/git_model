from git_sim.domain.working_directory import WorkingDirectory
from git_sim.domain.index import Index
from git_sim.domain.commit import Commit
from git_sim.domain.repository import Repository
from git_sim.domain.exceptions import NothingToCommitError
from git_sim.domain.status import StatusResult
from git_sim.application.events import GitEvent

class GitService:
    def __init__(self):
        self.working_dir = WorkingDirectory()
        self.index = Index()
        self.repo = Repository()
        self.last_event = None

    def init(self):
        self.repo = Repository()
        self.last_event = GitEvent(
            type="init",
            source=None,
            target="repository"
        )

    def add(self, filename: str):
        content = self.working_dir.read(filename)
        self.index.add(filename, content)

        self.last_event = GitEvent(
            type="add",
            source="working_dir",
            target="index",
            filename=filename
        )

    def commit(self):
        snapshot = self.index.snapshot()

        if not snapshot:
            raise NothingToCommitError("nothing to commit")

        if self.repo.head and snapshot == self.repo.head.snapshot:
            raise NothingToCommitError("nothing to commit")

        commit = Commit(snapshot, self.repo.head)
        self.repo.add_commit(commit)

        self.last_event = GitEvent(
            type="commit",
            source="index",
            target="repository"
        )

    def branch(self, name: str):
        self.repo.create_branch(name)

        self.last_event = GitEvent(
            type="branch",
            source="repository",
            target="repository",
            filename=name,
        )

    def checkout(self, name: str):
        self.repo.checkout(name)

        self.last_event = GitEvent(
            type="checkout",
            source="repository",
            target="repository",
            filename=name,
        )

    def status(self):
        wd = self.working_dir.snapshot()
        index = self.index.snapshot()
        head = self.repo.head.snapshot if self.repo.head else {}

        untracked = []
        staged = []
        modified = []

        # untracked: есть в WD, нет в index
        for filename in wd:
            if filename not in index:
                untracked.append(filename)

        # modified: есть в index, но отличается от WD
        for filename in index:
            if filename in wd and wd[filename] != index[filename]:
                modified.append(filename)

        # staged: отличается от HEAD
        for filename in index:
            if filename not in head or head[filename] != index[filename]:
                staged.append(filename)

        return StatusResult(untracked, staged, modified)

    def get_render_data(self):
        wd = self.working_dir.snapshot()
        index = self.index.snapshot()
        head = self.repo.head.snapshot if self.repo.head else None
        status = self.status()
        event = self.last_event

        return wd, index, head, status, event
