from pathlib import Path

from git_sim.application.scenario_stepper import ScenarioStepper
from git_sim.presentation.dag_renderer import DagRenderer


def test_dag_renderer_shows_head_branch_and_commit_links():
    scenario = Path(__file__).parents[2] / "scenarios" / "demo.yaml"
    stepper = ScenarioStepper.from_file(scenario)
    snap = stepper.snapshots[-1]

    output = DagRenderer.render(
        current_branch=snap.current_branch,
        branch_heads=snap.branch_heads,
        commit_nodes=snap.commit_nodes,
    )

    assert "HEAD -> feature" in output
    assert "main:" in output
    assert "feature:" in output
    assert "<-" in output
