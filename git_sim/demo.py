from git_sim.application.git_service import GitService
from git_sim.presentation.ascii_renderer import AsciiRenderer

git = GitService()

git.working_dir.write("a.txt", "1")
git.add("a.txt")
git.commit()

wd, index, head, status = git.get_render_data()

print(AsciiRenderer.render_state(wd, index, head, status))