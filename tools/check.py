#!/usr/bin/env python3
"""Repository health check for the skill library.

Usage:
  python3 tools/check.py            # errors fail; warnings are printed
  python3 tools/check.py --strict   # warnings also fail
  python3 tools/check.py --root DIR # check another checkout (used by tests)

Levels: error (must fix), warn (should fix). Standard library only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import FrontMatterError, parse_front_matter, read_text, repo_root

SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ADR_NAME_RE = re.compile(r"^(\d{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"```.*?```", re.S)

CATEGORIES = {"engineering", "productivity", "design", "repo"}
INVOCATIONS = {"model", "user", "both"}
ADR_STATUSES = {"proposed", "accepted", "rejected", "deprecated", "superseded"}
REQUIRED = (
    "README.md",
    "AGENTS.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "CHANGELOG.md",
    "docs/INDEX.md",
    "skills/README.md",
    "roles/README.md",
    "agents/README.md",
    "agents/protocols/README.md",
    "agents/adapters/README.md",
    "agents/evals/README.md",
    ".github/CODEOWNERS",
    ".github/pull_request_template.md",
    ".github/workflows/check.yml",
    "tools/tests/test_tools.py",
)
MAX_AGENTS_LINES = 100
MAX_SKILL_LINES = 500


@dataclass
class Finding:
    level: str
    code: str
    where: str
    msg: str


class Report:
    def __init__(self) -> None:
        self.items: List[Finding] = []

    def add(self, level: str, code: str, where: str, msg: str) -> None:
        self.items.append(Finding(level, code, where, msg))

    def error(self, code: str, where: str, msg: str) -> None:
        self.add("error", code, where, msg)

    def warn(self, code: str, where: str, msg: str) -> None:
        self.add("warn", code, where, msg)

    def count(self, level: str) -> int:
        return sum(1 for f in self.items if f.level == level)


def rel(root: Path, p: Path) -> str:
    try:
        return p.relative_to(root).as_posix()
    except ValueError:
        return p.as_posix()


def strip_fences(text: str) -> str:
    return FENCE_RE.sub("", text)


def check_required(root: Path, rep: Report) -> None:
    for item in REQUIRED:
        p = root / item
        if not p.exists():
            rep.error("required", item, "required file is missing")
    if not (root / "skills").is_dir():
        rep.error("required", "skills/", "skills/ folder is missing")


def check_agents(root: Path, rep: Report) -> None:
    p = root / "AGENTS.md"
    if not p.exists():
        return
    n = len(read_text(p).splitlines())
    if n > MAX_AGENTS_LINES:
        rep.error(
            "agents-size",
            "AGENTS.md",
            f"{n} lines; keep the always-loaded file under {MAX_AGENTS_LINES}",
        )


def check_skills(root: Path, rep: Report) -> int:
    base = root / "skills"
    if not base.is_dir():
        return 0
    count = 0
    for entry in sorted(base.iterdir()):
        if entry.name == "README.md" or entry.name.startswith("."):
            continue
        if not entry.is_dir():
            rep.error(
                "skill-layout",
                rel(root, entry),
                "skills/ holds one folder per skill (and README.md only)",
            )
            continue
        sk = entry / "SKILL.md"
        if not sk.exists():
            rep.error("skill", rel(root, entry), "skill folder has no SKILL.md")
            continue
        count += 1
        text = read_text(sk)
        r = rel(root, sk)
        try:
            fm, _ = parse_front_matter(text)
        except FrontMatterError as exc:
            rep.error("skill-front-matter", r, str(exc))
            continue
        if fm is None:
            rep.error(
                "skill-front-matter",
                r,
                "missing front matter (name, description, license, metadata)",
            )
            continue
        name = str(fm.get("name") or "").strip()
        desc = str(fm.get("description") or "").strip()
        license_name = str(fm.get("license") or "").strip()
        if not name:
            rep.error("skill-name", r, "missing 'name'")
        elif not SKILL_NAME_RE.fullmatch(name) or len(name) > 64:
            rep.error(
                "skill-name",
                r,
                "name must be 1-64 chars: lowercase letters, digits, single hyphens",
            )
        elif name != entry.name:
            rep.error("skill-name", r, f"name '{name}' must match the folder '{entry.name}'")
        if not desc:
            rep.error("skill-description", r, "missing 'description'")
        elif len(desc) > 1024:
            rep.error("skill-description", r, f"description is {len(desc)} chars; max 1024")
        if not license_name:
            rep.error("skill-license", r, "missing 'license' (required by this repository)")
        meta = fm.get("metadata")
        if meta is None:
            rep.error("skill-metadata", r, "missing 'metadata.category'")
        elif not isinstance(meta, dict):
            rep.error("skill-metadata", r, "'metadata' must be a map")
        else:
            category = str(meta.get("category") or "").strip()
            if category not in CATEGORIES:
                rep.error(
                    "skill-category",
                    r,
                    f"metadata.category must be one of {', '.join(sorted(CATEGORIES))}",
                )
            invocation = str(meta.get("invocation") or "both").strip()
            if invocation not in INVOCATIONS:
                rep.error(
                    "skill-invocation",
                    r,
                    f"metadata.invocation must be one of {', '.join(sorted(INVOCATIONS))}",
                )
        n = len(text.splitlines())
        if n > MAX_SKILL_LINES:
            rep.warn(
                "skill-size",
                r,
                f"{n} lines; move detail into references/ (spec recommends < {MAX_SKILL_LINES})",
            )
        check_skill_links(root, entry, sk, rep)
    return count


def check_skill_links(root: Path, skill_dir: Path, sk: Path, rep: Report) -> None:
    text = strip_fences(read_text(sk))
    for target in MARKDOWN_LINK_RE.findall(text):
        target = target.strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = target.split("#", 1)[0]
        if not target:
            continue
        dest = (skill_dir / target).resolve()
        try:
            dest.relative_to(skill_dir.resolve())
        except ValueError:
            rep.error("skill-link", rel(root, sk), f"link leaves the skill folder: {target}")
            continue
        if not dest.exists():
            rep.error("skill-link", rel(root, sk), f"link target not found: {target}")


def check_docs(root: Path, rep: Report) -> int:
    base = root / "docs"
    if not base.is_dir():
        return 0
    count = 0
    for p in sorted(base.rglob("*.md")):
        count += 1
        check_links(root, p, rep)
    for name in ("README.md", "AGENTS.md"):
        p = root / name
        if p.exists():
            check_links(root, p, rep)
    for name in ("skills/README.md", "roles/README.md", "agents/README.md"):
        p = root / name
        if p.exists():
            check_links(root, p, rep)
    return count


def check_links(root: Path, p: Path, rep: Report) -> None:
    text = strip_fences(read_text(p))
    for target in MARKDOWN_LINK_RE.findall(text):
        target = target.strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = target.split("#", 1)[0]
        if not target:
            continue
        dest = (p.parent / target).resolve()
        try:
            dest.relative_to(root.resolve())
        except ValueError:
            rep.error("link-outside", rel(root, p), f"link leaves the repository: {target}")
            continue
        if not dest.exists():
            rep.error("broken-link", rel(root, p), f"link target not found: {target}")


def check_adrs(root: Path, rep: Report) -> None:
    base = root / "docs" / "decisions"
    if not base.is_dir():
        return
    seen: Dict[str, Path] = {}
    for p in sorted(base.glob("*.md")):
        if p.name == "README.md":
            continue
        m = ADR_NAME_RE.match(p.name)
        if not m:
            rep.error("adr-name", rel(root, p), "ADR files are named NNNN-kebab-title.md")
            continue
        number = m.group(1)
        if number in seen:
            rep.error("adr-number", rel(root, p), f"number {number} also used by {seen[number].name}")
        seen[number] = p
        try:
            fm, _ = parse_front_matter(read_text(p))
        except FrontMatterError as exc:
            rep.error("adr-front-matter", rel(root, p), str(exc))
            continue
        if fm is None:
            rep.error(
                "adr-front-matter",
                rel(root, p),
                "missing front matter (title, status, date, summary)",
            )
            continue
        for key in ("title", "status", "date", "summary"):
            if not str(fm.get(key) or "").strip():
                rep.error("adr-front-matter", rel(root, p), f"missing '{key}'")
        status = str(fm.get("status") or "")
        if status and status not in ADR_STATUSES:
            rep.error(
                "adr-status",
                rel(root, p),
                f"status '{status}' not in {', '.join(sorted(ADR_STATUSES))}",
            )
        date = str(fm.get("date") or "")
        if date:
            try:
                dt.date.fromisoformat(date)
            except ValueError:
                rep.error("adr-date", rel(root, p), f"date '{date}' is not ISO YYYY-MM-DD")


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--strict", action="store_true", help="warnings also fail")
    ap.add_argument("--root", type=Path, default=None, help="repository root (default: this checkout)")
    args = ap.parse_args(argv)
    root = (args.root or repo_root()).resolve()
    if not root.is_dir():
        print(f"ERROR  root  {root}  not a directory")
        return 2
    rep = Report()
    check_required(root, rep)
    check_agents(root, rep)
    skills = check_skills(root, rep)
    docs = check_docs(root, rep)
    check_adrs(root, rep)
    for f in sorted(rep.items, key=lambda x: (x.level, x.where, x.code)):
        print(f"{f.level.upper():5} {f.code:20} {f.where}  {f.msg}")
    errors = rep.count("error")
    warnings = rep.count("warn")
    if errors or (args.strict and warnings):
        print(f"failed: {errors} error(s), {warnings} warning(s)")
        return 1
    print(f"ok: {skills} skill(s), {docs} doc(s), {warnings} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
