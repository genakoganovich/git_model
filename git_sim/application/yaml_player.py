from __future__ import annotations

from pathlib import Path
from typing import Any

from git_sim.application.git_service import GitService


class YamlCommandPlayer:
    """Runs a sequence of git-sim commands described in YAML."""

    def __init__(self, git_service: GitService | None = None):
        self.git = git_service or GitService()

    def play_file(self, path: str | Path) -> GitService:
        with open(path, "r", encoding="utf-8") as f:
            payload = _parse_minimal_yaml(f.read())
        return self.play(payload)

    def play(self, payload: Any) -> GitService:
        if not isinstance(payload, dict):
            raise ValueError("YAML root must be a mapping")

        commands = payload.get("commands")
        if not isinstance(commands, list):
            raise ValueError("YAML must contain 'commands' list")

        for item in commands:
            self.run_command(item)

        return self.git

    def run_command(self, item: dict[str, Any]) -> None:
        if not isinstance(item, dict):
            raise ValueError("Each command must be a mapping")

        cmd = item.get("cmd")
        if not isinstance(cmd, str):
            raise ValueError("Each command must include string field 'cmd'")

        if cmd == "init":
            self.git.init()
            return

        if cmd == "write":
            filename = _require_str(item, "filename")
            content = _require_str(item, "content")
            self.git.working_dir.write(filename, content)
            return

        if cmd == "add":
            filename = _require_str(item, "filename")
            self.git.add(filename)
            return

        if cmd == "commit":
            self.git.commit()
            return

        if cmd == "branch":
            name = _require_str(item, "name")
            self.git.branch(name)
            return

        if cmd == "checkout":
            name = _require_str(item, "name")
            self.git.checkout(name)
            return

        raise ValueError(f"Unknown command: {cmd}")


def _parse_minimal_yaml(text: str) -> dict[str, list[dict[str, str]]]:
    """Parse the tiny YAML subset used for scenario scripts.

    Supported shape:
      commands:
        - cmd: init
        - cmd: write
          filename: a.txt
          content: "value"
    """

    lines = [line.rstrip() for line in text.splitlines()]
    commands: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_commands = False

    for raw in lines:
        line = raw.strip()

        if not line or line.startswith("#"):
            continue

        if line == "commands:":
            in_commands = True
            continue

        if not in_commands:
            raise ValueError("YAML must start with 'commands:' section")

        if line.startswith("- "):
            if current is not None:
                commands.append(current)

            key, value = _split_kv(line[2:])
            current = {key: _parse_scalar(value)}
            continue

        if current is None:
            raise ValueError("Invalid YAML command item")

        key, value = _split_kv(line)
        current[key] = _parse_scalar(value)

    if current is not None:
        commands.append(current)

    return {"commands": commands}


def _split_kv(fragment: str) -> tuple[str, str]:
    if ":" not in fragment:
        raise ValueError(f"Invalid mapping line: {fragment}")

    key, value = fragment.split(":", 1)
    return key.strip(), value.strip()


def _parse_scalar(value: str) -> str:
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]

    return value


def _require_str(item: dict[str, Any], key: str) -> str:
    value = item.get(key)
    if not isinstance(value, str):
        raise ValueError(f"Command '{item.get('cmd')}' requires string field '{key}'")
    return value
