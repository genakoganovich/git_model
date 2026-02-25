from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class GitEvent:
    type: str              # "init" | "add" | "commit" | "branch" | "checkout" | "log" | "show"
    source: Optional[str]  # "working_dir" | "index" | "repository" | None
    target: Optional[str]  # "index" | "repository" | None
    filename: Optional[str] = None

    @classmethod
    def init(cls):
        return cls(type="init", source=None, target="repository")

    @classmethod
    def add(cls, filename: str):
        return cls(type="add", source="working_dir", target="index", filename=filename)

    @classmethod
    def commit(cls):
        return cls(type="commit", source="index", target="repository")

    @classmethod
    def branch(cls, name: str):
        return cls(type="branch", source="repository", target="repository", filename=name)

    @classmethod
    def checkout(cls, name: str):
        return cls(type="checkout", source="repository", target="repository", filename=name)

    @classmethod
    def log(cls):
        return cls(type="log", source="repository", target="repository")

    @classmethod
    def show(cls, ref: str):
        return cls(type="show", source="repository", target="repository", filename=ref)
