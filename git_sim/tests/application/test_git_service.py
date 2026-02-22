from git_sim.application.git_service import GitService


def test_full_flow():
    git = GitService()

    git.working_dir.write("file.txt", "hello")
    git.add("file.txt")
    git.commit()

    assert git.repo.head.snapshot == {"file.txt": "hello"}