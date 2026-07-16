#!/usr/bin/env python3
"""Preview or create a typed WireNet Manager person concept."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from manager_model import (
    MANAGER_SCHEMA,
    iso_date,
    iso_timestamp,
    load_json,
    normalize_slug,
    now,
    write_json,
    yaml_string,
)


def render_person(name: str, context: str) -> str:
    stamp = now()
    return "\n".join(
        [
            "---",
            'type: "Person"',
            f'schema: "{MANAGER_SCHEMA}"',
            f"title: {yaml_string(name)}",
            "visibility: private",
            "status: active",
            f"last_edited: {iso_date(stamp)}",
            "---",
            "",
            f"# {name}",
            "",
            "## Context",
            "",
            context.strip(),
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    parser.add_argument("--context", required=True)
    parser.add_argument("--manager-dir", default="~/Manager")
    parser.add_argument("--slug", default="")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    manager_dir = Path(args.manager_dir).expanduser().resolve(strict=False)
    slug = normalize_slug(args.slug or args.name)
    path = manager_dir / "people" / f"{slug}.md"
    result: dict[str, object] = {
        "ok": True,
        "dry_run": not args.apply,
        "manager_dir": str(manager_dir),
        "slug": slug,
        "path": str(path),
    }

    if not slug:
        result.update({"ok": False, "error": "person slug is empty"})
        print(json.dumps(result, indent=2))
        return 2
    if not args.context.strip():
        result.update({"ok": False, "error": "person context is empty"})
        print(json.dumps(result, indent=2))
        return 2
    if not manager_dir.is_dir():
        result.update({"ok": False, "error": "Manager directory does not exist"})
        print(json.dumps(result, indent=2))
        return 2
    if path.exists():
        result.update({"ok": False, "error": "person concept already exists"})
        print(json.dumps(result, indent=2))
        return 2

    metadata_path = manager_dir / ".wirenet/manager.json"
    try:
        manager_metadata = load_json(metadata_path)
    except ValueError as error:
        result.update({"ok": False, "error": str(error)})
        print(json.dumps(result, indent=2))
        return 2
    if not args.apply:
        print(json.dumps(result, indent=2))
        return 0

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_person(args.name, args.context), encoding="utf-8")
    manager_metadata["updated_at"] = iso_timestamp()
    write_json(metadata_path, manager_metadata)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
