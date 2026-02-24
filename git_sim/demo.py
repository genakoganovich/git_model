from pathlib import Path

from git_sim.application.yaml_player import YamlCommandPlayer
from git_sim.presentation.ascii_renderer import AsciiRenderer

scenario_path = Path(__file__).parent / "scenarios" / "demo.yaml"
player = YamlCommandPlayer()
git = player.play_file(scenario_path)

wd, index, head, status, event = git.get_render_data()

print(
    AsciiRenderer.render_state(
        wd,
        index,
        head,
        status,
        event,
    )
)
