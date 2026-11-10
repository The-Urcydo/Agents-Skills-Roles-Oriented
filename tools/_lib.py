#!/usr/bin/env python3
"""Shared helpers for the repository tools. Standard library only."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CATEGORIES = ("engineering", "productivity", "design", "repo")
INVOCATIONS = ("model", "user", "both")


def repo_root() -> Path:
    """Repository root, based on this file's location."""
    return Path(__file__).resolve().parent.parent


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def is_valid_skill_name(name: str) -> bool:
    return bool(SKILL_NAME_RE.fullmatch(name)) and 1 <= len(name) <= 64


def skill_folders(root: Path) -> List[Path]:
    """Skill folders that contain a SKILL.md, sorted by name."""
    base = root / "skills"
    if not base.is_dir():
        return []
    return [
        p
        for p in sorted(base.iterdir())
        if p.is_dir()
        and not p.name.startswith(".")
        and p.name != "README.md"
        and (p / "SKILL.md").exists()
    ]


class FrontMatterError(ValueError):
    """Raised when YAML front matter cannot be parsed."""


def _scalar(value: str) -> Any:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1]
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_scalar(part) for part in inner.split(",")]
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    return value


def parse_front_matter(text: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """Parse a leading '---' YAML block.

    Supports the subset this repository uses: scalars, quoted strings, inline
    lists, and one level of nested maps or lists. Returns (data, body); data is
    None when there is no front matter.
    """
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        raise FrontMatterError("front matter has no closing '---'")
    raw = text[4:end]
    body = text[end + 4:]
    if body.startswith("\n"):
        body = body[1:]

    data: Dict[str, Any] = {}
    current_key: Optional[str] = None
    current_kind: Optional[str] = None

    for lineno, line in enumerate(raw.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indented = line.startswith((" ", "\t"))
        stripped = line.strip()

        if indented:
            if current_key is None:
                raise FrontMatterError(f"line {lineno}: indented value without a parent key")
            if current_kind is None:
                current_kind = "list" if stripped.startswith("- ") else "map"
                data[current_key] = [] if current_kind == "list" else {}
            if current_kind == "list":
                if not stripped.startswith("- "):
                    raise FrontMatterError(f"line {lineno}: expected a list item")
                data[current_key].append(_scalar(stripped[2:]))
            else:
                key, sep, value = stripped.partition(":")
                if not sep:
                    raise FrontMatterError(f"line {lineno}: expected 'key: value'")
                data[current_key][key.strip()] = _scalar(value)
            continue

        key, sep, value = line.partition(":")
        if not sep:
            raise FrontMatterError(f"line {lineno}: expected 'key: value'")
        key = key.strip()
        value = value.strip()
        if not key:
            raise FrontMatterError(f"line {lineno}: empty key")
        if value == "":
            data[key] = None
            current_key = key
            current_kind = None
        else:
            data[key] = _scalar(value)
            current_key = None
            current_kind = None

    return data, body
