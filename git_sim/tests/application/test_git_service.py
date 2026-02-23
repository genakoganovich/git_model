from git_sim.application.git_service import GitService
from git_sim.domain.exceptions import NothingToCommitError


def test_full_flow():
    git = GitService()

    git.working_dir.write("file.txt", "hello")
    git.add("file.txt")
    git.commit()

    assert git.repo.head.snapshot == {"file.txt": "hello"}


def test_branch_creates_new_branch_on_current_head():
    git = GitService()
    git.working_dir.write("a.txt", "1")
    git.add("a.txt")
    git.commit()

    main_head = git.repo.head
    git.branch("feature")

    branches = git.repo.list_branches()
    assert branches["main"] is main_head
    assert branches["feature"] is main_head


def test_checkout_switches_current_branch():
    git = GitService()
    git.branch("feature")

    git.checkout("feature")

    assert git.repo.current_branch == "feature"


def test_branch_and_checkout_keep_branch_heads_independent():
    git = GitService()

    git.working_dir.write("a.txt", "main")
    git.add("a.txt")
    git.commit()
    main_head = git.repo.head

    git.branch("feature")
    git.checkout("feature")

    git.working_dir.write("a.txt", "feature")
    git.add("a.txt")
    git.commit()

    branches = git.repo.list_branches()
    assert git.repo.current_branch == "feature"
    assert branches["main"] is main_head
    assert branches["feature"] is git.repo.head
    assert branches["feature"] is not branches["main"]


def test_checkout_resets_index_and_working_tree_to_branch_head():
    git = GitService()

    git.working_dir.write("a.txt", "main")
    git.add("a.txt")
    git.commit()

    git.branch("feature")
    git.checkout("feature")
    git.working_dir.write("a.txt", "feature")
    git.add("a.txt")
    git.commit()

    git.checkout("main")

    assert git.index.snapshot() == {"a.txt": "main"}
    assert git.working_dir.snapshot() == {"a.txt": "main"}
    assert git.status().staged == []

    try:
        git.commit()
    except NothingToCommitError:
        pass
    else:
        raise AssertionError("checkout should not leave staged changes on target branch")
