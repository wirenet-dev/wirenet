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
    RUNTIME_SCHEMA,
    load_json,
    project_id_from_readme,
)
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
    ".wirenet/project-bindings.json",
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
FORBIDDEN_PATHS = ("templates",)
REQUIRED_PACK_FILES = ("README.md", "AGENTS.md")
RESERVED_OKF_FILES = {"index.md", "log.md"}


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
    missing = [item for item in REQUIRED_FILES if not (manager_dir / item).is_file()]
    missing.extend(
        f"{item}/" for item in REQUIRED_DIRECTORIES if not (manager_dir / item).is_dir()
    )
    errors: list[str] = []
    manager_meta: dict[str, object] = {}
    bindings: dict[str, object] = {}

    for relative in FORBIDDEN_PATHS:
        if (manager_dir / relative).exists():
            errors.append(f"{relative}/ is not part of the canonical v0.1 workspace")

    for path in iter_markdown(manager_dir):
        relative = path.relative_to(manager_dir).as_posix()
        content = path.read_text(encoding="utf-8")
        metadata, _ = parse_frontmatter(content)
        name = path.name.lower()
        if name == "agents.md":
            if metadata.get("schema") != RUNTIME_SCHEMA:
                errors.append(f"{relative} is not on the v0.1 runtime schema")
            if str(metadata.get("type") or "").strip():
                errors.append(f"{relative} must remain outside the OKF concept projection")
            continue
        if name in RESERVED_OKF_FILES:
            if str(metadata.get("type") or "").strip():
                errors.append(f"{relative} is reserved and must not declare an OKF type")
            if name == "index.md":
                if set(metadata) - {"okf_version"}:
                    errors.append(f"{relative} index frontmatter may contain only okf_version")
                if not re.search(r"(?m)^#\s+\S", content):
                    errors.append(f"{relative} must contain a section heading")
            else:
                if content.startswith("---\n"):
                    errors.append(f"{relative} is reserved history and must not use frontmatter")
                errors.extend(f"{relative}: {item}" for item in validate_update_log(path))
            continue
        if not str(metadata.get("type") or "").strip():
            errors.append(f"{relative} is missing a non-empty OKF type")

    root_readme = manager_dir / "README.md"
    if root_readme.is_file():
        root_metadata, _ = parse_frontmatter(root_readme.read_text(encoding="utf-8"))
        if root_metadata.get("type") != "Manager Overview":
            errors.append("README.md must use OKF type Manager Overview")
        if root_metadata.get("schema") != MANAGER_SCHEMA:
            errors.append("README.md is not on the v0.1 Manager schema")

    root_index = manager_dir / "index.md"
    if root_index.is_file():
        root_index_metadata, _ = parse_frontmatter(root_index.read_text(encoding="utf-8"))
        if root_index_metadata.get("okf_version") != "0.1":
            errors.append("index.md must declare okf_version 0.1")

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
            packet_missing = [name for name in REQUIRED_PACK_FILES if not (packet / name).is_file()]
            project_id = project_id_from_readme(packet / "README.md")
            packet_errors: list[str] = []
            if not project_id:
                packet_errors.append("README.md is missing project_id")
            elif project_id in project_ids:
                packet_errors.append(f"duplicate project_id: {project_id}")
            else:
                project_ids.add(project_id)
            concept_files = sorted(
                path
                for path in packet.glob("*.md")
                if path.name not in RESERVED_OKF_FILES | {"AGENTS.md"}
            )
            portable_files = concept_files + [packet / "AGENTS.md"]
            file_project_ids = {
                path.name: project_id_from_readme(path)
                for path in portable_files
                if path.is_file()
            }
            if project_id and any(value != project_id for value in file_project_ids.values()):
                packet_errors.append("all Project Pack concept files must share one project_id")
            for path in concept_files:
                content = path.read_text(encoding="utf-8")
                if f'schema: "{PROJECT_PACK_SCHEMA}"' not in content:
                    packet_errors.append(f"{path.name} is not on the v0.1 Project Pack schema")
                if not re.search(r"(?m)^type:\s*[\"']?\S", content):
                    packet_errors.append(f"{path.name} is missing a non-empty OKF type")
            agents_path = packet / "AGENTS.md"
            if agents_path.is_file():
                agents_content = agents_path.read_text(encoding="utf-8")
                if f'schema: "{RUNTIME_SCHEMA}"' not in agents_content:
                    packet_errors.append("AGENTS.md is not on the v0.1 runtime schema")
                if re.search(r"(?m)^type:\s*[\"']?\S", agents_content):
                    packet_errors.append("AGENTS.md must remain outside the OKF concept projection")
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
