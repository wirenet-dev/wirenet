#!/usr/bin/env python3
"""List likely project folders under roots explicitly approved by the user."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


MARKERS = (".git", "package.json", "pyproject.toml", "Cargo.toml", "go.mod", "AGENTS.md", "README.md")
IGNORED = {".git", ".venv", "node_modules", "dist", "build", "__pycache__", ".pytest_cache"}


def candidates(root: Path, max_depth: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    if not root.is_dir():
        return rows
    pending = [(root, 0)]
    while pending:
        current, depth = pending.pop(0)
        marker_names = [marker for marker in MARKERS if (current / marker).exists()]
        if current != root and marker_names:
            rows.append({"path": str(current.resolve()), "markers": marker_names})
            continue
        if depth >= max_depth:
            continue
        try:
            children = sorted(path for path in current.iterdir() if path.is_dir() and path.name not in IGNORED)
        except OSError:
            continue
        pending.extend((child, depth + 1) for child in children)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="+")
    parser.add_argument("--max-depth", type=int, default=2)
    args = parser.parse_args()
    roots = [Path(item).expanduser().resolve(strict=False) for item in args.root]
    result = {
        "ok": all(root.is_dir() for root in roots),
        "roots": [str(root) for root in roots],
        "max_depth": args.max_depth,
        "candidates": [row for root in roots for row in candidates(root, args.max_depth)],
    }
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
