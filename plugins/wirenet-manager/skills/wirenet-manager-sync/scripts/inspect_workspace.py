#!/usr/bin/env python3
"""Classify a workspace against local WireNet Manager bindings."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))

from manager_model import load_bindings, project_packet_for_id  # noqa: E402


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def binding_matches(manager_dir: Path, workspace: Path) -> list[tuple[Path, str, Path]]:
    matches: list[tuple[Path, str, Path]] = []
    bindings = load_bindings(manager_dir)
    for row in bindings.get("bindings", []):
        if not isinstance(row, dict):
            continue
        project_id = row.get("project_id")
        raw_path = row.get("path")
        if not isinstance(project_id, str) or not isinstance(raw_path, str):
            continue
        linked_path = Path(raw_path).expanduser().resolve(strict=False)
        packet = project_packet_for_id(manager_dir, project_id)
        if packet and is_within(workspace, linked_path):
            matches.append((linked_path, project_id, packet))
    return sorted(matches, key=lambda item: len(item[0].parts), reverse=True)


def route_matches(manager_dir: Path, workspace: Path) -> list[tuple[Path, str]]:
    matches: list[tuple[Path, str]] = []
    bindings = load_bindings(manager_dir)
    for row in bindings.get("routes", []):
        if not isinstance(row, dict):
            continue
        raw_path = row.get("path")
        classification = row.get("classification")
        if not isinstance(raw_path, str) or classification not in {"experiment", "ignored"}:
            continue
        routed_path = Path(raw_path).expanduser().resolve(strict=False)
        if is_within(workspace, routed_path):
            matches.append((routed_path, classification))
    return sorted(matches, key=lambda item: len(item[0].parts), reverse=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manager-dir", default=os.environ.get("WIRENET_MANAGER_DIR", "~/Manager"))
    parser.add_argument("--workspace", default=os.getcwd())
    args = parser.parse_args()

    manager_dir = Path(args.manager_dir).expanduser().resolve(strict=False)
    workspace = Path(args.workspace).expanduser().resolve(strict=False)
    result: dict[str, object] = {
        "ok": True,
        "manager_dir": str(manager_dir),
        "manager_exists": manager_dir.is_dir(),
        "workspace": str(workspace),
    }
    if not manager_dir.is_dir():
        result.update({"ok": False, "classification": "manager-missing"})
    elif is_within(workspace, manager_dir):
        result.update({"classification": "manager"})
    else:
        projects = binding_matches(manager_dir, workspace)
        routes = route_matches(manager_dir, workspace)
        project_depth = len(projects[0][0].parts) if projects else -1
        route_depth = len(routes[0][0].parts) if routes else -1
        if projects and project_depth >= route_depth:
            linked_path, project_id, packet = projects[0]
            result.update(
                {
                    "classification": "tracked",
                    "project_id": project_id,
                    "project_packet": str(packet),
                    "matched_workspace_path": str(linked_path),
                }
            )
        elif routes:
            routed_path, classification = routes[0]
            result.update(
                {
                    "classification": classification,
                    "matched_workspace_path": str(routed_path),
                }
            )
        else:
            result.update({"classification": "untracked"})
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
