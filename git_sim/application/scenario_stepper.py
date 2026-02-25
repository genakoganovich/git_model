from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from git_sim.application.git_service import GitService
from git_sim.application.yaml_player import YamlCommandPlayer, _parse_minimal_yaml


@dataclass(frozen=True)
class CommitNode:
    id: str
    parent_id: str | None
    files: dict[str, str]


@dataclass(frozen=True)
class ScenarioSnapshot:
    step_index: int
    command: dict[str, Any]
    wd: dict[str, str]
    index: dict[str, str]
    head: dict[str, str]
    current_branch: str
    branch_heads: dict[str, str | None]
    commit_nodes: tuple[CommitNode, ...]
    status_untracked: list[str]
    status_staged: list[str]
    status_modified: list[str]
    event_type: str | None
    log_lines: list[str]
    show_snapshot: dict[str, str]


@dataclass(frozen=True)
class ScenarioStepper:
    snapshots: list[ScenarioSnapshot]

    @classmethod
    def from_file(cls, path: str | Path) -> "ScenarioStepper":
        with open(path, "r", encoding="utf-8") as f:
            payload = _parse_minimal_yaml(f.read())
        return cls.from_payload(payload)

    @classmethod
    def from_payload(cls, payload: Any) -> "ScenarioStepper":
        if not isinstance(payload, dict):
            raise ValueError("YAML root must be a mapping")

        commands = payload.get("commands")
        if not isinstance(commands, list):
            raise ValueError("YAML must contain 'commands' list")

        git = GitService()
        player = YamlCommandPlayer(git)
        snapshots: list[ScenarioSnapshot] = []

        for idx, item in enumerate(commands):
            player.run_command(item)
            snapshots.append(_build_snapshot(git, idx, item))

        return cls(snapshots=snapshots)


class TimelineNavigator:
    def __init__(self, snapshots: list[ScenarioSnapshot]):
        self._snapshots = snapshots
        self._index = 0

    @property
    def index(self) -> int:
        return self._index

    @property
    def snapshots(self) -> list[ScenarioSnapshot]:
        return self._snapshots

    @property
    def current(self) -> ScenarioSnapshot | None:
        if not self._snapshots:
            return None
        return self._snapshots[self._index]

    def set_index(self, index: int) -> None:
        if not self._snapshots:
            self._index = 0
            return

        self._index = max(0, min(index, len(self._snapshots) - 1))

    def move_up(self) -> None:
        self.set_index(self._index - 1)

    def move_down(self) -> None:
        self.set_index(self._index + 1)


def _build_snapshot(
    git: GitService,
    step_index: int,
    command: dict[str, Any],
) -> ScenarioSnapshot:
    wd, index, head, status, event = git.get_render_data()
    branches = git.repo.list_branches()

    branch_heads = {
        branch: (commit.id if commit is not None else None)
        for branch, commit in branches.items()
    }

    return ScenarioSnapshot(
        step_index=step_index,
        command=dict(command),
        wd=dict(wd),
        index=dict(index),
        head=dict(head or {}),
        current_branch=git.repo.current_branch,
        branch_heads=branch_heads,
        commit_nodes=_collect_commit_nodes(branches),
        status_untracked=list(status.untracked),
        status_staged=list(status.staged),
        status_modified=list(status.modified),
        event_type=(event.type if event else None),
        log_lines=list(git.last_log),
        show_snapshot=dict(git.last_show),
    )


def _collect_commit_nodes(branches: dict[str, Any]) -> tuple[CommitNode, ...]:
    nodes: list[CommitNode] = []
    seen: set[str] = set()

    for commit in branches.values():
        current = commit
        while current is not None and current.id not in seen:
            seen.add(current.id)
            nodes.append(
                CommitNode(
                    id=current.id,
                    parent_id=(current.parent.id if current.parent else None),
                    files=dict(current.snapshot),
                )
            )
            current = current.parent

    return tuple(nodes)
