from __future__ import annotations
from git_sim.application.scenario_stepper import ScenarioSnapshot
from git_sim.presentation.graph_view import GraphNode, GraphEdge


def map_snapshot_to_graph(snap: ScenarioSnapshot) -> tuple[list[GraphNode], list[GraphEdge]]:
    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []

    nodes.append(GraphNode(id="HEAD", kind="head", label="HEAD"))
    edges.append(GraphEdge(source="HEAD", target=snap.current_branch, kind="points_to"))

    for branch in sorted(snap.branch_heads):
        nodes.append(GraphNode(id=branch, kind="branch", label=branch))
        commit_id = snap.branch_heads[branch]
        if commit_id:
            edges.append(GraphEdge(source=branch, target=commit_id, kind="points_to"))

    seen = set()
    for c in snap.commit_nodes:
        if c.id in seen:
            continue
        seen.add(c.id)
        nodes.append(GraphNode(id=c.id, kind="commit", label=c.id[:7]))
        if c.parent_id:
            edges.append(GraphEdge(source=c.id, target=c.parent_id, kind="parent"))

    return nodes, edges
