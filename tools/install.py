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
import tempfile
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import repo_root, skill_folders

TARGETS = {
    "claude": ".claude/skills",
    "opencode": ".opencode/skills",
    "agents": ".agents/skills",
}

IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")


def available_skills(root: Path) -> List[str]:
    return [p.name for p in skill_folders(root)]


def remove_path(path: Path) -> None:
    """Remove a file, symlink, or directory at path."""
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


def install_skill(src: Path, dest: Path) -> None:
    """Copy src to dest, keeping the old dest if the copy fails."""
    tmp = Path(tempfile.mkdtemp(prefix=f".{dest.name}.new-", dir=dest.parent))
    backup: Optional[Path] = None
    try:
        shutil.copytree(src, tmp, dirs_exist_ok=True, ignore=IGNORE)
        try:
            tmp.chmod(src.stat().st_mode & 0o777)
        except OSError:
            pass
        if dest.exists() or dest.is_symlink():
            backup = Path(tempfile.mkdtemp(prefix=f".{dest.name}.old-", dir=dest.parent))
            backup.rmdir()
            dest.rename(backup)
        try:
            tmp.rename(dest)
        except BaseException:
            if backup is not None and not (dest.exists() or dest.is_symlink()):
                backup.rename(dest)
                backup = None
            raise
        if backup is not None:
            try:
                remove_path(backup)
            except OSError:
                pass
            backup = None
    finally:
        if tmp.exists() or tmp.is_symlink():
            if tmp.is_symlink() or tmp.is_file():
                tmp.unlink()
            else:
                shutil.rmtree(tmp, ignore_errors=True)


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
    ap.add_argument("--dry-run", action="store_true", help="show what would be copied; exits 1 when the real run would skip")
    args = ap.parse_args(argv)

    root = (args.root or repo_root()).expanduser().resolve()
    project = args.project.expanduser().resolve()
    if not project.is_dir():
        print(f"error: project directory does not exist: {project}", file=sys.stderr)
        return 2

    skills = available_skills(root)
    if args.all and args.skill:
        print("error: use either --all or --skill, not both", file=sys.stderr)
        return 2
    selected = list(dict.fromkeys(skills if args.all else args.skill))
    if not selected:
        if args.all:
            print("error: no skills to install", file=sys.stderr)
        else:
            print("error: pass --skill NAME (repeatable) or --all", file=sys.stderr)
        return 2
    missing = [s for s in selected if s not in skills]
    if missing:
        print(f"error: unknown skill(s): {', '.join(missing)}", file=sys.stderr)
        print(f"available: {', '.join(skills) or '(none)'}", file=sys.stderr)
        return 2

    dest_root = project / TARGETS[args.target]
    if not args.dry_run:
        try:
            dest_root.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            print(f"error: cannot create {dest_root}: {exc}", file=sys.stderr)
            return 2

    failed = 0
    for name in selected:
        src = root / "skills" / name
        dest = dest_root / name
        exists = dest.exists() or dest.is_symlink()
        if exists and not args.force:
            if args.dry_run:
                print(f"would skip {name}: {dest} exists")
            else:
                print(f"skip {name}: {dest} exists (use --force to replace)", file=sys.stderr)
            failed += 1
            continue
        if args.dry_run:
            action = "replace" if exists else "install"
            print(f"would {action} {name} -> {dest}")
            continue
        try:
            install_skill(src, dest)
        except OSError as exc:
            print(f"error: {name}: {exc}", file=sys.stderr)
            failed += 1
            continue
        print(f"installed {name} -> {dest}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
