#!/usr/bin/env python3
"""Security checks for the GitHub Actions workflows. Standard library only."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_DIR = ROOT / ".github" / "workflows"
USES_RE = re.compile(r"^\s*(?:-\s*)?uses:\s*(\S+)")
SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")


def workflow_files() -> list[Path]:
    return sorted(WORKFLOW_DIR.glob("*.yml")) + sorted(WORKFLOW_DIR.glob("*.yaml"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


class WorkflowSecurityTests(unittest.TestCase):
    def test_workflows_exist(self) -> None:
        self.assertTrue(workflow_files(), "no workflow files found under .github/workflows/")

    def test_actions_are_pinned_to_a_full_commit_sha(self) -> None:
        problems = []
        for path in workflow_files():
            for lineno, line in enumerate(read(path).splitlines(), 1):
                if line.lstrip().startswith("#"):
                    continue
                match = USES_RE.match(line)
                if not match:
                    continue
                value = unquote(match.group(1))
                if value.startswith("./") or value.startswith("docker://"):
                    continue
                if "@" not in value:
                    problems.append(f"{path.name}:{lineno}: {value!r} has no @ref")
                    continue
                action, ref = value.rsplit("@", 1)
                if not action or not SHA_RE.fullmatch(ref):
                    problems.append(
                        f"{path.name}:{lineno}: {value!r} is not pinned to a 40-character commit SHA"
                    )
        self.assertEqual(problems, [], "\n".join(problems))

    def test_each_workflow_declares_top_level_permissions(self) -> None:
        problems = []
        for path in workflow_files():
            lines = read(path).splitlines()
            if not any(line.startswith("permissions:") for line in lines):
                problems.append(f"{path.name}: add a top-level permissions: block")
        self.assertEqual(problems, [], "\n".join(problems))


if __name__ == "__main__":
    unittest.main()
