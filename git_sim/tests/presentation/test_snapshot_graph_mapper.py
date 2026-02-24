from pathlib import Path
from git_sim.application.scenario_stepper import ScenarioStepper
from git_sim.presentation.snapshot_graph_mapper import map_snapshot_to_graph


def test_mapper_contains_head_branch_parent_edges():
    scenario = Path(__file__).parents[2] / "scenarios" / "demo.yaml"
    snap = ScenarioStepper.from_file(scenario).snapshots[-1]
    nodes, edges = map_snapshot_to_graph(snap)

    ids = {n.id for n in nodes}
    assert "HEAD" in ids
    assert snap.current_branch in ids
    assert any(e.source == "HEAD" and e.kind == "points_to" for e in edges)
    assert any(e.kind == "parent" for e in edges)
