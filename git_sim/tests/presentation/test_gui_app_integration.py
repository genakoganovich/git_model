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


def test_scenario_commands_down_moves_exactly_one_step() -> None:
    scenario = Path(__file__).parents[2] / "scenarios" / "demo.yaml"
    stepper = ScenarioStepper.from_file(scenario)
    navigator = TimelineNavigator(stepper.snapshots)

    root = _make_root_or_skip()
    try:
        window = GitSimWindow(root, navigator)

        assert navigator.index == 0

        # In withdrawn/headless Tk sessions, key events may not be delivered
        # to Listbox due to focus handling. Call the handler directly to verify
        # single-step navigation contract.
        window._on_down(tk.Event())

        assert navigator.index == 1
        assert window.commands_list.curselection() == (1,)
    finally:
        root.destroy()


def test_repository_panel_renders_log_and_show_sections() -> None:
    stepper = ScenarioStepper.from_payload(
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
    navigator = TimelineNavigator(stepper.snapshots)
    navigator.set_index(4)

    root = _make_root_or_skip()
    try:
        window = GitSimWindow(root, navigator)
        repo_text = window.repo_text.get("1.0", "end-1c")

        assert "log:" in repo_text
        assert "show:" in repo_text
        assert "a.txt: 1" in repo_text
    finally:
        root.destroy()


def test_status_panel_renders_unstage_hint() -> None:
    stepper = ScenarioStepper.from_payload(
        {
            "commands": [
                {"cmd": "write", "filename": "a.txt", "content": "v1"},
                {"cmd": "add", "filename": "a.txt"},
                {"cmd": "commit"},
                {"cmd": "write", "filename": "a.txt", "content": "v2"},
                {"cmd": "add", "filename": "a.txt"},
                {"cmd": "unstage", "filename": "a.txt"},
            ]
        }
    )
    navigator = TimelineNavigator(stepper.snapshots)
    navigator.set_index(5)

    root = _make_root_or_skip()
    try:
        window = GitSimWindow(root, navigator)
        status_text = window.status_text.get("1.0", "end-1c")

        assert "last action: unstage a.txt (index -> working_dir)" in status_text
    finally:
        root.destroy()
