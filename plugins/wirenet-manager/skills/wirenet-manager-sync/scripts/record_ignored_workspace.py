#!/usr/bin/env python3
"""Preview or record an ignored path in the local workspace registry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))

from manager_model import (  # noqa: E402
    BINDINGS_SCHEMA,
    iso_timestamp,
    load_workspace_bindings,
    workspace_paths,
    write_json,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--manager-dir", default="~/Manager")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    manager_dir = Path(args.manager_dir).expanduser().resolve(strict=False)
    workspace = str(Path(args.path).expanduser().resolve(strict=False))
    registry_path = manager_dir / ".wirenet/workspace-bindings.json"
    result: dict[str, object] = {
        "ok": manager_dir.is_dir(),
        "dry_run": not args.apply,
        "manager_dir": str(manager_dir),
        "registry": str(registry_path),
        "path": workspace,
        "classification": "ignored",
    }
    if not manager_dir.is_dir():
        result["error"] = "Manager directory does not exist"
        print(json.dumps(result, indent=2))
        return 2

    registry = load_workspace_bindings(manager_dir)
    project_or_experiment_paths = {
        str(row.get("path"))
        for name in ("projects", "experiments")
        for row in registry.get(name, [])
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    if workspace in project_or_experiment_paths:
        result.update({"ok": False, "error": "path is already bound to a packet"})
        print(json.dumps(result, indent=2))
        return 2

    ignored = registry.get("ignored", [])
    assert isinstance(ignored, list)
    unchanged = any(isinstance(row, dict) and row.get("path") == workspace for row in ignored)
    if unchanged:
        result["changed"] = False
        print(json.dumps(result, indent=2))
        return 0

    assert workspace not in workspace_paths(registry)
    ignored.append({"path": workspace})
    ignored.sort(key=lambda row: str(row.get("path", "")) if isinstance(row, dict) else "")
    registry.update(
        {
            "schema_version": BINDINGS_SCHEMA,
            "updated_at": iso_timestamp(),
            "ignored": ignored,
        }
    )
    result["changed"] = True
    if args.apply:
        write_json(registry_path, registry)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
