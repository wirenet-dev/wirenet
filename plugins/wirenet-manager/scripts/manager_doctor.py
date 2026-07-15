#!/usr/bin/env python3
"""Inspect a WireNet Manager v0.1 without modifying it."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from manager_model import (
    BINDINGS_SCHEMA,
    MANAGER_SCHEMA,
    PROJECT_PACK_SCHEMA,
    load_json,
    project_id_from_readme,
)


REQUIRED_PATHS = (
    "AGENTS.md",
    "README.md",
    "TODO.md",
    "agent/USER_CONTEXT.md",
    "people/README.md",
    "projects/index.md",
    "projects/AGENTS.md",
    "notes/README.md",
    "sources/README.md",
    ".wirenet/manager.json",
    ".wirenet/project-bindings.json",
)
PACK_CONCEPT_FILES = ("README.md", "AGENTS.md", "GOAL.md", "RESULT.md")
PACK_FILES = (*PACK_CONCEPT_FILES, "log.md")


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


def inspect(manager_dir: Path) -> dict[str, object]:
    missing = [item for item in REQUIRED_PATHS if not (manager_dir / item).exists()]
    errors: list[str] = []
    manager_meta: dict[str, object] = {}
    bindings: dict[str, object] = {}

    if (manager_dir / ".wirenet/manager.json").is_file():
        try:
            manager_meta = load_json(manager_dir / ".wirenet/manager.json")
            if manager_meta.get("schema_version") != MANAGER_SCHEMA:
                errors.append("manager.json has an unsupported schema_version")
            if not manager_meta.get("manager_id"):
                errors.append("manager.json is missing manager_id")
        except ValueError as error:
            errors.append(str(error))

    if (manager_dir / ".wirenet/project-bindings.json").is_file():
        try:
            bindings = load_json(manager_dir / ".wirenet/project-bindings.json")
            if bindings.get("schema_version") != BINDINGS_SCHEMA:
                errors.append("project-bindings.json has an unsupported schema_version")
            if not isinstance(bindings.get("bindings", []), list):
                errors.append("project-bindings.json bindings must be a list")
            if not isinstance(bindings.get("routes", []), list):
                errors.append("project-bindings.json routes must be a list")
        except ValueError as error:
            errors.append(str(error))

    packet_reports: list[dict[str, object]] = []
    project_ids: set[str] = set()
    projects_dir = manager_dir / "projects"
    project_index = ""
    if (projects_dir / "index.md").is_file():
        project_index = (projects_dir / "index.md").read_text(encoding="utf-8")
        if project_index.startswith("---\n"):
            errors.append("projects/index.md must not contain Project Pack frontmatter")
        if "## Active Project Packs" not in project_index:
            errors.append("projects/index.md is missing the active-packets section")
    if projects_dir.is_dir():
        for packet in sorted(path for path in projects_dir.iterdir() if path.is_dir()):
            packet_missing = [name for name in PACK_FILES if not (packet / name).is_file()]
            project_id = project_id_from_readme(packet / "README.md")
            packet_errors: list[str] = []
            if not project_id:
                packet_errors.append("README.md is missing project_id")
            elif project_id in project_ids:
                packet_errors.append(f"duplicate project_id: {project_id}")
            else:
                project_ids.add(project_id)
            file_project_ids = {
                name: project_id_from_readme(packet / name)
                for name in PACK_CONCEPT_FILES
                if (packet / name).is_file()
            }
            if project_id and any(value != project_id for value in file_project_ids.values()):
                packet_errors.append("the four concept files do not share one project_id")
            for name in PACK_CONCEPT_FILES:
                path = packet / name
                if path.is_file() and f'schema: "{PROJECT_PACK_SCHEMA}"' not in path.read_text(
                    encoding="utf-8"
                ):
                    packet_errors.append(f"{name} is not on the v0.1 Project Pack schema")
            if (packet / "log.md").is_file():
                packet_errors.extend(validate_update_log(packet / "log.md"))
            if project_index and f"({packet.name}/README.md)" not in project_index:
                packet_errors.append("Project Pack is missing from projects/index.md")
            packet_reports.append(
                {
                    "path": str(packet),
                    "project_id": project_id,
                    "missing": packet_missing,
                    "errors": packet_errors,
                }
            )
            errors.extend(f"{packet.name}: {item}" for item in packet_errors)
            errors.extend(f"{packet.name}: missing {item}" for item in packet_missing)

    binding_project_ids = {
        item.get("project_id")
        for item in bindings.get("bindings", [])
        if isinstance(item, dict) and item.get("project_id")
    }
    unknown_bindings = sorted(str(item) for item in binding_project_ids - project_ids)
    if unknown_bindings:
        errors.append(f"bindings reference unknown project ids: {unknown_bindings}")

    return {
        "ok": not missing and not errors,
        "manager_dir": str(manager_dir),
        "exists": manager_dir.is_dir(),
        "missing": missing,
        "errors": errors,
        "manager_id": manager_meta.get("manager_id"),
        "project_packs": packet_reports,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manager-dir", default="~/Manager")
    args = parser.parse_args()
    result = inspect(Path(args.manager_dir).expanduser().resolve(strict=False))
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
