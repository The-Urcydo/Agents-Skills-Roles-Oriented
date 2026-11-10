#!/usr/bin/env python3
"""Scaffold a new skill folder and regenerate SKILLS.md.

Usage:
  python3 tools/new_skill.py my-skill --category engineering
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
import catalog
from _lib import CATEGORIES, INVOCATIONS, is_valid_skill_name, repo_root

TEMPLATE = """---
name: {name}
description: "{description}"
license: MIT
metadata:
  category: {category}
  invocation: {invocation}
---
# {title}

TODO: state what this skill does and when it applies.

## Steps

1. TODO: write the first step.

## Verify

TODO: state the command, check, or observable result that proves the skill worked.

## Stop and ask

TODO: list the conditions that mean the agent must stop.
"""


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("name", help="skill name and folder name")
    ap.add_argument("--category", required=True, choices=CATEGORIES)
    ap.add_argument(
        "--description",
        default="TODO: what this skill does and when to use it.",
        help="one sentence: what it does and when to use it",
    )
    ap.add_argument("--invocation", default="both", choices=INVOCATIONS)
    ap.add_argument("--force", action="store_true", help="overwrite an existing SKILL.md")
    ap.add_argument("--root", type=Path, default=None, help="repository root")
    args = ap.parse_args(argv)

    root = (args.root or repo_root()).resolve()
    if not is_valid_skill_name(args.name):
        print(
            "error: name must be 1-64 chars: lowercase letters, digits, single hyphens",
            file=sys.stderr,
        )
        return 2

    folder = root / "skills" / args.name
    if folder.exists() and not args.force:
        print(
            f"error: {folder.relative_to(root)} already exists (use --force to overwrite)",
            file=sys.stderr,
        )
        return 2

    bad = catalog.unreadable_skills(root)
    if bad:
        print("error: fix unreadable skills before scaffolding:", file=sys.stderr)
        for path in bad:
            print(f"  {path}", file=sys.stderr)
        return 2

    folder.mkdir(parents=True, exist_ok=True)
    description = " ".join(args.description.split())
    description = description.replace("\\", "\\\\").replace('"', '\\"')
    content = TEMPLATE.format(
        name=args.name,
        description=description,
        category=args.category,
        invocation=args.invocation,
        title=args.name.replace("-", " ").title(),
    )
    (folder / "SKILL.md").write_text(content, encoding="utf-8")
    changed = catalog.write_catalog(root)
    print(f"created {folder.relative_to(root)}/SKILL.md")
    print("updated SKILLS.md" if changed else "SKILLS.md already up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
