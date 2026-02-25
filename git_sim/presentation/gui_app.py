from __future__ import annotations

import tkinter as tk

from git_sim.application.scenario_stepper import TimelineNavigator
from git_sim.presentation.graph_layout import GraphLayout
from git_sim.presentation.canvas_dag_renderer import CanvasDagRenderer
from git_sim.presentation.snapshot_graph_mapper import map_snapshot_to_graph


class GitSimWindow:
    def __init__(self, root: tk.Tk, navigator: TimelineNavigator):
        self.root = root
        self.navigator = navigator
        self.root.title("Git Simulation")

        self.graph_layout = GraphLayout()
        self.dag_canvas: tk.Canvas | None = None
        self.canvas_renderer: CanvasDagRenderer | None = None

        self.wd_text: tk.Text
        self.index_text: tk.Text
        self.repo_text: tk.Text
        self.status_text: tk.Text
        self.diff_text: tk.Text
        self.commands_list: tk.Listbox

        self._build_layout()
        self._bind_events()
        self._fill_commands()
        self._sync_selection()
        self._refresh()

    def _build_layout(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        top = tk.Frame(self.root)
        top.grid(row=0, column=0, sticky="nsew", padx=6, pady=(6, 3))
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=1)
        top.columnconfigure(2, weight=1)
        top.columnconfigure(3, weight=1)
        top.columnconfigure(4, weight=2)
        top.rowconfigure(0, weight=1)

        bottom = tk.Frame(self.root)
        bottom.grid(row=1, column=0, sticky="nsew", padx=6, pady=(3, 6))
        bottom.columnconfigure(0, weight=2)
        bottom.columnconfigure(1, weight=1)
        bottom.rowconfigure(0, weight=1)

        self.wd_text = self._make_text_panel(top, "Working Directory", 0, 0)
        self.index_text = self._make_text_panel(top, "Index", 0, 1)
        self.repo_text = self._make_text_panel(top, "Repository", 0, 2)
        self.status_text = self._make_text_panel(top, "Status", 0, 3)
        self.diff_text = self._make_text_panel(top, "Diff", 0, 4)

        dag_frame = tk.LabelFrame(bottom, text="DAG")
        dag_frame.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)
        self.dag_canvas = tk.Canvas(dag_frame, bg="white")
        self.dag_canvas.pack(fill="both", expand=True)
        self.canvas_renderer = CanvasDagRenderer(self.dag_canvas)

        self.commands_list = self._make_list_panel(bottom, "Scenario Commands", 0, 1)

    def _make_text_panel(self, parent: tk.Widget, title: str, row: int, col: int) -> tk.Text:
        frame = tk.LabelFrame(parent, text=title)
        frame.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
        parent.rowconfigure(row, weight=1)
        parent.columnconfigure(col, weight=1)

        text = tk.Text(frame, wrap="none")
        text.pack(fill="both", expand=True)
        text.configure(state="disabled")
        return text

    def _make_list_panel(self, parent: tk.Widget, title: str, row: int, col: int) -> tk.Listbox:
        frame = tk.LabelFrame(parent, text=title)
        frame.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
        parent.rowconfigure(row, weight=1)
        parent.columnconfigure(col, weight=1)

        listbox = tk.Listbox(frame, exportselection=False)
        listbox.pack(fill="both", expand=True)
        return listbox

    def _bind_events(self) -> None:
        self.root.bind("<Up>", self._on_up)
        self.root.bind("<Down>", self._on_down)

        # Intercept arrows at widget level to avoid double step from
        # Listbox class default navigation + our Timeline navigation.
        self.commands_list.bind("<Up>", self._on_up)
        self.commands_list.bind("<Down>", self._on_down)
        self.commands_list.bind("<<ListboxSelect>>", self._on_select)

    def _fill_commands(self) -> None:
        self.commands_list.delete(0, tk.END)
        for snap in self.navigator.snapshots:
            self.commands_list.insert(tk.END, _format_command(snap.command))

    def _sync_selection(self) -> None:
        if not self.navigator.snapshots:
            return
        self.commands_list.selection_clear(0, tk.END)
        self.commands_list.selection_set(self.navigator.index)
        self.commands_list.activate(self.navigator.index)
        self.commands_list.see(self.navigator.index)

    def _on_up(self, _event: tk.Event) -> str:
        self.navigator.move_up()
        self._sync_selection()
        self._refresh()
        return "break"

    def _on_down(self, _event: tk.Event) -> str:
        self.navigator.move_down()
        self._sync_selection()
        self._refresh()
        return "break"

    def _on_select(self, _event: tk.Event) -> None:
        selection = self.commands_list.curselection()
        if not selection:
            return
        self.navigator.set_index(int(selection[0]))
        self._refresh()

    def _refresh(self) -> None:
        snap = self.navigator.current
        if snap is None:
            self._set_text(self.wd_text, "")
            self._set_text(self.index_text, "")
            self._set_text(self.repo_text, "")
            self._set_text(self.status_text, "")
            self._set_text(self.diff_text, "")
            return

        self._set_text(self.wd_text, _format_mapping(snap.wd))
        self._set_text(self.index_text, _format_mapping(snap.index))
        self._set_text(
            self.repo_text,
            _format_repository_text(
                current_branch=snap.current_branch,
                head=snap.head,
                event_type=snap.event_type,
            ),
        )
        self._set_text(
            self.status_text,
            _format_status_text(
                untracked=snap.status_untracked,
                staged=snap.status_staged,
                modified=snap.status_modified,
            ),
        )
        self._set_text(
            self.diff_text,
            _build_diff_text(head=snap.head, index=snap.index, wd=snap.wd),
        )

        nodes, edges = map_snapshot_to_graph(snap)
        coords = self.graph_layout.compute(nodes, edges)
        if self.canvas_renderer is not None:
            self.canvas_renderer.draw(nodes, edges, coords)

    @staticmethod
    def _set_text(widget: tk.Text, text: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert("1.0", text)
        widget.configure(state="disabled")


def _format_mapping(data: dict[str, str]) -> str:
    if not data:
        return "(empty)"
    lines = []
    for name in sorted(data):
        lines.append(f"{name}: {data[name]}")
    return "\n".join(lines)


def _format_repository_text(
    current_branch: str,
    head: dict[str, str],
    event_type: str | None,
) -> str:
    lines = [f"branch: {current_branch}", ""]
    lines.append("HEAD snapshot:")
    lines.append(_format_mapping(head))
    lines.append("")
    lines.append(f"event: {event_type or '-'}")
    return "\n".join(lines)


def _format_status_text(
    untracked: list[str],
    staged: list[str],
    modified: list[str],
) -> str:
    lines = ["Status:", ""]
    lines.append(f"untracked: {sorted(untracked)}")
    lines.append(f"staged: {sorted(staged)}")
    lines.append(f"modified: {sorted(modified)}")
    return "\n".join(lines)


def _build_diff_text(head: dict[str, str], index: dict[str, str], wd: dict[str, str]) -> str:
    lines = ["HEAD -> INDEX", ""]
    lines.extend(_build_pair_diff(old=head, new=index))
    lines.append("")
    lines.append("INDEX -> WD")
    lines.append("")
    lines.extend(_build_pair_diff(old=index, new=wd))
    return "\n".join(lines)


def _build_pair_diff(old: dict[str, str], new: dict[str, str]) -> list[str]:
    added = sorted(name for name in new if name not in old)
    deleted = sorted(name for name in old if name not in new)
    modified = sorted(name for name in old if name in new and old[name] != new[name])

    lines: list[str] = []

    for name in added:
        lines.append(f"A {name}")
    for name in deleted:
        lines.append(f"D {name}")
    for name in modified:
        lines.append(f"M {name}")
        lines.append(f"- {old[name]}")
        lines.append(f"+ {new[name]}")

    if not lines:
        lines.append("(no changes)")

    return lines


def _format_command(command: dict[str, object]) -> str:
    cmd = command.get("cmd", "?")
    if cmd == "write":
        return f"write {command.get('filename', '?')}"
    if cmd == "add":
        return f"add {command.get('filename', '?')}"
    if cmd in {"branch", "checkout"}:
        return f"{cmd} {command.get('name', '?')}"
    return str(cmd)
