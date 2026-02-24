from pathlib import Path

from git_sim.application.scenario_stepper import ScenarioStepper, TimelineNavigator


def test_scenario_stepper_builds_snapshot_per_command():
    scenario = Path(__file__).parents[2] / "scenarios" / "demo.yaml"

    stepper = ScenarioStepper.from_file(scenario)

    assert len(stepper.snapshots) == 9
    assert stepper.snapshots[-1].current_branch == "feature"
    assert stepper.snapshots[-1].head == {"a.txt": "feature-v2"}


def test_scenario_stepper_tracks_checkout_state():
    scenario = Path(__file__).parents[2] / "scenarios" / "demo.yaml"

    stepper = ScenarioStepper.from_file(scenario)
    checkout_snapshot = stepper.snapshots[5]

    assert checkout_snapshot.command["cmd"] == "checkout"
    assert checkout_snapshot.current_branch == "feature"
    assert checkout_snapshot.wd == {"a.txt": "main-v1"}
    assert checkout_snapshot.index == {"a.txt": "main-v1"}


def test_timeline_navigator_clamps_bounds():
    scenario = Path(__file__).parents[2] / "scenarios" / "demo.yaml"
    stepper = ScenarioStepper.from_file(scenario)
    nav = TimelineNavigator(stepper.snapshots)

    nav.move_up()
    assert nav.index == 0

    nav.set_index(100)
    assert nav.index == len(stepper.snapshots) - 1

    nav.move_down()
    assert nav.index == len(stepper.snapshots) - 1
