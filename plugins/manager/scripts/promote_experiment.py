#!/usr/bin/env python3
"""Preview or promote an Experiment Pack into a durable Project Pack."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from manager_model import (
    BINDINGS_SCHEMA,
    experiment_id_from_readme,
    experiment_packet_for_id,
    frontmatter,
    iso_date,
    iso_timestamp,
    load_json,
    load_workspace_bindings,
    new_project_id,
    normalize_slug,
    now,
    project_packet_for_id,
    render_experiments_index,
    render_project_agents,
    render_project_readme,
    render_projects_index,
    update_frontmatter,
    write_json,
)


def resolve_experiment(manager_dir: Path, identity: str) -> Path | None:
    packet = experiment_packet_for_id(manager_dir, identity)
    if packet:
        return packet
    candidate = manager_dir / "experiments" / identity
    return candidate if (candidate / "README.md").is_file() else None


def append_section(content: str, heading: str, body: str) -> str:
    marker = f"## {heading}"
    if marker in content:
        return content
    return content.rstrip() + f"\n\n{marker}\n\n{body}\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", help="Experiment ID or packet slug")
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--project-slug", default="")
    parser.add_argument("--project-id", default="")
    parser.add_argument("--manager-dir", default="~/Manager")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    manager_dir = Path(args.manager_dir).expanduser().resolve(strict=False)
    experiment = resolve_experiment(manager_dir, args.experiment)
    if not experiment:
        print(json.dumps({"ok": False, "error": "Experiment Pack not found"}, indent=2))
        return 2
    experiment_readme = experiment / "README.md"
    experiment_metadata = frontmatter(experiment_readme)
    experiment_id = experiment_id_from_readme(experiment_readme)
    if not experiment_id:
        print(json.dumps({"ok": False, "error": "Experiment Pack is missing experiment_id"}, indent=2))
        return 2
    current_status = experiment_metadata.get("status", "active")
    if current_status == "promoted":
        print(json.dumps({"ok": False, "error": "Experiment Pack is already promoted"}, indent=2))
        return 2

    project_id = args.project_id or new_project_id()
    slug = normalize_slug(args.project_slug or args.project_name)
    project = manager_dir / "projects" / slug
    if not slug:
        print(json.dumps({"ok": False, "error": "project slug is empty"}, indent=2))
        return 2
    if project.exists():
        print(json.dumps({"ok": False, "error": "Project Pack already exists"}, indent=2))
        return 2
    if project_packet_for_id(manager_dir, project_id):
        print(json.dumps({"ok": False, "error": "project_id already exists"}, indent=2))
        return 2

    bindings = load_workspace_bindings(manager_dir)
    experiment_rows = bindings.get("experiments", [])
    assert isinstance(experiment_rows, list)
    transferred = [
        str(row["path"])
        for row in experiment_rows
        if isinstance(row, dict)
        and row.get("experiment_id") == experiment_id
        and isinstance(row.get("path"), str)
    ]
    result = {
        "ok": True,
        "dry_run": not args.apply,
        "experiment_id": experiment_id,
        "experiment_packet": str(experiment),
        "project_id": project_id,
        "project_packet": str(project),
        "workspace_paths": transferred,
        "transition": f"{current_status} -> promoted",
    }
    if not args.apply:
        print(json.dumps(result, indent=2))
        return 0

    stamp = now()
    project.mkdir(parents=True)
    project_readme = render_project_readme(
        args.project_name,
        args.summary,
        project_id,
        stamp,
        source_experiment=experiment_id,
    )
    project_readme = append_section(
        project_readme,
        "Origin",
        f"- Promoted from [{experiment_metadata.get('name', experiment.name)}](../../experiments/{experiment.name}/README.md).",
    )
    (project / "README.md").write_text(project_readme, encoding="utf-8")
    (project / "AGENTS.md").write_text(
        render_project_agents(args.project_name, project_id, stamp), encoding="utf-8"
    )

    experiment_content = update_frontmatter(
        experiment_readme.read_text(encoding="utf-8"),
        {
            "status": "promoted",
            "promoted_to_project_id": project_id,
            "updated_at": iso_date(stamp),
            "last_edited": iso_date(stamp),
        },
    )
    experiment_content = append_section(
        experiment_content,
        "Promotion",
        f"- Promoted to [{args.project_name}](../../projects/{slug}/README.md).",
    )
    experiment_readme.write_text(experiment_content, encoding="utf-8")

    bindings["experiments"] = [
        row
        for row in experiment_rows
        if not isinstance(row, dict) or row.get("experiment_id") != experiment_id
    ]
    project_rows = bindings.setdefault("projects", [])
    assert isinstance(project_rows, list)
    project_rows.extend({"project_id": project_id, "path": path} for path in transferred)
    bindings["schema_version"] = BINDINGS_SCHEMA
    bindings["updated_at"] = iso_timestamp(stamp)
    write_json(manager_dir / ".wirenet/workspace-bindings.json", bindings)
    (manager_dir / "projects/index.md").write_text(
        render_projects_index(manager_dir), encoding="utf-8"
    )
    (manager_dir / "experiments/index.md").write_text(
        render_experiments_index(manager_dir), encoding="utf-8"
    )
    manager_metadata_path = manager_dir / ".wirenet/manager.json"
    manager_metadata = load_json(manager_metadata_path)
    manager_metadata["updated_at"] = iso_timestamp(stamp)
    write_json(manager_metadata_path, manager_metadata)

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
