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
ROSTER_TOOL = ROOT / "tools" / "roster.py"

sys.path.insert(0, str(ROOT / "tools"))
import catalog  # noqa: E402
import roster  # noqa: E402


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def refresh_catalog(root: Path) -> None:
    write(root / "SKILLS.md", catalog.render_catalog(root))


def write_skill(root: Path, name: str, front_matter: str, body: str = "# Example\n") -> None:
    write(root / f"skills/{name}/SKILL.md", f"---\n{front_matter}---\n{body}")
    refresh_catalog(root)


def role_front_matter(
    name: str = "reviewer", tier: str = "flow", skills: str = "[]"
) -> str:
    return (
        f"role: {name}\n"
        f"tier: {tier}\n"
        "mission: Verify finished work.\n"
        "reads: [AGENTS.md]\n"
        f"skills: {skills}\n"
        "never: [review work you built]\n"
        "done_when: The review has a verdict.\n"
        "escalate_when: The criteria are wrong.\n"
    )


def write_role(root: Path, name: str, front_matter: str, body: str = "# Example\n") -> None:
    write(root / f"roles/{name}/ROLE.md", f"---\n{front_matter}---\n{body}")
    write(root / "roles/ROSTER.md", roster.render_roster(root))


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
        "tools/_lib.py": "# placeholder\n",
        "tools/catalog.py": "# placeholder\n",
        "tools/check.py": "# placeholder\n",
        "tools/install.py": "# placeholder\n",
        "tools/new_skill.py": "# placeholder\n",
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

    def test_broken_root_doc_link_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write(root / "SECURITY.md", "See [missing](missing.md).\n")
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("broken-link", result.stdout)
            self.assertIn("SECURITY.md", result.stdout)

    def test_broken_nested_readme_link_fails(self) -> None:
        for name in ("skills/README.md", "agents/README.md"):
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory() as tmp:
                    root = make_repo(Path(tmp))
                    write(root / name, "See [missing](missing.md).\n")
                    result = run_check(root)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn("broken-link", result.stdout)
                    self.assertIn(name, result.stdout)

    def test_core_fields_must_be_strings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write_skill(
                root,
                "example-skill",
                (
                    "name: example-skill\n"
                    "description: [a, b]\n"
                    "license: true\n"
                    "metadata:\n"
                    "  category: engineering\n"
                ),
            )
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("'description' must be a string", result.stdout)
            self.assertIn("'license' must be a string", result.stdout)

    def test_allowed_tools_must_be_space_separated(self) -> None:
        cases = [
            ("Read,Grep", "not comma-separated"),
            ("[Read, Grep]", "space-separated string"),
        ]
        for value, expected in cases:
            with self.subTest(value=value):
                with tempfile.TemporaryDirectory() as tmp:
                    root = make_repo(Path(tmp))
                    write_skill(
                        root,
                        "example-skill",
                        (
                            "name: example-skill\n"
                            "description: Does a thing. Use when testing.\n"
                            "license: MIT\n"
                            f"allowed-tools: {value}\n"
                            "metadata:\n"
                            "  category: engineering\n"
                        ),
                    )
                    result = run_check(root)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn(expected, result.stdout)

    def test_metadata_values_must_be_strings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write_skill(
                root,
                "example-skill",
                (
                    "name: example-skill\n"
                    "description: Does a thing. Use when testing.\n"
                    "license: MIT\n"
                    "metadata:\n"
                    "  category: engineering\n"
                    "  version: true\n"
                ),
            )
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("metadata.version must be a string", result.stdout)

    def test_todo_placeholder_fails_strict(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write_skill(
                root,
                "example-skill",
                (
                    "name: example-skill\n"
                    "description: TODO: finish this skill.\n"
                    "license: MIT\n"
                    "metadata:\n"
                    "  category: engineering\n"
                ),
            )
            result = run_check(root, "--strict")
            self.assertEqual(result.returncode, 1)
            self.assertIn("skill-placeholder", result.stdout)

    def test_broken_reference_link_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write_skill(
                root,
                "example-skill",
                (
                    "name: example-skill\n"
                    "description: Does a thing. Use when testing.\n"
                    "license: MIT\n"
                    "metadata:\n"
                    "  category: engineering\n"
                ),
            )
            write(root / "skills/example-skill/references/notes.md", "[missing](missing.md)\n")
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("link target not found", result.stdout)

    def test_reference_link_cannot_leave_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write_skill(
                root,
                "example-skill",
                (
                    "name: example-skill\n"
                    "description: Does a thing. Use when testing.\n"
                    "license: MIT\n"
                    "metadata:\n"
                    "  category: engineering\n"
                ),
            )
            write(root / "skills/example-skill/references/notes.md", "[outside](../../README.md)\n")
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("link leaves the skill folder", result.stdout)

    def test_inline_code_and_comments_are_not_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write_skill(
                root,
                "example-skill",
                (
                    "name: example-skill\n"
                    "description: Does a thing. Use when testing.\n"
                    "license: MIT\n"
                    "metadata:\n"
                    "  category: engineering\n"
                ),
                body="`[missing](missing.md)`\n\n<!-- [missing](missing.md) -->\n",
            )
            result = run_check(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_catalog_escapes_a_trailing_backslash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write_skill(
                root,
                "example-skill",
                (
                    "name: example-skill\n"
                    r'description: "ends with a backslash \\"' + "\n"
                    "license: MIT\n"
                    "metadata:\n"
                    "  category: engineering\n"
                ),
            )
            catalog_text = (root / "SKILLS.md").read_text(encoding="utf-8")
            self.assertIn(r"ends with a backslash \\ |", catalog_text)
            result = run_check(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_block_scalar_reports_clear_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write(
                root / "skills/example-skill/SKILL.md",
                (
                    "---\n"
                    "name: example-skill\n"
                    "description: >\n"
                    "  folded text\n"
                    "license: MIT\n"
                    "metadata:\n"
                    "  category: engineering\n"
                    "---\n"
                ),
            )
            refresh_catalog(root)
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("block scalars", result.stdout)
            self.assertNotIn("Traceback", result.stderr)

    def test_bom_front_matter_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write(
                root / "skills/example-skill/SKILL.md",
                (
                    "\ufeff---\n"
                    "name: example-skill\n"
                    "description: Does a thing. Use when testing.\n"
                    "license: MIT\n"
                    "metadata:\n"
                    "  category: engineering\n"
                    "---\n"
                    "# Example\n"
                ),
            )
            refresh_catalog(root)
            result = run_check(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unreadable_agents_reports_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            (root / "AGENTS.md").write_bytes(b"\xff")
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("read", result.stdout)
            self.assertNotIn("Traceback", result.stderr)

    def test_unreadable_adr_reports_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            (root / "docs/decisions/0002-bad.md").write_bytes(b"\xff")
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("read", result.stdout)
            self.assertNotIn("Traceback", result.stderr)

    def test_catalog_read_errors_are_reported_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            (root / "SKILLS.md").write_bytes(b"\xff")
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("catalog-read", result.stdout)
            self.assertNotIn("Traceback", result.stderr)
            catalog_result = run_tool(CATALOG, root, "--check")
            self.assertEqual(catalog_result.returncode, 1)
            self.assertIn("cannot read", catalog_result.stderr)


class RoleTests(unittest.TestCase):
    def test_valid_role_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write_role(root, "reviewer", role_front_matter())
            result = run_check(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("1 role(s)", result.stdout)

    def test_role_name_must_match_folder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write_role(root, "reviewer", role_front_matter(name="builder"))
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("must match the folder", result.stdout)

    def test_role_tier_must_be_known(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write_role(root, "reviewer", role_front_matter(tier="boss"))
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("tier must be one of", result.stdout)

    def test_role_skill_must_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write_role(root, "reviewer", role_front_matter(skills="[missing-skill]"))
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("does not exist", result.stdout)

    def test_role_reads_must_be_a_list(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            front_matter = role_front_matter().replace("reads: [AGENTS.md]", "reads: AGENTS.md")
            write_role(root, "reviewer", front_matter)
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("reads must be a non-empty list", result.stdout)

    def test_unknown_role_field_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            front_matter = role_front_matter() + "item_files: [brief.md]\n"
            write_role(root, "reviewer", front_matter)
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("unsupported front matter field", result.stdout)

    def test_role_access_read_only_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write_role(root, "reviewer", role_front_matter() + "access: read-only\n")
            result = run_check(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_role_access_must_be_known(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write_role(root, "reviewer", role_front_matter() + "access: write\n")
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("access must be one of", result.stdout)

    def test_role_use_when_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write_role(
                root,
                "reviewer",
                role_front_matter() + "use_when: a caller needs a fact checked\n",
            )
            result = run_check(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_role_use_when_must_be_non_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write_role(root, "reviewer", role_front_matter() + "use_when:\n")
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("use_when must be a non-empty string", result.stdout)

    def test_missing_role_roster_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write(
                root / "roles/reviewer/ROLE.md",
                f"---\n{role_front_matter()}---\n# Example\n",
            )
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("generated roster is missing", result.stdout)

    def test_stale_role_roster_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write_role(root, "reviewer", role_front_matter())
            write(root / "roles/ROSTER.md", "# Old roster\n")
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("generated roster is out of date", result.stdout)

    def test_unreadable_role_reports_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write_role(root, "reviewer", role_front_matter())
            (root / "roles/reviewer/ROLE.md").write_bytes(b"\xff")
            result = run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("role-read", result.stdout)
            self.assertNotIn("Traceback", result.stderr)

    def test_roster_tool_writes_and_checks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write(
                root / "roles/reviewer/ROLE.md",
                f"---\n{role_front_matter()}---\n# Example\n",
            )
            written = run_tool(ROSTER_TOOL, root)
            self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
            self.assertTrue((root / "roles/ROSTER.md").exists())
            checked = run_tool(ROSTER_TOOL, root, "--check")
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            check = run_check(root)
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)


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
            self.assertIn('Say "hi" and C:\\\\tmp', catalog_text)
            check = run_check(root)
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_new_skill_force_repairs_broken_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            write(root / "skills/example-skill/SKILL.md", "---\nname: example-skill\n")
            result = run_tool(
                NEW_SKILL,
                root,
                "example-skill",
                "--category",
                "engineering",
                "--description",
                "Use when testing the repair path.",
                "--force",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            check = run_check(root)
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_new_skill_rejects_empty_and_long_descriptions(self) -> None:
        cases = [
            ("", "must not be empty"),
            ("x" * 1025, "1024"),
        ]
        for description, expected in cases:
            with self.subTest(length=len(description)):
                with tempfile.TemporaryDirectory() as tmp:
                    root = make_repo(Path(tmp))
                    result = run_tool(
                        NEW_SKILL,
                        root,
                        "example-skill",
                        "--category",
                        "engineering",
                        "--description",
                        description,
                    )
                    self.assertEqual(result.returncode, 2)
                    self.assertIn(expected, result.stderr)
                    self.assertFalse((root / "skills/example-skill").exists())

    def test_new_skill_rejects_invalid_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            result = run_tool(
                NEW_SKILL,
                root,
                "Bad_Name",
                "--category",
                "engineering",
                "--description",
                "Use when testing the name rule.",
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("name must be", result.stderr)

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

    def test_install_force_replaces_a_file_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            project = Path(tmp) / "project"
            project.mkdir()
            created = run_tool(NEW_SKILL, root, "example-skill", "--category", "engineering")
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            dest = project / ".claude/skills/example-skill"
            dest.parent.mkdir(parents=True)
            dest.write_text("old\n", encoding="utf-8")
            result = run_tool(
                INSTALL,
                root,
                "--target",
                "claude",
                "--skill",
                "example-skill",
                "--project",
                str(project),
                "--force",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(dest.is_dir())
            self.assertTrue((dest / "SKILL.md").exists())

    def test_install_force_replaces_a_symlink_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            project = Path(tmp) / "project"
            project.mkdir()
            created = run_tool(NEW_SKILL, root, "example-skill", "--category", "engineering")
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            target = Path(tmp) / "target"
            target.mkdir()
            (target / "keep.txt").write_text("keep\n", encoding="utf-8")
            dest = project / ".claude/skills/example-skill"
            dest.parent.mkdir(parents=True)
            try:
                dest.symlink_to(target, target_is_directory=True)
            except OSError:
                self.skipTest("symlinks are not available")
            result = run_tool(
                INSTALL,
                root,
                "--target",
                "claude",
                "--skill",
                "example-skill",
                "--project",
                str(project),
                "--force",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse(dest.is_symlink())
            self.assertTrue((dest / "SKILL.md").exists())
            self.assertTrue((target / "keep.txt").exists())

    def test_install_copy_failure_preserves_existing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            project = Path(tmp) / "project"
            project.mkdir()
            created = run_tool(NEW_SKILL, root, "example-skill", "--category", "engineering")
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            source = root / "skills/example-skill"
            try:
                (source / "broken-link").symlink_to("/nonexistent/target")
            except OSError:
                self.skipTest("symlinks are not available")
            dest = project / ".claude/skills/example-skill"
            dest.mkdir(parents=True)
            (dest / "SKILL.md").write_text("old\n", encoding="utf-8")
            result = run_tool(
                INSTALL,
                root,
                "--target",
                "claude",
                "--skill",
                "example-skill",
                "--project",
                str(project),
                "--force",
            )
            self.assertEqual(result.returncode, 1)
            self.assertEqual((dest / "SKILL.md").read_text(encoding="utf-8"), "old\n")
            self.assertEqual(list(dest.parent.glob(".example-skill.*")), [])

    def test_install_all_continues_after_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            project = Path(tmp) / "project"
            project.mkdir()
            for name in ("a-broken", "b-good"):
                created = run_tool(
                    NEW_SKILL,
                    root,
                    name,
                    "--category",
                    "engineering",
                    "--description",
                    "Use when testing install all.",
                )
                self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            try:
                (root / "skills/a-broken/broken-link").symlink_to("/nonexistent/target")
            except OSError:
                self.skipTest("symlinks are not available")
            result = run_tool(
                INSTALL,
                root,
                "--target",
                "claude",
                "--all",
                "--project",
                str(project),
                "--force",
            )
            self.assertEqual(result.returncode, 1)
            self.assertTrue((project / ".claude/skills/b-good/SKILL.md").exists())
            self.assertFalse((project / ".claude/skills/a-broken").exists())
            self.assertEqual(list((project / ".claude/skills").glob(".*")), [])


if __name__ == "__main__":
    unittest.main()
