from __future__ import annotations

from pathlib import Path
import tkinter as tk

import pytest

from git_sim.application.scenario_stepper import ScenarioStepper, TimelineNavigator
from git_sim.presentation.gui_app import GitSimWindow


def _make_root_or_skip() -> tk.Tk:
    try:
        root = tk.Tk()
    except tk.TclError as exc:
        pytest.skip(f"Tk is unavailable in this environment: {exc}")
    root.withdraw()
    return root


def test_gui_window_refresh_renders_dag_and_panels() -> None:
    scenario = Path(__file__).parents[2] / "scenarios" / "demo.yaml"
    stepper = ScenarioStepper.from_file(scenario)
    navigator = TimelineNavigator(stepper.snapshots)

    root = _make_root_or_skip()
    try:
        window = GitSimWindow(root, navigator)

        # __init__ already calls _refresh(), but call explicitly once more for clarity.
        window._refresh()

        wd_text = window.wd_text.get("1.0", "end-1c")
        repo_text = window.repo_text.get("1.0", "end-1c")

        assert wd_text != ""
        assert "branch:" in repo_text

        assert window.dag_canvas is not None
        assert len(window.dag_canvas.find_all()) > 0
    finally:
        root.destroy()
