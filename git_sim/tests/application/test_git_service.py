from git_sim.application.git_service import GitService


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
