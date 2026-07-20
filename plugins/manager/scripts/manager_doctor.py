#!/usr/bin/env python3
"""Inspect a wirenet Manager v0.2 without modifying it."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from manager_model import (
    BINDINGS_SCHEMA,
    EXPERIMENT_PACK_SCHEMA,
    EXPERIMENT_STATUSES,
    MANAGER_SCHEMA,
    PROJECT_PACK_SCHEMA,
    PROJECT_STATUSES,
    RUNTIME_SCHEMA,
    experiment_id_from_readme,
    frontmatter,
    load_json,
    manager_schema_version,
    project_id_from_readme,
)
from manager_update import check_for_update
from okf_projection import iter_markdown, parse_frontmatter


REQUIRED_FILES = (
    ".gitignore",
    "AGENTS.md",
    "index.md",
    "README.md",
    "TODO.md",
    "agent/USER_CONTEXT.md",
    "projects/index.md",
    "projects/AGENTS.md",
    ".wirenet/manager.json",
    ".wirenet/workspace-bindings.json",
)
REQUIRED_DIRECTORIES = (
    ".wirenet",
    "agent",
    "archive",
    "docs",
    "experiments",
    "notes",
    "outputs",
    "people",
    "projects",
    "sources",
)
FORBIDDEN_PATHS = ("templates", ".wirenet/project-bindings.json")
REQUIRED_PACK_FILES = ("README.md", "AGENTS.md")
RESERVED_OKF_FILES = {"index.md", "log.md"}


def manager_version_state(workspace_schema: str) -> str:
    if workspace_schema == MANAGER_SCHEMA:
        return "current"
    workspace = manager_schema_version(workspace_schema)
    supported = manager_schema_version(MANAGER_SCHEMA)
    if workspace is None or supported is None:
        return "unsupported"
    return "plugin-too-old" if workspace > supported else "upgrade-required"


def validate_update_log(path: Path) -> list[str]:
    content = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if not content.startswith("# "):
        errors.append("log.md must start with a level-one title")
    dates = re.findall(r"(?m)^## (\d{4}-\d{2}-\d{2})$", content)
    if not dates:
        errors.append("log.md must contain at least one ISO-date heading")
    elif dates != sorted(dates, reverse=True):
        errors.append("log.md date headings must be newest first")
    return errors


def validate_runtime(path: Path, identity_key: str, identity: str | None) -> list[str]:
    metadata = frontmatter(path)
    errors: list[str] = []
    if metadata.get("schema") != RUNTIME_SCHEMA:
        errors.append(f"{path.name} is not on the v0.1 runtime schema")
    if metadata.get("type"):
        errors.append(f"{path.name} must remain outside the OKF concept projection")
    if identity and metadata.get(identity_key) != identity:
        errors.append(f"{path.name} must share the packet's {identity_key}")
    return errors


def inspect_packets(
    manager_dir: Path,
    *,
    collection: str,
    identity_key: str,
    identity_reader,
    schema: str,
    statuses: tuple[str, ...],
    index_path: Path,
) -> tuple[list[dict[str, object]], set[str], list[str]]:
    reports: list[dict[str, object]] = []
    identities: set[str] = set()
    errors: list[str] = []
    root = manager_dir / collection
    if not root.is_dir():
        return reports, identities, errors
    index = index_path.read_text(encoding="utf-8") if index_path.is_file() else ""
    for packet in sorted(path for path in root.iterdir() if path.is_dir()):
        missing = [
            name for name in REQUIRED_PACK_FILES if not (packet / name).is_file()
        ]
        identity = identity_reader(packet / "README.md")
        packet_errors: list[str] = []
        if not identity:
            packet_errors.append(f"README.md is missing {identity_key}")
        elif identity in identities:
            packet_errors.append(f"duplicate {identity_key}: {identity}")
        else:
            identities.add(identity)

        concept_files = sorted(
            path
            for path in packet.glob("*.md")
            if path.name not in RESERVED_OKF_FILES | {"AGENTS.md"}
        )
        portable_files = concept_files + [packet / "AGENTS.md"]
        file_identities = {
            path.name: frontmatter(path).get(identity_key)
            for path in portable_files
            if path.is_file()
        }
        if identity and any(value != identity for value in file_identities.values()):
            packet_errors.append(
                f"all {collection} packet files must share one {identity_key}"
            )
        for path in concept_files:
            metadata = frontmatter(path)
            if metadata.get("schema") != schema:
                packet_errors.append(
                    f"{path.name} is not on the expected packet schema"
                )
            if not metadata.get("type"):
                packet_errors.append(f"{path.name} is missing a non-empty OKF type")
            if path.name == "WORKLOG.md":
                if collection != "projects":
                    packet_errors.append("WORKLOG.md is allowed only in Project Packs")
                if metadata.get("type") != "Goal Worklog":
                    packet_errors.append("WORKLOG.md must use OKF type Goal Worklog")
                if metadata.get("producer") != "ultragoal":
                    packet_errors.append("WORKLOG.md must declare producer ultragoal")
        agents = packet / "AGENTS.md"
        if agents.is_file():
            packet_errors.extend(validate_runtime(agents, identity_key, identity))
        readme_metadata = frontmatter(packet / "README.md")
        status = readme_metadata.get("status", "")
        if status not in statuses:
            packet_errors.append(
                f"README.md has unsupported status: {status or '<missing>'}"
            )
        if not readme_metadata.get("name"):
            packet_errors.append("README.md is missing name")
        if "summary" not in readme_metadata:
            packet_errors.append("README.md is missing summary")
        if not index:
            packet_errors.append(f"{collection}/index.md is missing")
        elif f"({packet.name}/README.md)" not in index:
            packet_errors.append(f"packet is missing from {collection}/index.md")
        reports.append(
            {
                "path": str(packet),
                identity_key: identity,
                "status": status,
                "missing": missing,
                "errors": packet_errors,
            }
        )
        errors.extend(f"{collection}/{packet.name}: {item}" for item in packet_errors)
        errors.extend(f"{collection}/{packet.name}: missing {item}" for item in missing)
    return reports, identities, errors


def inspect(manager_dir: Path) -> dict[str, object]:
    missing = [item for item in REQUIRED_FILES if not (manager_dir / item).is_file()]
    missing.extend(
        f"{item}/" for item in REQUIRED_DIRECTORIES if not (manager_dir / item).is_dir()
    )
    errors: list[str] = []
    manager_meta: dict[str, object] = {}
    bindings: dict[str, object] = {}
    version_state = "unknown"
    workspace_schema = ""

    for relative in FORBIDDEN_PATHS:
        if (manager_dir / relative).exists():
            errors.append(f"{relative} is not part of the canonical v0.2 workspace")

    for path in iter_markdown(manager_dir):
        relative = path.relative_to(manager_dir).as_posix()
        content = path.read_text(encoding="utf-8")
        metadata, _ = parse_frontmatter(content)
        name = path.name.lower()
        if path.name == "WORKLOG.md":
            parts = Path(relative).parts
            if len(parts) != 3 or parts[0] != "projects":
                errors.append(
                    f"{relative} is reserved for UltraGoal state in a Project Pack"
                )
        if name == "agents.md":
            if metadata.get("schema") != RUNTIME_SCHEMA:
                errors.append(f"{relative} is not on the v0.1 runtime schema")
            if str(metadata.get("type") or "").strip():
                errors.append(
                    f"{relative} must remain outside the OKF concept projection"
                )
            continue
        if name in RESERVED_OKF_FILES:
            if str(metadata.get("type") or "").strip():
                errors.append(
                    f"{relative} is reserved and must not declare an OKF type"
                )
            if name == "index.md":
                if set(metadata) - {"okf_version"}:
                    errors.append(
                        f"{relative} index frontmatter may contain only okf_version"
                    )
                if not re.search(r"(?m)^#\s+\S", content):
                    errors.append(f"{relative} must contain a section heading")
            else:
                if content.startswith("---\n"):
                    errors.append(
                        f"{relative} is reserved history and must not use frontmatter"
                    )
                errors.extend(
                    f"{relative}: {item}" for item in validate_update_log(path)
                )
            continue
        if not str(metadata.get("type") or "").strip():
            errors.append(f"{relative} is missing a non-empty OKF type")

    root_readme = manager_dir / "README.md"
    if root_readme.is_file():
        root_metadata = frontmatter(root_readme)
        if root_metadata.get("type") != "Manager Overview":
            errors.append("README.md must use OKF type Manager Overview")
        if root_metadata.get("schema") != MANAGER_SCHEMA:
            errors.append("README.md is not on the v0.2 Manager schema")

    root_index = manager_dir / "index.md"
    if root_index.is_file():
        root_index_metadata, _ = parse_frontmatter(
            root_index.read_text(encoding="utf-8")
        )
        if root_index_metadata.get("okf_version") != "0.1":
            errors.append("index.md must declare okf_version 0.1")

    metadata_path = manager_dir / ".wirenet/manager.json"
    if metadata_path.is_file():
        try:
            manager_meta = load_json(metadata_path)
            workspace_schema = str(manager_meta.get("schema_version") or "")
            version_state = manager_version_state(workspace_schema)
            if version_state == "upgrade-required":
                errors.append(
                    f"manager.json requires upgrade from {workspace_schema} to {MANAGER_SCHEMA}"
                )
            elif version_state == "plugin-too-old":
                errors.append(
                    f"Manager requires {workspace_schema}; update the plugin beyond {MANAGER_SCHEMA}"
                )
            elif version_state == "unsupported":
                errors.append("manager.json has an unsupported schema_version")
            if not manager_meta.get("manager_id"):
                errors.append("manager.json is missing manager_id")
            if manager_meta.get("project_pack_profile") != PROJECT_PACK_SCHEMA:
                errors.append("manager.json has an unsupported Project Pack profile")
            if manager_meta.get("experiment_pack_profile") != EXPERIMENT_PACK_SCHEMA:
                errors.append("manager.json has an unsupported Experiment Pack profile")
        except ValueError as error:
            errors.append(str(error))

    bindings_path = manager_dir / ".wirenet/workspace-bindings.json"
    if bindings_path.is_file():
        try:
            bindings = load_json(bindings_path)
            if bindings.get("schema_version") != BINDINGS_SCHEMA:
                errors.append(
                    "workspace-bindings.json has an unsupported schema_version"
                )
            for name in ("projects", "experiments", "ignored"):
                rows = bindings.get(name, [])
                if not isinstance(rows, list):
                    errors.append(f"workspace-bindings.json {name} must be a list")
                    continue
                identity_key = {
                    "projects": "project_id",
                    "experiments": "experiment_id",
                    "ignored": None,
                }[name]
                for position, row in enumerate(rows):
                    label = f"workspace-bindings.json {name}[{position}]"
                    if not isinstance(row, dict):
                        errors.append(f"{label} must be an object")
                        continue
                    path_value = row.get("path")
                    if not isinstance(path_value, str) or not path_value:
                        errors.append(f"{label} must contain a non-empty path")
                    elif not Path(path_value).is_absolute():
                        errors.append(f"{label} path must be absolute")
                    if identity_key:
                        identity = row.get(identity_key)
                        if not isinstance(identity, str) or not identity:
                            errors.append(
                                f"{label} must contain a non-empty {identity_key}"
                            )
        except ValueError as error:
            errors.append(str(error))

    projects_index = manager_dir / "projects/index.md"
    if projects_index.is_file():
        content = projects_index.read_text(encoding="utf-8")
        for heading in (
            "## Active Project Packs",
            "## Waiting And Blocked",
            "## Completed Project Packs",
            "## Archived Project Packs",
        ):
            if heading not in content:
                errors.append(f"projects/index.md is missing {heading}")

    project_reports, project_ids, project_errors = inspect_packets(
        manager_dir,
        collection="projects",
        identity_key="project_id",
        identity_reader=project_id_from_readme,
        schema=PROJECT_PACK_SCHEMA,
        statuses=PROJECT_STATUSES,
        index_path=projects_index,
    )
    errors.extend(project_errors)

    experiments_dir = manager_dir / "experiments"
    experiment_packets = (
        [path for path in experiments_dir.iterdir() if path.is_dir()]
        if experiments_dir.is_dir()
        else []
    )
    experiments_index = experiments_dir / "index.md"
    if experiment_packets and not experiments_index.is_file():
        errors.append("experiments/index.md is required once Experiment Packs exist")
    if experiments_index.is_file():
        content = experiments_index.read_text(encoding="utf-8")
        for heading in (
            "## Active Experiments",
            "## Concluded Experiments",
            "## Promoted Experiments",
            "## Archived Experiments",
        ):
            if heading not in content:
                errors.append(f"experiments/index.md is missing {heading}")
    experiment_reports, experiment_ids, experiment_errors = inspect_packets(
        manager_dir,
        collection="experiments",
        identity_key="experiment_id",
        identity_reader=experiment_id_from_readme,
        schema=EXPERIMENT_PACK_SCHEMA,
        statuses=EXPERIMENT_STATUSES,
        index_path=experiments_index,
    )
    errors.extend(experiment_errors)

    binding_project_ids = {
        row.get("project_id")
        for row in bindings.get("projects", [])
        if isinstance(row, dict) and row.get("project_id")
    }
    binding_experiment_ids = {
        row.get("experiment_id")
        for row in bindings.get("experiments", [])
        if isinstance(row, dict) and row.get("experiment_id")
    }
    unknown_projects = sorted(str(item) for item in binding_project_ids - project_ids)
    unknown_experiments = sorted(
        str(item) for item in binding_experiment_ids - experiment_ids
    )
    if unknown_projects:
        errors.append(f"bindings reference unknown project ids: {unknown_projects}")
    if unknown_experiments:
        errors.append(
            f"bindings reference unknown experiment ids: {unknown_experiments}"
        )
    paths: list[str] = []
    for name in ("projects", "experiments", "ignored"):
        paths.extend(
            str(row.get("path"))
            for row in bindings.get(name, [])
            if isinstance(row, dict) and isinstance(row.get("path"), str)
        )
    duplicates = sorted({path for path in paths if paths.count(path) > 1})
    if duplicates:
        errors.append(f"workspace paths have multiple classifications: {duplicates}")

    return {
        "ok": not missing and not errors,
        "manager_dir": str(manager_dir),
        "exists": manager_dir.is_dir(),
        "missing": missing,
        "errors": errors,
        "manager_id": manager_meta.get("manager_id"),
        "workspace_schema": workspace_schema or None,
        "supported_schema": MANAGER_SCHEMA,
        "version_state": version_state,
        "project_packs": project_reports,
        "experiment_packs": experiment_reports,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manager-dir", default="~/Manager")
    parser.add_argument(
        "--check-updates",
        action="store_true",
        help="read the latest public GitHub release without changing local state",
    )
    parser.add_argument(
        "--release-json",
        type=Path,
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()
    result = inspect(Path(args.manager_dir).expanduser().resolve(strict=False))
    if args.check_updates:
        result["update"] = check_for_update(release_json=args.release_json)
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
