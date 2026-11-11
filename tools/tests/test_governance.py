#!/usr/bin/env python3
"""Checks for the governance files that GitHub does not validate for us. Standard library only."""
from __future__ import annotations

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
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/private_channel.yml",
    ".github/ISSUE_TEMPLATE/question.yml",
    ".github/ISSUE_TEMPLATE/skill_proposal.yml",
    "docs/decisions/0006-repository-governance.md",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


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

    def test_codeowners_is_a_single_catch_all(self) -> None:
        entries = parse_codeowners()
        self.assertEqual(
            [pattern for pattern, _ in entries],
            ["*"],
            "CODEOWNERS should be only the * catch-all; narrower lines are redundant",
        )
        self.assertTrue(entries[0][1], "the * catch-all line needs at least one owner")

    def test_agents_names_every_codeowner(self) -> None:
        agents = read(AGENTS).lower()
        owners = set().union(*(owners for _, owners in parse_codeowners()))
        missing = sorted(owner for owner in owners if owner not in agents)
        self.assertEqual(missing, [], f"AGENTS.md does not name the owners: {missing}")

    def test_dependabot_tracks_github_actions_weekly(self) -> None:
        text = read(DEPENDABOT)
        self.assertIn("package-ecosystem: github-actions", text)
        self.assertIn("interval: weekly", text)


if __name__ == "__main__":
    unittest.main()
