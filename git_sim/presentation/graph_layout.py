from __future__ import annotations
from git_sim.presentation.graph_view import GraphNode, GraphEdge


class GraphLayout:
    def compute(self, nodes: list[GraphNode], edges: list[GraphEdge]) -> dict[str, tuple[float, float]]:
        coords: dict[str, tuple[float, float]] = {}

        commit_ids = [n.id for n in nodes if n.kind == "commit"]
        commit_ids_sorted = sorted(commit_ids)
        for i, cid in enumerate(commit_ids_sorted):
            coords[cid] = (float(i), 0.0)

        max_x = float(len(commit_ids_sorted) - 1) if commit_ids_sorted else 0.0
        branch_x = max_x + 2.0
        head_x = branch_x + 2.0

        branches = sorted([n.id for n in nodes if n.kind == "branch"])
        active = _find_active_branch(edges, branches)
        step = 1.0
        temp = {b: -(i + 1) * step for i, b in enumerate(branches)}
        shift = -temp.get(active, 0.0)
        for b in branches:
            coords[b] = (branch_x, temp[b] + shift)

        for h in [n.id for n in nodes if n.kind == "head"]:
            coords[h] = (head_x, 0.0)

        return coords


def _find_active_branch(edges: list[GraphEdge], branches: list[str]) -> str:
    for e in edges:
        if e.kind == "points_to" and e.source == "HEAD" and e.target in branches:
            return e.target
    return "main" if "main" in branches else (branches[0] if branches else "")
