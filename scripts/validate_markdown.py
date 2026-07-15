#!/usr/bin/env python3
"""Validate the Markdown metadata contract used by tests and packaging CI."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


IGNORED_PARTS = {".git", ".pytest_cache", ".ruff_cache", ".venv", "dist", "__pycache__"}
OKF_RESERVED_FILES = {"index.md", "log.md"}


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


def validate_markdown(
    path: Path,
    *,
    skill: bool = False,
    plugin_skill: bool = False,
) -> list[str]:
    errors: list[str] = []
    try:
        data = frontmatter(path)
    except ValueError as error:
        return [f"{path}: {error}"]
    if plugin_skill:
        allowed = {"name", "description", "license", "allowed-tools", "metadata"}
        if unexpected := set(data) - allowed:
            errors.append(f"{path}: unsupported plugin skill keys: {sorted(unexpected)}")
        for key in ("name", "description"):
            if not data.get(key):
                errors.append(f"{path}: {key} must not be empty")
        return errors

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


def validate_okf_reserved(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if path.name == "index.md":
        if text.startswith("---\n"):
            try:
                data = frontmatter(path)
            except ValueError as error:
                return [f"{path}: {error}"]
            if set(data) != {"okf_version"}:
                return [f"{path}: OKF index frontmatter may contain only okf_version"]
        if not re.search(r"(?m)^# .+", text):
            return [f"{path}: OKF index must contain a section heading"]
        return []

    if text.startswith("---\n"):
        return [f"{path}: OKF log is a reserved history file, not a concept document"]
    if not text.startswith("# "):
        return [f"{path}: OKF log must start with a level-one title"]
    dates = re.findall(r"(?m)^## (\d{4}-\d{2}-\d{2})$", text)
    if not dates:
        return [f"{path}: OKF log must contain at least one ISO-date heading"]
    if dates != sorted(dates, reverse=True):
        return [f"{path}: OKF log date headings must be newest first"]
    return []


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
        if path.name in OKF_RESERVED_FILES:
            errors.extend(validate_okf_reserved(path))
            continue
        is_skill = path.name == "SKILL.md" and ".codex" in path.parts and "skills" in path.parts
        is_plugin_skill = path.name == "SKILL.md" and "plugins" in path.parts and "skills" in path.parts
        errors.extend(validate_markdown(path, skill=is_skill, plugin_skill=is_plugin_skill))
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
