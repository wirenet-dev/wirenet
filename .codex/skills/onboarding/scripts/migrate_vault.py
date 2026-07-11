#!/usr/bin/env python3
"""Plan or apply a conservative copy into a new canonical Assistant vault."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from vault_doctor import TEMPORARY_HANDOFF_NAMES, inspect, reconcile


EXCLUDED_DIRS = {".git", "__pycache__", ".pytest_cache", ".ruff_cache", ".venv"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def inventory(source: Path) -> tuple[list[Path], list[str]]:
    included: list[Path] = []
    excluded: list[str] = []
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        if path.is_symlink():
            excluded.append(relative.as_posix())
            continue
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            if path.is_file():
                excluded.append(relative.as_posix())
            continue
        if path.name in TEMPORARY_HANDOFF_NAMES or path.suffix in EXCLUDED_SUFFIXES:
            excluded.append(relative.as_posix())
            continue
        if path.is_file():
            included.append(relative)
    return included, excluded


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inventory or copy a vault into a new empty destination, excluding transient artifacts."
    )
    parser.add_argument("--source", required=True)
    parser.add_argument("--destination", required=True)
    parser.add_argument("--apply", action="store_true", help="Apply the planned copy and scaffold reconciliation.")
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve(strict=True)
    destination = Path(args.destination).expanduser().resolve(strict=False)
    if source == destination:
        raise SystemExit("Source and destination must be different paths.")
    if destination.exists() and any(destination.iterdir()):
        raise SystemExit(f"Destination must be absent or empty: {destination}")

    included, excluded = inventory(source)
    created: list[str] = []
    doctor: dict[str, object] | None = None
    if args.apply:
        destination.mkdir(parents=True, exist_ok=True)
        for relative in included:
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / relative, target)
        created = reconcile(destination)
        doctor = inspect(destination)

    result = {
        "ok": bool(doctor["ok"]) if doctor else True,
        "dry_run": not args.apply,
        "source": str(source),
        "destination": str(destination),
        "path_changes": [{"from": str(source), "to": str(destination)}],
        "included_files": [path.as_posix() for path in included],
        "excluded_transient_files": excluded,
        "created_scaffold": created,
        "doctor": doctor,
        "automation_handoffs": "manual verification required",
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
