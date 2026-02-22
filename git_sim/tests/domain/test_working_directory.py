import pytest
from git_sim.domain.working_directory import WorkingDirectory


def test_write_and_read_file():
    wd = WorkingDirectory()

    wd.write("file.txt", "hello")

    assert wd.read("file.txt") == "hello"


def test_snapshot_returns_copy():
    wd = WorkingDirectory()
    wd.write("a.txt", "1")

    snap = wd.snapshot()
    snap["a.txt"] = "modified"

    # внутреннее состояние не должно измениться
    assert wd.read("a.txt") == "1"


def test_read_missing_file_raises():
    wd = WorkingDirectory()

    with pytest.raises(KeyError):
        wd.read("missing.txt")