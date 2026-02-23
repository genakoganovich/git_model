import pytest

from git_sim.domain.repository import Repository
from git_sim.domain.commit import Commit


def test_repository_starts_empty():
    repo = Repository()

    assert repo.head is None
    assert repo.list_commits() == []


def test_add_commit_sets_head():
    repo = Repository()
    commit = Commit({"a.txt": "1"})

    repo.add_commit(commit)

    assert repo.head is commit
    assert repo.list_commits() == [commit]


def test_multiple_commits_update_head():
    repo = Repository()

    c1 = Commit({"a.txt": "1"})
    repo.add_commit(c1)

    c2 = Commit({"a.txt": "2"}, parent=c1)
    repo.add_commit(c2)

    assert repo.head is c2

    commits = repo.list_commits()
    # HEAD должен быть первый
    assert commits[0] is c2
    # parent от HEAD
    assert commits[1] is c1
    # в конце списка нет лишних коммитов
    assert len(commits) == 2


def test_create_branch_points_to_current_head():
    repo = Repository()
    base_commit = Commit({"a.txt": "1"})
    repo.add_commit(base_commit)

    repo.create_branch("feature")

    branches = repo.list_branches()
    assert branches["main"] is base_commit
    assert branches["feature"] is base_commit


def test_checkout_switches_active_branch_head():
    repo = Repository()

    main_commit = Commit({"a.txt": "main"})
    repo.add_commit(main_commit)
    repo.create_branch("feature")

    repo.checkout("feature")
    feature_commit = Commit({"a.txt": "feature"}, parent=main_commit)
    repo.add_commit(feature_commit)

    assert repo.current_branch == "feature"
    assert repo.head is feature_commit

    branches = repo.list_branches()
    assert branches["main"] is main_commit
    assert branches["feature"] is feature_commit


def test_create_existing_branch_raises_error():
    repo = Repository()

    repo.create_branch("feature")

    with pytest.raises(ValueError, match="Branch already exists"):
        repo.create_branch("feature")


def test_checkout_unknown_branch_raises_error():
    repo = Repository()

    with pytest.raises(ValueError, match="Branch does not exist"):
        repo.checkout("missing")
