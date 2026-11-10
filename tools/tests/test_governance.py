#!/usr/bin/env python3
"""Checks for the governance files that GitHub does not validate for us. Standard library only."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CODEOWNERS = ROOT / ".github" / "CODEOWNERS"
AGENTS = ROOT / "AGENTS.md"
DEPENDABOT = ROOT / ".github" / "dependabot.yml"
GOVERNANCE_FILES = (
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    ".github/dependabot.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    "docs/decisions/0006-repository-governance.md",
)
LINKED_DOCS = ("SECURITY.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "README.md")
LINK_RE = re.compile(r"(?<!\\)\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"```.*?```", re.S)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_fences(text: str) -> str:
    return FENCE_RE.sub("", text)


def parse_codeowners() -> list[tuple[str, set[str]]]:
    entries = []
    for raw in read(CODEOWNERS).splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        pattern, *owners = line.split()
        if not owners:
            raise AssertionError(f"CODEOWNERS line {pattern!r} has no owners")
        entries.append((pattern, {owner.lstrip("@").lower() for owner in owners}))
    return entries


class GovernanceTests(unittest.TestCase):
    def test_required_governance_files_exist(self) -> None:
        missing = [path for path in GOVERNANCE_FILES if not (ROOT / path).exists()]
        self.assertEqual(missing, [], f"missing governance files: {missing}")

    def test_codeowners_has_one_catch_all_with_owners(self) -> None:
        entries = parse_codeowners()
        catch_all = [owners for pattern, owners in entries if pattern == "*"]
        self.assertEqual(len(catch_all), 1, "CODEOWNERS needs exactly one * catch-all line")
        self.assertTrue(catch_all[0], "the * catch-all line needs at least one owner")

    def test_every_codeowners_line_uses_the_catch_all_owners(self) -> None:
        entries = parse_codeowners()
        catch_all = next(owners for pattern, owners in entries if pattern == "*")
        problems = [
            f"{pattern!r} has {sorted(owners)}, expected {sorted(catch_all)}"
            for pattern, owners in entries
            if pattern != "*" and owners != catch_all
        ]
        self.assertEqual(problems, [], "\n".join(problems))

    def test_agents_names_every_codeowner(self) -> None:
        agents = read(AGENTS).lower()
        owners = set().union(*(owners for _, owners in parse_codeowners()))
        missing = sorted(owner for owner in owners if owner not in agents)
        self.assertEqual(missing, [], f"AGENTS.md does not name the owners: {missing}")

    def test_dependabot_tracks_github_actions_weekly(self) -> None:
        text = read(DEPENDABOT)
        self.assertIn("package-ecosystem: github-actions", text)
        self.assertIn("interval: weekly", text)

    def test_relative_links_in_root_governance_docs_resolve(self) -> None:
        problems = []
        for name in LINKED_DOCS:
            path = ROOT / name
            for target in LINK_RE.findall(strip_fences(read(path))):
                target = target.strip()
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target = target.split("#", 1)[0]
                if not target:
                    continue
                destination = (path.parent / target).resolve()
                try:
                    destination.relative_to(ROOT.resolve())
                except ValueError:
                    problems.append(f"{name}: link leaves the repository: {target}")
                    continue
                if not destination.exists():
                    problems.append(f"{name}: link target not found: {target}")
        self.assertEqual(problems, [], "\n".join(problems))


if __name__ == "__main__":
    unittest.main()
