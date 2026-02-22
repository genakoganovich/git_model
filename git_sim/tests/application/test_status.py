from git_sim.application.git_service import GitService


def test_untracked_file():
    git = GitService()

    git.working_dir.write("a.txt", "1")

    status = git.status()

    assert status.untracked == ["a.txt"]
    assert status.staged == []
    assert status.modified == []

def test_staged_file():
    git = GitService()

    git.working_dir.write("a.txt", "1")
    git.add("a.txt")

    status = git.status()

    assert status.untracked == []
    assert status.modified == []
    assert status.staged == ["a.txt"]

def test_modified_after_add():
    git = GitService()

    git.working_dir.write("a.txt", "1")
    git.add("a.txt")

    git.working_dir.write("a.txt", "2")

    status = git.status()

    assert status.modified == ["a.txt"]

def test_clean_after_commit():
    git = GitService()

    git.working_dir.write("a.txt", "1")
    git.add("a.txt")
    git.commit()

    status = git.status()

    assert status.untracked == []
    assert status.modified == []
    assert status.staged == []