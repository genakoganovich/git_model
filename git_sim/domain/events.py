from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class GitEvent:
    type: str              # "init" | "add" | "commit"
    source: Optional[str]  # "working_dir" | "index" | None
    target: Optional[str]  # "index" | "repository" | None
    filename: Optional[str] = None