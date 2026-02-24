from __future__ import annotations
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class GraphNode:
    id: str
    kind: Literal["commit", "branch", "head"]
    label: str


@dataclass(frozen=True)
class GraphEdge:
    source: str
    target: str
    kind: Literal["parent", "points_to"]
