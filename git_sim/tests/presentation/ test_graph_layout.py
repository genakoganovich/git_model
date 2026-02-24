from git_sim.presentation.graph_view import GraphNode, GraphEdge
from git_sim.presentation.graph_layout import GraphLayout


def test_layout_head_right_of_branches():
    nodes = [
        GraphNode("HEAD", "head", "HEAD"),
        GraphNode("main", "branch", "main"),
        GraphNode("a1", "commit", "a1"),
    ]
    edges = [
        GraphEdge("HEAD", "main", "points_to"),
        GraphEdge("main", "a1", "points_to"),
    ]
    coords = GraphLayout().compute(nodes, edges)
    assert coords["HEAD"][0] > coords["main"][0]
