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
        self.last_log = []
        self.last_show = {}

    def init(self):
        self.repo = Repository()
        self.last_event = GitEvent.init()
        self.last_log = []
        self.last_show = {}

    def add(self, filename: str):
        content = self.working_dir.read(filename)
        self.index.add(filename, content)

        self.last_event = GitEvent.add(filename)

    def commit(self):
        snapshot = self.index.snapshot()

        if not snapshot:
            raise NothingToCommitError("nothing to commit")

        if self.repo.head and snapshot == self.repo.head.snapshot:
            raise NothingToCommitError("nothing to commit")

        commit = Commit(snapshot, self.repo.head)
        self.repo.add_commit(commit)

        self.last_event = GitEvent.commit()

    def branch(self, name: str):
        self.repo.create_branch(name)

        self.last_event = GitEvent.branch(name)

    def checkout(self, name: str):
        self.repo.checkout(name)

        branch_head = self.repo.head
        branch_snapshot = branch_head.snapshot if branch_head else {}

        self.index = Index()
        self.working_dir = WorkingDirectory()
        for filename, content in branch_snapshot.items():
            self.index.add(filename, content)
            self.working_dir.write(filename, content)
        self.last_event = GitEvent.checkout(name)

    def log(self) -> list[str]:
        commits = self.repo.list_commits()
        lines = [f"commit {commit.id}" for commit in commits]
        self.last_log = lines
        self.last_event = GitEvent.log()
        return list(lines)

    def show(self, ref: str = "HEAD") -> dict[str, str]:
        commit = self._resolve_ref(ref)
        snapshot = dict(commit.snapshot) if commit is not None else {}
        self.last_show = snapshot
        self.last_event = GitEvent.show(ref)
        return dict(snapshot)

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

    def _resolve_ref(self, ref: str):
        if ref == "HEAD":
            return self.repo.head

        branches = self.repo.list_branches()
        if ref in branches:
            return branches[ref]

        raise ValueError(f"Unknown ref: {ref}")
