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


def test_log_returns_commits_from_head_to_root():
    git = GitService()

    git.working_dir.write("a.txt", "1")
    git.add("a.txt")
    git.commit()
    first = git.repo.head.id

    git.working_dir.write("a.txt", "2")
    git.add("a.txt")
    git.commit()
    second = git.repo.head.id

    output = git.log()

    assert output == [f"commit {second}", f"commit {first}"]
    assert git.last_log == output


def test_show_head_returns_head_snapshot():
    git = GitService()
    git.working_dir.write("a.txt", "1")
    git.add("a.txt")
    git.commit()

    snap = git.show("HEAD")

    assert snap == {"a.txt": "1"}
    assert git.last_show == {"a.txt": "1"}


def test_show_branch_ref_returns_branch_head_snapshot():
    git = GitService()
    git.working_dir.write("a.txt", "main")
    git.add("a.txt")
    git.commit()
    git.branch("feature")
    git.checkout("feature")
    git.working_dir.write("a.txt", "feature")
    git.add("a.txt")
    git.commit()

    snap = git.show("main")

    assert snap == {"a.txt": "main"}


def test_show_raises_for_unknown_ref():
    git = GitService()

    try:
        git.show("missing")
    except ValueError as exc:
        assert "Unknown ref" in str(exc)
    else:
        raise AssertionError("show should fail for unknown ref")


def test_unstage_restores_index_version_from_head():
    git = GitService()
    git.working_dir.write("a.txt", "v1")
    git.add("a.txt")
    git.commit()

    git.working_dir.write("a.txt", "v2")
    git.add("a.txt")
    git.unstage("a.txt")

    assert git.index.snapshot() == {"a.txt": "v1"}
    assert git.working_dir.snapshot() == {"a.txt": "v2"}
    assert git.status().staged == []
    assert git.status().modified == ["a.txt"]


def test_unstage_removes_newly_staged_file_when_absent_in_head():
    git = GitService()
    git.working_dir.write("new.txt", "data")
    git.add("new.txt")

    git.unstage("new.txt")

    assert git.index.snapshot() == {}
    assert git.working_dir.snapshot() == {"new.txt": "data"}
    assert git.status().untracked == ["new.txt"]
