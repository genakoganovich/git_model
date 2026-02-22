from git_sim.presentation.ascii_renderer import AsciiRenderer
from git_sim.domain.status import StatusResult


def test_ascii_renderer_basic():
    wd = {"a.txt": "1"}
    index = {"a.txt": "1"}
    head = {"a.txt": "1"}

    status = StatusResult(
        untracked=[],
        staged=[],
        modified=[]
    )

    output = AsciiRenderer.render_state(wd, index, head, status)

    assert "Working Directory" in output
    assert "Index" in output
    assert "Repository (HEAD)" in output
    assert "a.txt: 1" in output