#!/usr/bin/env python3
"""Preview or create an open wirenet Manager Project Pack."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from manager_model import (
    BINDINGS_SCHEMA,
    iso_timestamp,
    load_json,
    load_workspace_bindings,
    new_project_id,
    normalize_slug,
    now,
    project_packet_for_id,
    render_projects_index,
    render_project_agents,
    render_project_goal,
    render_project_log,
    render_project_readme,
    render_project_result,
    write_json,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    parser.add_argument(
        "--description",
        "--summary",
        dest="description",
        required=True,
        help="One-sentence project description (`--summary` remains compatible).",
    )
    parser.add_argument("--manager-dir", default="~/Manager")
    parser.add_argument("--workspace", action="append", default=[])
    parser.add_argument("--project-id", default="")
    parser.add_argument("--slug", default="")
    parser.add_argument("--with-goal", action="store_true")
    parser.add_argument("--with-result", action="store_true")
    parser.add_argument("--with-log", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    manager_dir = Path(args.manager_dir).expanduser().resolve(strict=False)
    slug = normalize_slug(args.slug or args.name)
    project_id = args.project_id or new_project_id()
    packet = manager_dir / "projects" / slug
    workspaces = list(
        dict.fromkeys(
            str(Path(item).expanduser().resolve(strict=False)) for item in args.workspace
        )
    )
    file_names = ["README.md", "AGENTS.md"]
    if args.with_goal:
        file_names.append("GOAL.md")
    if args.with_result:
        file_names.append("RESULT.md")
    if args.with_log:
        file_names.append("log.md")
    files = [packet / name for name in file_names]
    result: dict[str, object] = {
        "ok": True,
        "dry_run": not args.apply,
        "manager_dir": str(manager_dir),
        "project_id": project_id,
        "slug": slug,
        "packet": str(packet),
        "workspace_paths": workspaces,
        "files": [str(path) for path in files],
    }

    if not slug:
        result.update({"ok": False, "error": "project slug is empty"})
        print(json.dumps(result, indent=2))
        return 2
    if not manager_dir.is_dir():
        result.update({"ok": False, "error": "Manager directory does not exist"})
        print(json.dumps(result, indent=2))
        return 2
    if packet.exists():
        result.update({"ok": False, "error": "Project Pack already exists"})
        print(json.dumps(result, indent=2))
        return 2
    if project_packet_for_id(manager_dir, project_id):
        result.update({"ok": False, "error": "project_id already exists"})
        print(json.dumps(result, indent=2))
        return 2

    index_path = manager_dir / "projects/index.md"
    stamp = now()
    try:
        index_path.read_text(encoding="utf-8")
        bindings = load_workspace_bindings(manager_dir)
        manager_metadata = load_json(manager_dir / ".wirenet/manager.json")
    except (OSError, ValueError) as error:
        result.update({"ok": False, "error": str(error)})
        print(json.dumps(result, indent=2))
        return 2
    collections = [bindings.get(name, []) for name in ("projects", "experiments", "ignored")]
    existing_local_paths = {
        row.get("path")
        for collection in collections
        if isinstance(collection, list)
        for row in collection
        if isinstance(row, dict)
    }
    if overlap := sorted(set(workspaces) & existing_local_paths):
        result.update({"ok": False, "error": f"workspace paths are already classified: {overlap}"})
        print(json.dumps(result, indent=2))
        return 2
    if not args.apply:
        print(json.dumps(result, indent=2))
        return 0

    packet.mkdir(parents=True)
    (packet / "README.md").write_text(
        render_project_readme(args.name, args.description, project_id, stamp),
        encoding="utf-8",
    )
    (packet / "AGENTS.md").write_text(render_project_agents(args.name, project_id, stamp), encoding="utf-8")
    if args.with_goal:
        (packet / "GOAL.md").write_text(
            render_project_goal(args.name, args.description, project_id, stamp),
            encoding="utf-8",
        )
    if args.with_result:
        (packet / "RESULT.md").write_text(
            render_project_result(args.name, project_id, stamp), encoding="utf-8"
        )
    if args.with_log:
        (packet / "log.md").write_text(render_project_log(args.name, stamp), encoding="utf-8")

    index_path.write_text(render_projects_index(manager_dir), encoding="utf-8")

    binding_path = manager_dir / ".wirenet/workspace-bindings.json"
    bindings["schema_version"] = BINDINGS_SCHEMA
    bindings["updated_at"] = iso_timestamp(stamp)
    binding_rows = bindings.setdefault("projects", [])
    assert isinstance(binding_rows, list)
    for workspace in workspaces:
        binding_rows.append({"project_id": project_id, "path": workspace})
    write_json(binding_path, bindings)
    manager_metadata["updated_at"] = iso_timestamp(stamp)
    write_json(manager_dir / ".wirenet/manager.json", manager_metadata)

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
