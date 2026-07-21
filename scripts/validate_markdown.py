#!/usr/bin/env python3
"""Validate v0.5 markdown conventions: checked like code, not typed.

Rules: every markdown file has a level-1 heading near the top; plugin
skills carry exactly the supported frontmatter; no merge-conflict markers.
No frontmatter is required anywhere else (ADR 004).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

IGNORED_PARTS = {".git", ".pytest_cache", ".ruff_cache", ".venv", "dist",
                 "__pycache__", "node_modules", "LICENSES"}
SKILL_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
CONFLICT = re.compile(r"^(<{7} |={7}$|>{7} )", re.MULTILINE)


def frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    data: dict[str, str] = {}
    for line in parts[1].splitlines():
        if not line.strip() or line[0].isspace():
            continue
        key, sep, value = line.partition(":")
        if sep:
            data[key.strip()] = value.strip().strip("\"'")
    return data, parts[2]


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return [f"{path}: empty file"]
    if CONFLICT.search(text):
        errors.append(f"{path}: merge conflict markers")
    data, body = frontmatter(text)
    if path.name == "SKILL.md":
        for key in ("name", "description"):
            if not data.get(key):
                errors.append(f"{path}: skill frontmatter missing {key}")
        if unexpected := set(data) - SKILL_KEYS:
            errors.append(f"{path}: unsupported skill keys: {sorted(unexpected)}")
    head = [line for line in body.splitlines()[:10]]
    if not any(line.startswith("# ") for line in head):
        errors.append(f"{path}: no level-1 heading near the top")
    return errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    args = parser.parse_args(argv)
    errors: list[str] = []
    for path in sorted(args.root.rglob("*.md")):
        if IGNORED_PARTS.intersection(path.parts):
            continue
        errors.extend(validate(path))
    for line in errors:
        print(line)
    print(f"validate_markdown: {'FAIL' if errors else 'ok'} ({len(errors)} error(s))")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
