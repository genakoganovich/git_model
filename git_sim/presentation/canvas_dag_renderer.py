from __future__ import annotations
import tkinter as tk
from git_sim.presentation.graph_view import GraphNode, GraphEdge


class CanvasDagRenderer:
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas

    def draw(
        self,
        nodes: list[GraphNode],
        edges: list[GraphEdge],
        coords: dict[str, tuple[float, float]],
    ) -> None:
        self.canvas.delete("all")
        sx, sy = 100, 80
        ox, oy = 60, 180

        def pt(node_id: str) -> tuple[float, float]:
            x, y = coords[node_id]
            return ox + x * sx, oy + y * sy

        for e in edges:
            if e.source in coords and e.target in coords:
                x1, y1 = pt(e.source)
                x2, y2 = pt(e.target)
                color = "gray40" if e.kind == "parent" else "forest green"
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

        for n in nodes:
            x, y = pt(n.id)
            r = 10 if n.kind == "commit" else (12 if n.kind == "branch" else 14)
            color = "skyblue" if n.kind == "commit" else ("orange" if n.kind == "branch" else "red")
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="")
            self.canvas.create_text(x, y - (r + 10), text=n.label, fill="black")
