from git_sim.domain.status import StatusResult


class AsciiRenderer:
    @staticmethod
    def render_state(wd: dict, index: dict, head: dict | None, status: StatusResult) -> str:
        head = head or {}

        lines = []

        # Working Directory
        lines.append("+---------------------+")
        lines.append("| Working Directory   |")
        lines.append("+---------------------+")
        for name in sorted(wd):
            lines.append(f"| {name}: {wd[name]}")
        lines.append("")

        # Index
        lines.append("+---------------------+")
        lines.append("| Index               |")
        lines.append("+---------------------+")
        for name in sorted(index):
            lines.append(f"| {name}: {index[name]}")
        lines.append("")

        # HEAD
        lines.append("+---------------------+")
        lines.append("| Repository (HEAD)   |")
        lines.append("+---------------------+")
        for name in sorted(head):
            lines.append(f"| {name}: {head[name]}")
        lines.append("")

        # Status
        lines.append("+---------------------+")
        lines.append("| Status              |")
        lines.append("+---------------------+")
        lines.append(f"| Untracked: {sorted(status.untracked)}")
        lines.append(f"| Staged: {sorted(status.staged)}")
        lines.append(f"| Modified: {sorted(status.modified)}")

        return "\n".join(lines)