import pytest
from git_sim.application.git_service import GitService
from git_sim.domain.exceptions import NothingToCommitError


def test_commit_empty_index_raises():
    git = GitService()

    with pytest.raises(NothingToCommitError):
        git.commit()


def test_commit_same_as_head_raises():
    git = GitService()

    git.working_dir.write("a.txt", "1")
    git.add("a.txt")
    git.commit()

    # index всё ещё совпадает с HEAD
    with pytest.raises(NothingToCommitError):
        git.commit()