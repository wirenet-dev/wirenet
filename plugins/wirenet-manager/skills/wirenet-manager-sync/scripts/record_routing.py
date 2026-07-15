#!/usr/bin/env python3
"""Preview or record an experiment/ignored path in the local binding registry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))

from manager_model import BINDINGS_SCHEMA, iso_timestamp, load_bindings, write_json  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--classification", choices=["experiment", "ignored"], required=True)
    parser.add_argument("--manager-dir", default="~/Manager")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    manager_dir = Path(args.manager_dir).expanduser().resolve(strict=False)
    workspace = str(Path(args.path).expanduser().resolve(strict=False))
    registry_path = manager_dir / ".wirenet/project-bindings.json"
    result: dict[str, object] = {
        "ok": manager_dir.is_dir(),
        "dry_run": not args.apply,
        "manager_dir": str(manager_dir),
        "registry": str(registry_path),
        "path": workspace,
        "classification": args.classification,
    }
    if not manager_dir.is_dir():
        result["error"] = "Manager directory does not exist"
        print(json.dumps(result, indent=2))
        return 2

    registry = load_bindings(manager_dir)
    bindings = registry.get("bindings", [])
    if any(isinstance(row, dict) and row.get("path") == workspace for row in bindings):
        result.update({"ok": False, "error": "path is already bound to a Project Pack"})
        print(json.dumps(result, indent=2))
        return 2

    existing_routes = registry.get("routes", [])
    unchanged = any(
        isinstance(row, dict)
        and row.get("path") == workspace
        and row.get("classification") == args.classification
        for row in existing_routes
    ) and sum(
        1 for row in existing_routes if isinstance(row, dict) and row.get("path") == workspace
    ) == 1
    if unchanged:
        result["changed"] = False
        print(json.dumps(result, indent=2))
        return 0

    routes = [
        row
        for row in existing_routes
        if not isinstance(row, dict) or row.get("path") != workspace
    ]
    routes.append({"path": workspace, "classification": args.classification})
    routes.sort(key=lambda row: str(row.get("path", "")) if isinstance(row, dict) else "")
    registry.update(
        {
            "schema_version": BINDINGS_SCHEMA,
            "updated_at": iso_timestamp(),
            "routes": routes,
        }
    )

    result["changed"] = True
    if args.apply:
        write_json(registry_path, registry)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
