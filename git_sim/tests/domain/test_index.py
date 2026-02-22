from git_sim.domain.index import Index


def test_add_and_snapshot():
    index = Index()

    index.add("file.txt", "data")

    assert index.snapshot() == {"file.txt": "data"}


def test_snapshot_is_copy():
    index = Index()
    index.add("a.txt", "1")

    snap = index.snapshot()
    snap["a.txt"] = "changed"

    assert index.snapshot()["a.txt"] == "1"


def test_clear_removes_all_files():
    index = Index()
    index.add("a.txt", "1")
    index.add("b.txt", "2")

    index.clear()

    assert index.snapshot() == {}