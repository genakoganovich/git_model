from git_sim.application.events import GitEvent
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


def test_branch_generates_event():
    git = GitService()

    git.branch("feature")

    event = git.last_event
    assert event.type == "branch"
    assert event.source == "repository"
    assert event.target == "repository"
    assert event.filename == "feature"


def test_checkout_generates_event():
    git = GitService()
    git.branch("feature")

    git.checkout("feature")

    event = git.last_event
    assert event.type == "checkout"
    assert event.source == "repository"
    assert event.target == "repository"
    assert event.filename == "feature"


def test_event_factories_produce_expected_payloads():
    assert GitEvent.init() == GitEvent(type="init", source=None, target="repository")
    assert GitEvent.add("a.txt") == GitEvent(
        type="add", source="working_dir", target="index", filename="a.txt"
    )
    assert GitEvent.commit() == GitEvent(type="commit", source="index", target="repository")
    assert GitEvent.branch("feature") == GitEvent(
        type="branch", source="repository", target="repository", filename="feature"
    )
    assert GitEvent.checkout("feature") == GitEvent(
        type="checkout", source="repository", target="repository", filename="feature"
    )
