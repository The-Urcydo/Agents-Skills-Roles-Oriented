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
import catalog
import roster
from _lib import (
    CATEGORIES,
    INVOCATIONS,
    TIERS,
    FrontMatterError,
    is_valid_skill_name,
    parse_front_matter,
    read_text,
    repo_root,
    role_folders,
    skill_folders,
)

ADR_NAME_RE = re.compile(r"^(\d{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
MARKDOWN_LINK_RE = re.compile(r"(?<!\\)\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
PLACEHOLDER_RE = re.compile(r"\bTODO\b")

ADR_STATUSES = {"proposed", "accepted", "rejected", "deprecated", "superseded"}
REQUIRED = (
    "README.md",
    "AGENTS.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "CHANGELOG.md",
    "SKILLS.md",
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
    "tools/_lib.py",
    "tools/catalog.py",
    "tools/check.py",
    "tools/install.py",
    "tools/new_skill.py",
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


def strip_noise(text: str) -> str:
    """Remove fenced blocks, inline code, and HTML comments before link checks."""
    text = strip_fences(text)
    text = INLINE_CODE_RE.sub("", text)
    return HTML_COMMENT_RE.sub("", text)


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
    try:
        n = len(read_text(p).splitlines())
    except (OSError, UnicodeDecodeError) as exc:
        rep.error("read", "AGENTS.md", str(exc))
        return
    if n > MAX_AGENTS_LINES:
        rep.error(
            "agents-size",
            "AGENTS.md",
            f"{n} lines; keep the always-loaded file under {MAX_AGENTS_LINES}",
        )


def _field_string(
    fm: Dict[str, object], key: str, rep: Report, where: str, missing_code: str
) -> str:
    value = fm.get(key)
    if value is None:
        rep.error(missing_code, where, f"missing '{key}'")
        return ""
    if not isinstance(value, str):
        rep.error("skill-type", where, f"'{key}' must be a string")
        return ""
    value = value.strip()
    if not value:
        rep.error(missing_code, where, f"missing '{key}'")
    return value


def check_skills(root: Path, rep: Report) -> int:
    base = root / "skills"
    if not base.is_dir():
        return 0
    count = 0
    valid = {p.name for p in skill_folders(root)}
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
        if entry.name not in valid:
            rep.error("skill", rel(root, entry), "skill folder has no SKILL.md")
            continue
        sk = entry / "SKILL.md"
        count += 1
        r = rel(root, sk)
        try:
            text = read_text(sk)
        except (OSError, UnicodeDecodeError) as exc:
            rep.error("skill-read", r, str(exc))
            continue
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
        allowed_fields = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
        unknown = sorted(set(fm) - allowed_fields)
        if unknown:
            rep.error("skill-field", r, f"unsupported front matter field(s): {', '.join(unknown)}")
        if "compatibility" in fm:
            compatibility = fm["compatibility"]
            if (
                not isinstance(compatibility, str)
                or not compatibility.strip()
                or len(compatibility) > 500
            ):
                rep.error("skill-compatibility", r, "compatibility must be 1-500 chars")
        if "allowed-tools" in fm:
            tools = fm["allowed-tools"]
            if not isinstance(tools, str):
                rep.error("skill-tools", r, "allowed-tools must be a space-separated string")
            elif not tools.strip():
                rep.error("skill-tools", r, "allowed-tools must not be empty")
            elif "," in tools:
                rep.error(
                    "skill-tools",
                    r,
                    "allowed-tools must be space-separated, not comma-separated",
                )
        name = _field_string(fm, "name", rep, r, "skill-name")
        desc = _field_string(fm, "description", rep, r, "skill-description")
        _field_string(fm, "license", rep, r, "skill-license")
        if name and not is_valid_skill_name(name):
            rep.error(
                "skill-name",
                r,
                "name must be 1-64 chars: lowercase letters, digits, single hyphens",
            )
        elif name and name != entry.name:
            rep.error("skill-name", r, f"name '{name}' must match the folder '{entry.name}'")
        if len(desc) > 1024:
            rep.error("skill-description", r, f"description is {len(desc)} chars; max 1024")
        meta = fm.get("metadata")
        if meta is None:
            rep.error("skill-metadata", r, "missing 'metadata.category'")
        elif not isinstance(meta, dict):
            rep.error("skill-metadata", r, "'metadata' must be a map")
        else:
            for key, value in meta.items():
                if not isinstance(value, str):
                    rep.error("skill-metadata", r, f"metadata.{key} must be a string")
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
        if PLACEHOLDER_RE.search(text):
            rep.warn(
                "skill-placeholder",
                r,
                "contains a TODO placeholder; finish the skill before merging",
            )
        n = len(text.splitlines())
        if n > MAX_SKILL_LINES:
            rep.warn(
                "skill-size",
                r,
                f"{n} lines; move detail into references/ (spec recommends < {MAX_SKILL_LINES})",
            )
        check_skill_links(root, entry, rep)
    return count


def check_markdown_links(
    root: Path,
    p: Path,
    base: Path,
    contain: Path,
    rep: Report,
    outside_code: str,
    broken_code: str,
    scope: str,
    text: str,
) -> None:
    contain = contain.resolve()
    for target in MARKDOWN_LINK_RE.findall(strip_noise(text)):
        target = target.strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = target.split("#", 1)[0]
        if not target:
            continue
        dest = (base / target).resolve()
        try:
            dest.relative_to(contain)
        except ValueError:
            rep.error(outside_code, rel(root, p), f"link leaves the {scope}: {target}")
            continue
        if not dest.exists():
            rep.error(broken_code, rel(root, p), f"link target not found: {target}")


def check_skill_links(root: Path, skill_dir: Path, rep: Report) -> None:
    contain = skill_dir.resolve()
    for p in sorted(skill_dir.rglob("*.md")):
        try:
            p.resolve().relative_to(contain)
        except ValueError:
            rep.error("skill-link", rel(root, p), "skill file resolves outside the skill folder")
            continue
        try:
            raw = read_text(p)
        except (OSError, UnicodeDecodeError) as exc:
            rep.error("skill-read", rel(root, p), str(exc))
            continue
        text = raw
        if p.name == "SKILL.md":
            try:
                _, text = parse_front_matter(raw)
            except FrontMatterError:
                text = raw
        check_markdown_links(
            root,
            p,
            skill_dir,
            skill_dir,
            rep,
            "skill-link",
            "skill-link",
            "skill folder",
            text,
        )


def check_catalog(root: Path, rep: Report) -> None:
    p = root / "SKILLS.md"
    try:
        current = catalog.read_catalog(p)
    except OSError as exc:
        rep.error("catalog-read", "SKILLS.md", str(exc))
        return
    if current is None:
        rep.error("catalog", "SKILLS.md", "generated catalog is missing; run python3 tools/catalog.py")
        return
    if current != catalog.render_catalog(root):
        rep.error("catalog", "SKILLS.md", "generated catalog is out of date; run python3 tools/catalog.py")


def check_docs(root: Path, rep: Report) -> int:
    base = root / "docs"
    if not base.is_dir():
        return 0
    count = 0
    for p in sorted(base.rglob("*.md")):
        count += 1
        check_links(root, p, rep)
    seen = set()
    for name in (
        "README.md",
        "AGENTS.md",
        "SKILLS.md",
        "skills/README.md",
        "roles/README.md",
        "roles/ROSTER.md",
        "agents/README.md",
        "agents/protocols/README.md",
    ):
        p = root / name
        if p.exists() and p not in seen:
            seen.add(p)
            check_links(root, p, rep)
    for folder in ("roles", "agents/protocols"):
        d = root / folder
        if d.is_dir():
            for p in sorted(d.rglob("*.md")):
                if p not in seen:
                    seen.add(p)
                    check_links(root, p, rep)
    return count


def check_links(root: Path, p: Path, rep: Report) -> None:
    try:
        text = read_text(p)
    except (OSError, UnicodeDecodeError) as exc:
        rep.error("read", rel(root, p), str(exc))
        return
    check_markdown_links(
        root,
        p,
        p.parent,
        root,
        rep,
        "link-outside",
        "broken-link",
        "repository",
        text,
    )


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
            text = read_text(p)
        except (OSError, UnicodeDecodeError) as exc:
            rep.error("read", rel(root, p), str(exc))
            continue
        try:
            fm, _ = parse_front_matter(text)
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


def check_roles(root: Path, rep: Report) -> int:
    folders = role_folders(root)
    if not folders:
        return 0
    skill_names = {p.name for p in skill_folders(root)}
    allowed = {
        "role",
        "tier",
        "mission",
        "reads",
        "skills",
        "never",
        "done_when",
        "escalate_when",
    }
    required = (
        "role",
        "tier",
        "mission",
        "reads",
        "skills",
        "never",
        "done_when",
        "escalate_when",
    )
    count = 0
    for entry in folders:
        count += 1
        r = rel(root, entry / "ROLE.md")
        try:
            text = read_text(entry / "ROLE.md")
        except (OSError, UnicodeDecodeError) as exc:
            rep.error("role-read", r, str(exc))
            continue
        try:
            fm, _ = parse_front_matter(text)
        except FrontMatterError as exc:
            rep.error("role-front-matter", r, str(exc))
            continue
        if fm is None:
            rep.error(
                "role-front-matter",
                r,
                "missing front matter (role, tier, mission, reads, skills, never, done_when, escalate_when)",
            )
            continue
        unknown = sorted(set(fm) - allowed)
        if unknown:
            rep.error("role-field", r, f"unsupported front matter field(s): {', '.join(unknown)}")
        for key in required:
            if key not in fm:
                rep.error("role-field", r, f"missing '{key}'")

        role = fm.get("role")
        if not isinstance(role, str) or not role.strip():
            rep.error("role-name", r, "role must be a non-empty string")
        elif role.strip() != entry.name:
            rep.error("role-name", r, f"role '{role.strip()}' must match the folder '{entry.name}'")

        tier = fm.get("tier")
        if not isinstance(tier, str) or tier.strip() not in TIERS:
            rep.error("role-tier", r, f"tier must be one of {', '.join(TIERS)}")

        mission = fm.get("mission")
        if not isinstance(mission, str) or not mission.strip():
            rep.error("role-field", r, "mission must be a non-empty string")

        for key in ("reads", "never"):
            value = fm.get(key)
            if not isinstance(value, list) or not value:
                rep.error("role-field", r, f"{key} must be a non-empty list")
            elif not all(isinstance(item, str) and item.strip() for item in value):
                rep.error("role-field", r, f"{key} must contain non-empty strings")

        skills = fm.get("skills")
        if not isinstance(skills, list):
            rep.error("role-field", r, "skills must be a list (empty is allowed)")
        else:
            for name in skills:
                if not isinstance(name, str) or not name.strip():
                    rep.error("role-field", r, "skills must contain non-empty strings")
                elif name.strip() not in skill_names:
                    rep.error("role-skill", r, f"skill '{name.strip()}' does not exist")

        done = fm.get("done_when")
        if not isinstance(done, str) or not done.strip():
            rep.error("role-field", r, "done_when must be a non-empty string")

        escalate = fm.get("escalate_when")
        if isinstance(escalate, list):
            if not escalate or not all(isinstance(item, str) and item.strip() for item in escalate):
                rep.error("role-field", r, "escalate_when must be a non-empty string or list")
        elif not isinstance(escalate, str) or not escalate.strip():
            rep.error("role-field", r, "escalate_when must be a non-empty string or list")

    roster_path = root / "roles" / "ROSTER.md"
    if not roster_path.exists():
        rep.error("roster", "roles/ROSTER.md", "generated roster is missing; run python3 tools/roster.py")
    else:
        try:
            current = roster.read_roster(roster_path)
        except OSError as exc:
            rep.error("roster-read", "roles/ROSTER.md", str(exc))
        else:
            if current != roster.render_roster(root):
                rep.error(
                    "roster",
                    "roles/ROSTER.md",
                    "generated roster is out of date; run python3 tools/roster.py",
                )
    return count


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
    check_catalog(root, rep)
    roles = check_roles(root, rep)
    docs = check_docs(root, rep)
    check_adrs(root, rep)
    for f in sorted(rep.items, key=lambda x: (x.level, x.where, x.code)):
        print(f"{f.level.upper():5} {f.code:20} {f.where}  {f.msg}")
    errors = rep.count("error")
    warnings = rep.count("warn")
    if errors or (args.strict and warnings):
        print(f"failed: {errors} error(s), {warnings} warning(s)")
        return 1
    print(f"ok: {skills} skill(s), {roles} role(s), {docs} doc(s), {warnings} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
