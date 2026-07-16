#!/usr/bin/env python3
"""Classify a workspace against wirenet Manager v0.2 workspace bindings."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))

from manager_model import (  # noqa: E402
    experiment_id_from_readme,
    experiment_packet_for_id,
    load_workspace_bindings,
    project_id_from_readme,
    project_packet_for_id,
)


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def local_packet(manager_dir: Path, workspace: Path) -> dict[str, object] | None:
    for kind, collection, id_reader in (
        ("tracked", "projects", project_id_from_readme),
        ("experiment", "experiments", experiment_id_from_readme),
    ):
        root = manager_dir / collection
        if not is_within(workspace, root):
            continue
        relative = workspace.relative_to(root)
        if not relative.parts:
            continue
        packet = root / relative.parts[0]
        identity = id_reader(packet / "README.md")
        if identity:
            key = "project_id" if kind == "tracked" else "experiment_id"
            return {
                "classification": kind,
                key: identity,
                "packet": str(packet),
                "manager_native": True,
                "matched_workspace_path": str(packet),
            }
    return None


def bound_matches(manager_dir: Path, workspace: Path) -> list[tuple[Path, dict[str, object]]]:
    registry = load_workspace_bindings(manager_dir)
    matches: list[tuple[Path, dict[str, object]]] = []
    for row in registry.get("projects", []):
        if not isinstance(row, dict):
            continue
        project_id = row.get("project_id")
        raw_path = row.get("path")
        if not isinstance(project_id, str) or not isinstance(raw_path, str):
            continue
        linked = Path(raw_path).expanduser().resolve(strict=False)
        packet = project_packet_for_id(manager_dir, project_id)
        if packet and is_within(workspace, linked):
            matches.append(
                (
                    linked,
                    {
                        "classification": "tracked",
                        "project_id": project_id,
                        "packet": str(packet),
                        "project_packet": str(packet),
                        "manager_native": False,
                        "matched_workspace_path": str(linked),
                    },
                )
            )
    for row in registry.get("experiments", []):
        if not isinstance(row, dict):
            continue
        experiment_id = row.get("experiment_id")
        raw_path = row.get("path")
        if not isinstance(experiment_id, str) or not isinstance(raw_path, str):
            continue
        linked = Path(raw_path).expanduser().resolve(strict=False)
        packet = experiment_packet_for_id(manager_dir, experiment_id)
        if packet and is_within(workspace, linked):
            matches.append(
                (
                    linked,
                    {
                        "classification": "experiment",
                        "experiment_id": experiment_id,
                        "packet": str(packet),
                        "experiment_packet": str(packet),
                        "manager_native": False,
                        "matched_workspace_path": str(linked),
                    },
                )
            )
    for row in registry.get("ignored", []):
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            continue
        linked = Path(str(row["path"])).expanduser().resolve(strict=False)
        if is_within(workspace, linked):
            matches.append(
                (
                    linked,
                    {
                        "classification": "ignored",
                        "matched_workspace_path": str(linked),
                    },
                )
            )
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
    elif packet := local_packet(manager_dir, workspace):
        result.update(packet)
        if packet["classification"] == "tracked":
            result["project_packet"] = packet["packet"]
        else:
            result["experiment_packet"] = packet["packet"]
    elif is_within(workspace, manager_dir):
        result.update({"classification": "manager"})
    elif matches := bound_matches(manager_dir, workspace):
        result.update(matches[0][1])
    else:
        result.update({"classification": "untracked"})
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
