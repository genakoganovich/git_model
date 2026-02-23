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