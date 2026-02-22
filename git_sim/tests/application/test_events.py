from git_sim.application.git_service import GitService


def test_add_generates_event():
    git = GitService()
    git.working_dir.write("a.txt", "1")

    git.add("a.txt")

    event = git.last_event
    assert event.type == "add"
    assert event.source == "working_dir"
    assert event.target == "index"
    assert event.filename == "a.txt"


def test_commit_generates_event():
    git = GitService()
    git.working_dir.write("a.txt", "1")
    git.add("a.txt")
    git.commit()

    event = git.last_event
    assert event.type == "commit"
    assert event.source == "index"
    assert event.target == "repository"