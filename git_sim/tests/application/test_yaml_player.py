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


def test_yaml_player_supports_log_and_show_commands():
    player = YamlCommandPlayer()

    git = player.play(
        {
            "commands": [
                {"cmd": "write", "filename": "a.txt", "content": "1"},
                {"cmd": "add", "filename": "a.txt"},
                {"cmd": "commit"},
                {"cmd": "log"},
                {"cmd": "show", "ref": "HEAD"},
            ]
        }
    )

    assert len(git.last_log) == 1
    assert git.last_log[0].startswith("commit ")
    assert git.last_show == {"a.txt": "1"}
