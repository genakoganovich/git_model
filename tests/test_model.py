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