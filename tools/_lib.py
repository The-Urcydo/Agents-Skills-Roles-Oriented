#!/usr/bin/env python3
"""Shared helpers for the repository tools. Standard library only."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Tuple


def repo_root() -> Path:
    """Repository root, based on this file's location."""
    return Path(__file__).resolve().parent.parent


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class FrontMatterError(ValueError):
    """Raised when YAML front matter cannot be parsed."""


def _scalar(value: str) -> Any:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
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
