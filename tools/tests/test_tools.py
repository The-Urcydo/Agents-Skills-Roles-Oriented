#!/usr/bin/env python3
"""Tests for the repository tools. Standard library only."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECK = ROOT / "tools" / "check.py"
NEW_SKILL = ROOT / "tools" / "new_skill.py"
CATALOG = ROOT / "tools" / "catalog.py"
INSTALL = ROOT / "tools" / "install.py"

sys.path.insert(0, str(ROOT / "tools"))
import catalog  # noqa: E402


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def refresh_catalog(root: Path) -> None:
    write(root / "SKILLS.md", catalog.render_catalog(root))


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
    refresh_catalog(root)
    return root


def run_check(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECK), "--root", str(root), *args],
        text=True,
        capture_output=True,
    )


def run_tool(tool: Path, root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(tool), "--root", str(root), *args],
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
            refresh_catalog(root)
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
            refresh_catalog(root)
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
            refresh_catalog(root)
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("missing 'license'", result.stdout)

    def test_unknown_skill_field_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write(
                root / "skills/example-skill/SKILL.md",
                (
                    "---\n"
                    "name: example-skill\n"
                    "description: Does a thing. Use when testing.\n"
                    "license: MIT\n"
                    "disable-model-invocation: true\n"
                    "metadata:\n"
                    "  category: engineering\n"
                    "---\n"
                ),
            )
            refresh_catalog(root)
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("unsupported front matter field", result.stdout)

    def test_compatibility_too_long_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write(
                root / "skills/example-skill/SKILL.md",
                (
                    "---\n"
                    "name: example-skill\n"
                    "description: Does a thing. Use when testing.\n"
                    "license: MIT\n"
                    f"compatibility: {'x' * 501}\n"
                    "metadata:\n"
                    "  category: engineering\n"
                    "---\n"
                ),
            )
            refresh_catalog(root)
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("compatibility must be 1-500 chars", result.stdout)

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
            refresh_catalog(root)
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
            refresh_catalog(root)
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("link target not found", result.stdout)


class ToolTests(unittest.TestCase):
    def test_new_skill_scaffolds_and_updates_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            result = run_tool(NEW_SKILL, root, "example-skill", "--category", "engineering")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            skill = root / "skills/example-skill/SKILL.md"
            self.assertTrue(skill.exists())
            self.assertIn("name: example-skill", skill.read_text(encoding="utf-8"))
            self.assertIn("example-skill", (root / "SKILLS.md").read_text(encoding="utf-8"))
            check = run_check(root)
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_new_skill_rejects_duplicate_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            first = run_tool(NEW_SKILL, root, "example-skill", "--category", "engineering")
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            second = run_tool(NEW_SKILL, root, "example-skill", "--category", "engineering")
            self.assertEqual(second.returncode, 2)
            self.assertIn("already exists", second.stderr)

    def test_new_skill_force_reports_unchanged_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            first = run_tool(NEW_SKILL, root, "example-skill", "--category", "engineering")
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            forced = run_tool(
                NEW_SKILL,
                root,
                "example-skill",
                "--category",
                "engineering",
                "--force",
            )
            self.assertEqual(forced.returncode, 0, forced.stdout + forced.stderr)
            self.assertIn("already up to date", forced.stdout)

    def test_new_skill_quotes_a_description_with_a_colon(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            result = run_tool(
                NEW_SKILL,
                root,
                "example-skill",
                "--category",
                "engineering",
                "--description",
                "Use when: testing a colon",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            text = (root / "skills/example-skill/SKILL.md").read_text(encoding="utf-8")
            self.assertIn('description: "Use when: testing a colon"', text)
            check = run_check(root)
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_description_quotes_and_backslashes_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            result = run_tool(
                NEW_SKILL,
                root,
                "example-skill",
                "--category",
                "engineering",
                "--description",
                'Say "hi" and C:\\tmp',
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            catalog_text = (root / "SKILLS.md").read_text(encoding="utf-8")
            self.assertIn('Say "hi" and C:\\tmp', catalog_text)
            check = run_check(root)
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_catalog_check_fails_when_out_of_date(self) -> None:
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
                ),
            )
            result = run_tool(CATALOG, root, "--check")
            self.assertEqual(result.returncode, 1)
            self.assertIn("out of date", result.stdout)

    def test_catalog_write_mode_creates_the_file(self) -> None:
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
                ),
            )
            result = run_tool(CATALOG, root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("example-skill", (root / "SKILLS.md").read_text(encoding="utf-8"))
            check = run_tool(CATALOG, root, "--check")
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_catalog_escapes_markdown_links_in_descriptions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write(
                root / "skills/example-skill/SKILL.md",
                (
                    "---\n"
                    "name: example-skill\n"
                    'description: "Use [docs](references/missing.md) when testing."\n'
                    "license: MIT\n"
                    "metadata:\n"
                    "  category: engineering\n"
                    "---\n"
                ),
            )
            refresh_catalog(root)
            catalog_text = (root / "SKILLS.md").read_text(encoding="utf-8")
            self.assertIn("\\[docs\\]", catalog_text)
            result = run_check(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_check_fails_when_catalog_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            (root / "SKILLS.md").unlink()
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("catalog", result.stdout)
            self.assertIn("required", result.stdout)

    def test_check_fails_when_catalog_is_out_of_date(self) -> None:
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
                ),
            )
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("catalog", result.stdout)

    def test_catalog_check_fails_on_unreadable_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write(root / "skills/bad-skill/SKILL.md", "---\nname: bad-skill\n")
            result = run_tool(CATALOG, root, "--check")
            self.assertEqual(result.returncode, 1)
            self.assertIn("unreadable", result.stdout)

    def test_catalog_check_fails_on_non_utf8_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            skill = root / "skills/bad-skill/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_bytes(b"\xff")
            result = run_tool(CATALOG, root, "--check")
            self.assertEqual(result.returncode, 1)
            self.assertIn("unreadable", result.stdout)

    def test_install_copies_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            project = Path(tmp) / "project"
            project.mkdir()
            created = run_tool(NEW_SKILL, root, "example-skill", "--category", "engineering")
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            write(root / "skills/example-skill/references/notes.md", "note\n")
            result = run_tool(
                INSTALL,
                root,
                "--target",
                "claude",
                "--skill",
                "example-skill",
                "--project",
                str(project),
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((project / ".claude/skills/example-skill/SKILL.md").exists())
            self.assertTrue((project / ".claude/skills/example-skill/references/notes.md").exists())

    def test_install_targets(self) -> None:
        targets = {
            "claude": ".claude/skills",
            "opencode": ".opencode/skills",
            "agents": ".agents/skills",
        }
        for target, destination in targets.items():
            with self.subTest(target=target):
                with tempfile.TemporaryDirectory() as tmp:
                    root = make_repo(Path(tmp))
                    project = Path(tmp) / "project"
                    project.mkdir()
                    created = run_tool(
                        NEW_SKILL, root, "example-skill", "--category", "engineering"
                    )
                    self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
                    result = run_tool(
                        INSTALL,
                        root,
                        "--target",
                        target,
                        "--skill",
                        "example-skill",
                        "--project",
                        str(project),
                    )
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertTrue(
                        (project / destination / "example-skill/SKILL.md").exists()
                    )

    def test_install_all_and_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            project = Path(tmp) / "project"
            project.mkdir()
            created = run_tool(NEW_SKILL, root, "example-skill", "--category", "engineering")
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)

            first = run_tool(
                INSTALL, root, "--target", "claude", "--all", "--project", str(project)
            )
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            installed = project / ".claude/skills/example-skill/SKILL.md"
            self.assertTrue(installed.exists())

            source = root / "skills/example-skill/SKILL.md"
            source.write_text(source.read_text(encoding="utf-8") + "\nchanged\n", encoding="utf-8")
            skipped = run_tool(
                INSTALL, root, "--target", "claude", "--all", "--project", str(project)
            )
            self.assertEqual(skipped.returncode, 1)
            self.assertNotIn("changed", installed.read_text(encoding="utf-8"))

            forced = run_tool(
                INSTALL,
                root,
                "--target",
                "claude",
                "--all",
                "--project",
                str(project),
                "--force",
            )
            self.assertEqual(forced.returncode, 0, forced.stdout + forced.stderr)
            self.assertIn("changed", installed.read_text(encoding="utf-8"))

    def test_install_dry_run_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            project = Path(tmp) / "project"
            project.mkdir()
            created = run_tool(NEW_SKILL, root, "example-skill", "--category", "engineering")
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            result = run_tool(
                INSTALL,
                root,
                "--target",
                "claude",
                "--skill",
                "example-skill",
                "--project",
                str(project),
                "--dry-run",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("would install", result.stdout)
            self.assertFalse((project / ".claude/skills/example-skill").exists())

    def test_install_dry_run_existing_returns_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            project = Path(tmp) / "project"
            project.mkdir()
            created = run_tool(NEW_SKILL, root, "example-skill", "--category", "engineering")
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            installed = project / ".claude/skills/example-skill/SKILL.md"
            write(installed, "old\n")
            result = run_tool(
                INSTALL,
                root,
                "--target",
                "claude",
                "--skill",
                "example-skill",
                "--project",
                str(project),
                "--dry-run",
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("would skip", result.stdout)
            self.assertEqual(installed.read_text(encoding="utf-8"), "old\n")

    def test_install_rejects_all_plus_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            project = Path(tmp) / "project"
            project.mkdir()
            result = run_tool(
                INSTALL,
                root,
                "--target",
                "claude",
                "--all",
                "--skill",
                "example-skill",
                "--project",
                str(project),
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("either --all or --skill", result.stderr)

    def test_install_all_on_empty_library_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            project = Path(tmp) / "project"
            project.mkdir()
            result = run_tool(
                INSTALL,
                root,
                "--target",
                "claude",
                "--all",
                "--project",
                str(project),
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("no skills to install", result.stderr)

    def test_install_unknown_skill_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            project = Path(tmp) / "project"
            project.mkdir()
            result = run_tool(
                INSTALL,
                root,
                "--target",
                "claude",
                "--skill",
                "missing",
                "--project",
                str(project),
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("unknown skill", result.stderr)


if __name__ == "__main__":
    unittest.main()
