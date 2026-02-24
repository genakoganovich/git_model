from __future__ import annotations

from git_sim.application.scenario_stepper import CommitNode


class DagRenderer:
    @staticmethod
    def render(
        current_branch: str,
        branch_heads: dict[str, str | None],
        commit_nodes: tuple[CommitNode, ...],
    ) -> str:
        lines: list[str] = [f"HEAD -> {current_branch}", ""]

        for branch in sorted(branch_heads):
            marker = "*" if branch == current_branch else " "
            commit_id = branch_heads[branch]
            short_id = commit_id[:7] if commit_id else "None"
            lines.append(f"{marker} {branch}: {short_id}")

        lines.append("")
        lines.append("Commits:")

        if not commit_nodes:
            lines.append("(empty)")
            return "\n".join(lines)

        for node in commit_nodes:
            parent = node.parent_id[:7] if node.parent_id else "None"
            file_names = ", ".join(sorted(node.files)) if node.files else "-"
            lines.append(f"{node.id[:7]} <- {parent} [{file_names}]")

        return "\n".join(lines)
