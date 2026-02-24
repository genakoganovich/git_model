from pathlib import Path
import tkinter as tk

from git_sim.application.scenario_stepper import ScenarioStepper, TimelineNavigator
from git_sim.presentation.gui_app import GitSimWindow


def main() -> None:
    scenario_path = Path(__file__).parent / "scenarios" / "demo.yaml"
    stepper = ScenarioStepper.from_file(scenario_path)
    navigator = TimelineNavigator(stepper.snapshots)

    root = tk.Tk()
    root.geometry("1200x700")
    GitSimWindow(root, navigator)
    root.mainloop()


if __name__ == "__main__":
    main()
