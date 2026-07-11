#!/usr/bin/env python3
"""Validate the Markdown metadata contract used by tests and packaging CI."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


IGNORED_PARTS = {".git", ".pytest_cache", ".ruff_cache", ".venv", "dist", "__pycache__"}


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or text.count("---") < 2:
        raise ValueError("missing frontmatter")
    raw = text.split("---", 2)[1]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line[0].isspace():
            continue
        key, separator, value = line.partition(":")
        if not separator:
            raise ValueError(f"top-level frontmatter line must be key/value: {line}")
        data[key.strip()] = value.strip().strip('"\'')
    return data


def validate_markdown(path: Path, *, skill: bool = False) -> list[str]:
    errors: list[str] = []
    try:
        data = frontmatter(path)
    except ValueError as error:
        return [f"{path}: {error}"]
    edited = data.get("last_edited", "")
    try:
        date.fromisoformat(edited)
    except ValueError:
        errors.append(f"{path}: last_edited must be an ISO date, got {edited!r}")
    if skill:
        expected = {"name", "description", "last_edited"}
        if set(data) != expected:
            errors.append(f"{path}: skill frontmatter keys must be {sorted(expected)}, got {sorted(data)}")
        for key in ("name", "description"):
            if not data.get(key):
                errors.append(f"{path}: {key} must not be empty")
    return errors


def validate_tree(root: Path) -> list[str]:
    markdown = [
        path
        for path in sorted(root.rglob("*.md"))
        if not any(part in IGNORED_PARTS for part in path.relative_to(root).parts)
    ]
    if not markdown:
        return [f"{root}: no Markdown files found"]
    errors: list[str] = []
    for path in markdown:
        is_skill = path.name == "SKILL.md" and ".codex" in path.parts and "skills" in path.parts
        errors.extend(validate_markdown(path, skill=is_skill))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors = validate_tree(root)
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Markdown metadata valid: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
