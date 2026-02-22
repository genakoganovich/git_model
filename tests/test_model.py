# tests/test_working_directory.py

from git_sim.model import WorkingDirectory


def test_write_and_read():
    wd = WorkingDirectory()
    wd.write("file.txt", "hello")

    assert wd.read("file.txt") == "hello"


def test_list_files():
    wd = WorkingDirectory()
    wd.write("a.txt", "1")
    wd.write("b.txt", "2")

    files = wd.list_files()
    assert files == {"a.txt": "1", "b.txt": "2"}

from git_sim.model import Index


def test_index_add():
    index = Index()
    index.add("file.txt", "data")

    assert index.list_files() == {"file.txt": "data"}

from git_sim.model import Commit


def test_commit_is_snapshot():
    data = {"file.txt": "v1"}
    commit = Commit(data)

    data["file.txt"] = "v2"

    assert commit.snapshot["file.txt"] == "v1"

from git_sim.model import Repository, Commit


def test_repository_add_commit():
    repo = Repository()
    commit = Commit({"a.txt": "1"})

    repo.add_commit(commit)

    assert repo.head == commit
    assert len(repo.list_commits()) == 1