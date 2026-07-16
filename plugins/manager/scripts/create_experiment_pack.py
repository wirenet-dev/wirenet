#!/usr/bin/env python3
"""Preview or create a bounded wirenet Manager Experiment Pack."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from manager_model import (
    BINDINGS_SCHEMA,
    experiment_packet_for_id,
    iso_timestamp,
    load_json,
    load_workspace_bindings,
    new_experiment_id,
    normalize_slug,
    now,
    render_experiment_agents,
    render_experiment_readme,
    render_experiment_result,
    render_experiments_index,
    workspace_paths,
    write_json,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    parser.add_argument("--question", required=True)
    parser.add_argument("--decision-criterion", required=True)
    parser.add_argument("--manager-dir", default="~/Manager")
    parser.add_argument("--workspace", action="append", default=[])
    parser.add_argument("--experiment-id", default="")
    parser.add_argument("--slug", default="")
    parser.add_argument("--with-result", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    manager_dir = Path(args.manager_dir).expanduser().resolve(strict=False)
    slug = normalize_slug(args.slug or args.name)
    experiment_id = args.experiment_id or new_experiment_id()
    packet = manager_dir / "experiments" / slug
    workspaces = list(
        dict.fromkeys(
            str(Path(item).expanduser().resolve(strict=False)) for item in args.workspace
        )
    )
    file_names = ["README.md", "AGENTS.md"]
    if args.with_result:
        file_names.append("RESULT.md")
    result: dict[str, object] = {
        "ok": True,
        "dry_run": not args.apply,
        "manager_dir": str(manager_dir),
        "experiment_id": experiment_id,
        "slug": slug,
        "packet": str(packet),
        "workspace_paths": workspaces,
        "files": [str(packet / name) for name in file_names],
    }

    if not slug:
        result.update({"ok": False, "error": "experiment slug is empty"})
        print(json.dumps(result, indent=2))
        return 2
    if not manager_dir.is_dir():
        result.update({"ok": False, "error": "Manager directory does not exist"})
        print(json.dumps(result, indent=2))
        return 2
    if packet.exists():
        result.update({"ok": False, "error": "Experiment Pack already exists"})
        print(json.dumps(result, indent=2))
        return 2
    if experiment_packet_for_id(manager_dir, experiment_id):
        result.update({"ok": False, "error": "experiment_id already exists"})
        print(json.dumps(result, indent=2))
        return 2

    stamp = now()
    try:
        bindings = load_workspace_bindings(manager_dir)
        manager_metadata = load_json(manager_dir / ".wirenet/manager.json")
    except (OSError, ValueError) as error:
        result.update({"ok": False, "error": str(error)})
        print(json.dumps(result, indent=2))
        return 2
    if overlap := sorted(set(workspaces) & workspace_paths(bindings)):
        result.update({"ok": False, "error": f"workspace paths are already classified: {overlap}"})
        print(json.dumps(result, indent=2))
        return 2
    if not args.apply:
        print(json.dumps(result, indent=2))
        return 0

    packet.mkdir(parents=True)
    (packet / "README.md").write_text(
        render_experiment_readme(
            args.name,
            args.question,
            args.decision_criterion,
            experiment_id,
            stamp,
        ),
        encoding="utf-8",
    )
    (packet / "AGENTS.md").write_text(
        render_experiment_agents(args.name, experiment_id, stamp), encoding="utf-8"
    )
    if args.with_result:
        (packet / "RESULT.md").write_text(
            render_experiment_result(args.name, experiment_id, stamp), encoding="utf-8"
        )

    (manager_dir / "experiments/index.md").write_text(
        render_experiments_index(manager_dir), encoding="utf-8"
    )
    rows = bindings.setdefault("experiments", [])
    assert isinstance(rows, list)
    rows.extend({"experiment_id": experiment_id, "path": workspace} for workspace in workspaces)
    bindings["schema_version"] = BINDINGS_SCHEMA
    bindings["updated_at"] = iso_timestamp(stamp)
    write_json(manager_dir / ".wirenet/workspace-bindings.json", bindings)
    manager_metadata["updated_at"] = iso_timestamp(stamp)
    write_json(manager_dir / ".wirenet/manager.json", manager_metadata)

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
