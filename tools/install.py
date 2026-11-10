#!/usr/bin/env python3
"""Install skills into an agent's project skills folder.

Targets:
  claude    .claude/skills/<name>/
  opencode  .opencode/skills/<name>/
  agents    .agents/skills/<name>/

The installer copies the whole skill folder, including references, scripts,
assets, and PROVENANCE.md. It does not symlink.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import repo_root

TARGETS = {
    "claude": ".claude/skills",
    "opencode": ".opencode/skills",
    "agents": ".agents/skills",
}


def available_skills(root: Path) -> List[str]:
    base = root / "skills"
    if not base.is_dir():
        return []
    return sorted(
        p.name
        for p in base.iterdir()
        if p.is_dir() and not p.name.startswith(".") and (p / "SKILL.md").exists()
    )


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--target", required=True, choices=sorted(TARGETS))
    ap.add_argument("--skill", action="append", default=[], help="skill name; repeat for several")
    ap.add_argument("--all", action="store_true", help="install every skill")
    ap.add_argument(
        "--project",
        type=Path,
        default=Path("."),
        help="project root (default: current directory)",
    )
    ap.add_argument("--root", type=Path, default=None, help="library root (default: this checkout)")
    ap.add_argument("--force", action="store_true", help="replace an existing skill folder")
    ap.add_argument("--dry-run", action="store_true", help="show what would be copied")
    args = ap.parse_args(argv)

    root = (args.root or repo_root()).resolve()
    project = args.project.resolve()
    if not project.is_dir():
        print(f"error: project directory does not exist: {project}", file=sys.stderr)
        return 2

    skills = available_skills(root)
    selected = skills if args.all else args.skill
    if not selected:
        print("error: pass --skill NAME (repeatable) or --all", file=sys.stderr)
        return 2
    missing = [s for s in selected if s not in skills]
    if missing:
        print(f"error: unknown skill(s): {', '.join(missing)}", file=sys.stderr)
        print(f"available: {', '.join(skills) or '(none)'}", file=sys.stderr)
        return 2

    dest_root = project / TARGETS[args.target]
    if not args.dry_run:
        dest_root.mkdir(parents=True, exist_ok=True)

    failed = 0
    for name in selected:
        src = root / "skills" / name
        dest = dest_root / name
        if dest.exists() and not args.force:
            print(f"skip {name}: {dest} exists (use --force to replace)", file=sys.stderr)
            failed += 1
            continue
        if args.dry_run:
            print(f"would install {name} -> {dest}")
            continue
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(
            src,
            dest,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
        )
        print(f"installed {name} -> {dest}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
