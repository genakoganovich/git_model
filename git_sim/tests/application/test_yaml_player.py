from pathlib import Path

import pytest

from git_sim.application.yaml_player import YamlCommandPlayer


def test_yaml_player_runs_demo_scenario_and_updates_branch_heads():
    scenario = Path(__file__).parents[2] / "scenarios" / "demo.yaml"

    player = YamlCommandPlayer()
    git = player.play_file(scenario)

    branches = git.repo.list_branches()
    assert git.repo.current_branch == "feature"
    assert branches["main"].snapshot == {"a.txt": "main-v1"}
    assert branches["feature"].snapshot == {"a.txt": "feature-v2"}


def test_yaml_player_rejects_unknown_command():
    player = YamlCommandPlayer()

    with pytest.raises(ValueError, match="Unknown command"):
        player.play({"commands": [{"cmd": "rebase"}]})
