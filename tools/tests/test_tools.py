#!/usr/bin/env python3
"""Tests for tools/check.py. Standard library only."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECK = ROOT / "tools" / "check.py"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_repo(tmp: Path) -> Path:
    root = tmp / "repo"
    required = {
        "README.md": "# Test\n",
        "AGENTS.md": "# Test\n",
        "LICENSE": "MIT\n",
        "THIRD_PARTY_NOTICES.md": "# Notices\n",
        "CHANGELOG.md": "# Changelog\n",
        "docs/INDEX.md": "# Docs\n",
        "docs/decisions/README.md": "# Decisions\n",
        "docs/decisions/0001-test.md": (
            "---\n"
            "title: Test decision\n"
            "status: accepted\n"
            "date: 2026-11-10\n"
            "summary: A test decision.\n"
            "---\n"
            "# 0001: Test decision\n"
        ),
        "skills/README.md": "# Skills\n",
        "roles/README.md": "# Roles\n",
        "agents/README.md": "# Agents\n",
        "agents/protocols/README.md": "# Protocols\n",
        "agents/adapters/README.md": "# Adapters\n",
        "agents/evals/README.md": "# Evals\n",
        ".github/CODEOWNERS": "* @owner\n",
        ".github/pull_request_template.md": "## Summary\n",
        ".github/workflows/check.yml": "name: check\n",
        "tools/tests/test_tools.py": "# placeholder\n",
    }
    for path, text in required.items():
        write(root / path, text)
    return root


def run_check(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECK), "--root", str(root), *args],
        text=True,
        capture_output=True,
    )


class CheckTests(unittest.TestCase):
    def test_current_repo_passes(self) -> None:
        result = subprocess.run([sys.executable, str(CHECK)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ok:", result.stdout)

    def test_valid_skill_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write(
                root / "skills/example-skill/SKILL.md",
                (
                    "---\n"
                    "name: example-skill\n"
                    "description: Does a thing. Use when testing the checker.\n"
                    "license: MIT\n"
                    "metadata:\n"
                    "  category: engineering\n"
                    "  invocation: both\n"
                    "---\n"
                    "# Example\n"
                ),
            )
            result = run_check(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("1 skill(s)", result.stdout)

    def test_name_must_match_folder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write(
                root / "skills/example-skill/SKILL.md",
                (
                    "---\n"
                    "name: other-name\n"
                    "description: Does a thing. Use when testing.\n"
                    "license: MIT\n"
                    "metadata:\n"
                    "  category: engineering\n"
                    "---\n"
                ),
            )
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("must match the folder", result.stdout)

    def test_missing_license_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write(
                root / "skills/example-skill/SKILL.md",
                (
                    "---\n"
                    "name: example-skill\n"
                    "description: Does a thing. Use when testing.\n"
                    "metadata:\n"
                    "  category: engineering\n"
                    "---\n"
                ),
            )
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("missing 'license'", result.stdout)

    def test_skill_size_is_a_warning_until_strict(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            body = "\n".join(["line"] * 501)
            write(
                root / "skills/example-skill/SKILL.md",
                (
                    "---\n"
                    "name: example-skill\n"
                    "description: Does a thing. Use when testing.\n"
                    "license: MIT\n"
                    "metadata:\n"
                    "  category: engineering\n"
                    "---\n"
                    f"{body}\n"
                ),
            )
            result = run_check(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            strict = run_check(root, "--strict")
            self.assertEqual(strict.returncode, 1)
            self.assertIn("skill-size", strict.stdout)

    def test_broken_skill_link_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write(
                root / "skills/example-skill/SKILL.md",
                (
                    "---\n"
                    "name: example-skill\n"
                    "description: Does a thing. Use when testing.\n"
                    "license: MIT\n"
                    "metadata:\n"
                    "  category: engineering\n"
                    "---\n"
                    "See [missing](references/missing.md).\n"
                ),
            )
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("link target not found", result.stdout)


if __name__ == "__main__":
    unittest.main()
