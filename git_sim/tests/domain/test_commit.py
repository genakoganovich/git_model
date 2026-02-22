from git_sim.domain.commit import Commit


def test_commit_stores_snapshot():
    data = {"file.txt": "v1"}

    commit = Commit(data)

    assert commit.snapshot == {"file.txt": "v1"}


def test_commit_is_immutable_snapshot():
    data = {"file.txt": "v1"}
    commit = Commit(data)

    data["file.txt"] = "v2"

    # commit должен сохранить старое состояние
    assert commit.snapshot["file.txt"] == "v1"


def test_commit_has_unique_id():
    c1 = Commit({})
    c2 = Commit({})

    assert c1.id != c2.id


def test_commit_parent_link():
    parent = Commit({"a.txt": "1"})
    child = Commit({"a.txt": "2"}, parent=parent)

    assert child.parent is parent