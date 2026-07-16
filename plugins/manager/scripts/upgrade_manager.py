#!/usr/bin/env python3
"""Preview or apply a supported wirenet Manager workspace migration."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from manager_doctor import inspect
from manager_model import (
    BINDINGS_SCHEMA,
    EXPERIMENT_OKF_PROFILE,
    EXPERIMENT_PACK_SCHEMA,
    MANAGER_SCHEMA,
    PLUGIN_VERSION,
    PROJECT_OKF_PROFILE,
    PROJECT_PACK_SCHEMA,
    frontmatter,
    iso_timestamp,
    load_json,
    manager_schema_version,
    update_frontmatter,
    write_json,
)


LEGACY_MANAGER_SCHEMA = "wirenet-manager/v0.1"
LEGACY_BINDINGS_SCHEMA = "wirenet-project-bindings/v0.1"
ROOT_CONCEPTS = ("README.md", "TODO.md", "agent/USER_CONTEXT.md")
PROJECT_INDEX_HEADINGS = (
    "## Active Project Packs",
    "## Waiting And Blocked",
    "## Completed Project Packs",
    "## Archived Project Packs",
)
RUNTIME_CLAUSE_UPDATES = (
    (
        "3. `projects/index.md` for active workstreams.\n"
        "4. The relevant Project Pack's `README.md` and `AGENTS.md`.",
        "3. `projects/index.md` for project lifecycle and `experiments/index.md` when it\n"
        "   exists and a bounded spike is relevant.\n"
        "4. The relevant Project or Experiment Pack's `README.md` and `AGENTS.md`.",
    ),
    (
        "- Detailed UltraGoal attempts belong in optional `WORKLOG.md`.",
        "- Only an explicitly invoked UltraGoal may create or update `WORKLOG.md` for\n"
        "  detailed attempts and recovery state.",
    ),
    (
        "- Curated retained evidence belongs in `sources/`; short-lived spikes belong in\n"
        "  `experiments/`; inactive durable context belongs in `archive/`.\n"
        "- Generated intermediates may use ignored `outputs/`, but canonical meaning\n"
        "  must be promoted into a typed knowledge document.",
        "- Curated retained evidence belongs in `sources/`; short-lived spikes belong in\n"
        "  `experiments/`; each real experiment starts with `README.md` and `AGENTS.md`,\n"
        "  remains bounded, and ends by conclusion, promotion, or archive. Inactive\n"
        "  durable context belongs in `archive/`.\n"
        "- A few transient review files may stay together under\n"
        "  `outputs/<task-slug>/`. When files begin to need recurring editing, durable\n"
        "  delivery, or their own toolchain, suggest an external workspace and Project\n"
        "  Pack without interrupting useful work merely to reorganize it. Promote\n"
        "  canonical meaning into a typed knowledge document.\n"
        "- Do not write new working state into archived packets without explicit\n"
        "  reactivation. Treat waiting and blocked as live states, and preserve promoted\n"
        "  experiments as origin evidence.",
    ),
    (
        "- Update `projects/index.md` when creating or archiving a packet.",
        "- Update `projects/index.md` after every packet creation or lifecycle transition.",
    ),
    (
        "- Let an active UltraGoal use `WORKLOG.md` for detailed attempts; do not mirror that detail into `log.md`.\n"
        "- Create or update `log.md` only when a sparse OKF chronology materially improves navigation or synchronization.",
        "- Only an explicitly invoked UltraGoal may create or update `WORKLOG.md`.\n"
        "- Create or update `log.md` only when sparse chronology materially improves navigation or synchronization.\n"
        "- Never mirror detailed UltraGoal WORKLOG entries into `log.md`.",
    ),
    (
        "5. Revisit the canonical external sources listed below selectively.",
        "5. Revisit canonical external sources selectively when a workspace is bound.",
    ),
)


def resolve_executable(explicit: str | None, name: str) -> str | None:
    if explicit:
        candidate = Path(explicit).expanduser().resolve(strict=False)
        return str(candidate) if candidate.is_file() and os.access(candidate, os.X_OK) else None
    return shutil.which(name)


def git_worktree_status(manager_dir: Path, git_bin: str | None) -> tuple[bool, str]:
    if not (manager_dir / ".git").is_dir():
        return (
            False,
            "Manager migration requires the local Git repository created by bootstrap",
        )
    if not git_bin:
        return False, "Git is unavailable; load the Codex runtime or provide --git-bin"
    result = subprocess.run(
        [git_bin, "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=manager_dir,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return False, result.stderr.strip() or "cannot inspect Manager Git state"
    if result.stdout.strip():
        return (
            False,
            "Manager has uncommitted changes; create a local checkpoint before migrating",
        )
    return True, "clean"


def _schema_state(workspace_schema: str) -> str:
    current = manager_schema_version(MANAGER_SCHEMA)
    workspace = manager_schema_version(workspace_schema)
    if workspace_schema == MANAGER_SCHEMA:
        return "current"
    if current is None or workspace is None:
        return "unsupported"
    return "plugin-too-old" if workspace > current else "upgrade-available"


def plan_upgrade(
    manager_dir: Path, *, git_bin: str | None = None
) -> dict[str, object]:
    result: dict[str, object] = {
        "ok": True,
        "dry_run": True,
        "manager_dir": str(manager_dir),
        "supported_schema": MANAGER_SCHEMA,
        "plugin_version": PLUGIN_VERSION,
        "actions": [],
    }
    metadata_path = manager_dir / ".wirenet/manager.json"
    if not manager_dir.is_dir() or not metadata_path.is_file():
        result.update(
            {
                "ok": False,
                "state": "invalid-manager",
                "error": "Manager metadata is missing; bootstrap or repair the workspace first",
            }
        )
        return result
    try:
        metadata = load_json(metadata_path)
    except ValueError as error:
        result.update({"ok": False, "state": "invalid-manager", "error": str(error)})
        return result

    workspace_schema = str(metadata.get("schema_version") or "")
    state = _schema_state(workspace_schema)
    result.update({"state": state, "workspace_schema": workspace_schema})
    if state == "current":
        result["actions"] = []
        return result
    if state == "plugin-too-old":
        result.update(
            {
                "ok": False,
                "error": "Manager schema is newer than this plugin; update wirenet Manager",
            }
        )
        return result
    if state == "unsupported" or workspace_schema != LEGACY_MANAGER_SCHEMA:
        result.update(
            {
                "ok": False,
                "state": "unsupported",
                "error": f"no migration path from {workspace_schema or '<missing>'} to {MANAGER_SCHEMA}",
            }
        )
        return result

    required_paths = (
        "README.md",
        "AGENTS.md",
        "TODO.md",
        "agent/USER_CONTEXT.md",
        "projects/index.md",
        "projects/AGENTS.md",
    )
    missing_paths = [
        relative
        for relative in required_paths
        if not (manager_dir / relative).is_file()
    ]
    if not (manager_dir / "experiments").is_dir():
        missing_paths.append("experiments/")
    if missing_paths:
        result.update(
            {
                "ok": False,
                "state": "recovery-required",
                "error": "legacy Manager is missing required migration inputs",
                "missing": missing_paths,
            }
        )
        return result

    legacy_path = manager_dir / ".wirenet/project-bindings.json"
    current_path = manager_dir / ".wirenet/workspace-bindings.json"
    backup_path = (
        manager_dir / ".wirenet/migrations/wirenet-manager-v0.1/project-bindings.json"
    )
    if not legacy_path.is_file():
        result.update(
            {
                "ok": False,
                "state": "recovery-required",
                "error": "legacy project-bindings.json is missing",
            }
        )
        return result
    if current_path.exists() or backup_path.exists():
        result.update(
            {
                "ok": False,
                "state": "recovery-required",
                "error": "new bindings or a prior migration backup already exists; inspect the partial migration",
            }
        )
        return result
    try:
        legacy = load_json(legacy_path)
    except ValueError as error:
        result.update({"ok": False, "state": "invalid-manager", "error": str(error)})
        return result
    if legacy.get("schema_version") != LEGACY_BINDINGS_SCHEMA:
        result.update(
            {
                "ok": False,
                "state": "unsupported",
                "error": "legacy binding registry has an unsupported schema",
            }
        )
        return result
    bindings = legacy.get("bindings", [])
    routes = legacy.get("routes", [])
    if not isinstance(bindings, list) or not isinstance(routes, list):
        result.update(
            {
                "ok": False,
                "state": "invalid-manager",
                "error": "legacy bindings and routes must be lists",
            }
        )
        return result
    experiment_routes = [
        row
        for row in routes
        if isinstance(row, dict) and row.get("classification") == "experiment"
    ]
    if experiment_routes:
        result.update(
            {
                "ok": False,
                "state": "manual-review",
                "error": "legacy experiment routes need a question and decision criterion before migration",
                "manual_paths": [str(row.get("path")) for row in experiment_routes],
            }
        )
        return result

    legacy_experiment_directories = sorted(
        str(path) for path in (manager_dir / "experiments").iterdir() if path.is_dir()
    )
    if legacy_experiment_directories:
        result.update(
            {
                "ok": False,
                "state": "manual-review",
                "error": "legacy experiment directories need a question and decision criterion before migration",
                "manual_paths": legacy_experiment_directories,
            }
        )
        return result

    project_directories = sorted(
        path for path in (manager_dir / "projects").iterdir() if path.is_dir()
    )
    invalid_packets = [
        str(path)
        for path in project_directories
        if not (path / "AGENTS.md").is_file()
        or not frontmatter(path / "README.md").get("project_id")
    ]
    if invalid_packets:
        result.update(
            {
                "ok": False,
                "state": "manual-review",
                "error": "legacy Project Packs need valid project IDs before migration",
                "manual_paths": invalid_packets,
            }
        )
        return result

    project_ids = {
        frontmatter(path / "README.md").get("project_id")
        for path in project_directories
    }
    malformed_rows: list[str] = []
    routed_paths: list[str] = []
    for position, row in enumerate(bindings):
        if not isinstance(row, dict):
            malformed_rows.append(f"bindings[{position}]")
            continue
        project_id = row.get("project_id")
        path_value = row.get("path")
        if (
            not isinstance(project_id, str)
            or project_id not in project_ids
            or not isinstance(path_value, str)
            or not Path(path_value).is_absolute()
        ):
            malformed_rows.append(f"bindings[{position}]")
        elif path_value in routed_paths:
            malformed_rows.append(f"bindings[{position}] duplicate path")
        else:
            routed_paths.append(path_value)
    for position, row in enumerate(routes):
        if not isinstance(row, dict):
            malformed_rows.append(f"routes[{position}]")
            continue
        path_value = row.get("path")
        if (
            row.get("classification") not in {"ignored", "experiment"}
            or not isinstance(path_value, str)
            or not Path(path_value).is_absolute()
        ):
            malformed_rows.append(f"routes[{position}]")
        elif path_value in routed_paths:
            malformed_rows.append(f"routes[{position}] duplicate path")
        else:
            routed_paths.append(path_value)
    if malformed_rows:
        result.update(
            {
                "ok": False,
                "state": "manual-review",
                "error": "legacy workspace routes need repair before migration",
                "manual_paths": malformed_rows,
            }
        )
        return result

    clean, git_detail = git_worktree_status(
        manager_dir, git_bin or resolve_executable(None, "git")
    )
    result.update(
        {
            "git_clean": clean,
            "git_detail": git_detail,
            "actions": [
                "preserve personal Markdown bodies and runtime instructions",
                "update known Manager concept schemas to wirenet-manager/v0.2",
                "complete legacy Project Status metadata from its existing heading and purpose",
                "update known generated runtime clauses without replacing user additions",
                "add missing project lifecycle index sections",
                "convert project and ignored routes into workspace-bindings.json",
                "retain the legacy registry under .wirenet/migrations/",
                "update Manager metadata and validate with Manager Doctor",
            ],
        }
    )
    return result


def _replace_manager_schema(content: str) -> str:
    return re.sub(
        rf'(?m)^schema:\s*["\']?{re.escape(LEGACY_MANAGER_SCHEMA)}["\']?\s*$',
        f'schema: "{MANAGER_SCHEMA}"',
        content,
        count=1,
    )


def _upgrade_project_index(content: str) -> str:
    updated = content.rstrip()
    for heading in PROJECT_INDEX_HEADINGS:
        if heading not in updated:
            updated += f"\n\n{heading}"
    return updated + "\n"


def _project_name_and_summary(content: str, path: Path) -> tuple[str, str]:
    heading = re.search(r"(?m)^#\s+(.+?)\s*$", content)
    name = (
        heading.group(1).strip()
        if heading
        else path.parent.name.replace("-", " ").title()
    )
    purpose = re.search(
        r"(?ms)^## Purpose\s*\n+(.*?)(?=^##\s|\Z)",
        content,
    )
    summary = ""
    if purpose:
        paragraphs = [
            line.strip() for line in purpose.group(1).splitlines() if line.strip()
        ]
        summary = " ".join(paragraphs)
    return name, summary or f"Current status and next move for {name}."


def _upgrade_project_readme(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    metadata = frontmatter(path)
    updates: dict[str, str] = {}
    name, summary = _project_name_and_summary(content, path)
    if not metadata.get("name"):
        updates["name"] = name
    if "summary" not in metadata:
        updates["summary"] = summary
    if not updates:
        return False
    path.write_text(update_frontmatter(content, updates), encoding="utf-8")
    return True


def _upgrade_known_runtime_clauses(path: Path) -> bool:
    if not path.is_file():
        return False
    content = path.read_text(encoding="utf-8")
    updated = content
    for old, new in RUNTIME_CLAUSE_UPDATES:
        updated = updated.replace(old, new)
    if updated == content:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def apply_v01_to_v02(manager_dir: Path) -> list[str]:
    metadata_path = manager_dir / ".wirenet/manager.json"
    legacy_path = manager_dir / ".wirenet/project-bindings.json"
    current_path = manager_dir / ".wirenet/workspace-bindings.json"
    backup_path = (
        manager_dir / ".wirenet/migrations/wirenet-manager-v0.1/project-bindings.json"
    )
    metadata = load_json(metadata_path)
    legacy = load_json(legacy_path)
    bindings = legacy.get("bindings", [])
    routes = legacy.get("routes", [])
    assert isinstance(bindings, list)
    assert isinstance(routes, list)
    workspace_bindings = {
        "schema_version": BINDINGS_SCHEMA,
        "updated_at": iso_timestamp(),
        "projects": [dict(row) for row in bindings if isinstance(row, dict)],
        "experiments": [],
        "ignored": [
            {"path": str(row.get("path"))}
            for row in routes
            if isinstance(row, dict)
            and row.get("classification") == "ignored"
            and isinstance(row.get("path"), str)
        ],
    }

    changed: list[str] = []
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    legacy_path.replace(backup_path)
    changed.extend(
        [
            ".wirenet/project-bindings.json",
            ".wirenet/migrations/wirenet-manager-v0.1/project-bindings.json",
        ]
    )
    write_json(current_path, workspace_bindings)
    changed.append(".wirenet/workspace-bindings.json")

    for relative in ROOT_CONCEPTS:
        path = manager_dir / relative
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        updated = _replace_manager_schema(content)
        if updated != content:
            path.write_text(updated, encoding="utf-8")
            changed.append(relative)

    runtime_paths = [manager_dir / "AGENTS.md", manager_dir / "projects/AGENTS.md"]
    runtime_paths.extend(sorted((manager_dir / "projects").glob("*/AGENTS.md")))
    for path in runtime_paths:
        if _upgrade_known_runtime_clauses(path):
            changed.append(path.relative_to(manager_dir).as_posix())

    for readme in sorted((manager_dir / "projects").glob("*/README.md")):
        if _upgrade_project_readme(readme):
            changed.append(readme.relative_to(manager_dir).as_posix())

    projects_index = manager_dir / "projects/index.md"
    content = projects_index.read_text(encoding="utf-8")
    updated_index = _upgrade_project_index(content)
    if updated_index != content:
        projects_index.write_text(updated_index, encoding="utf-8")
        changed.append("projects/index.md")
    (manager_dir / "experiments").mkdir(parents=True, exist_ok=True)

    metadata.update(
        {
            "schema_version": MANAGER_SCHEMA,
            "updated_at": iso_timestamp(),
            "plugin_version": PLUGIN_VERSION,
            "project_pack_profile": PROJECT_PACK_SCHEMA,
            "experiment_pack_profile": EXPERIMENT_PACK_SCHEMA,
            "okf_profiles": [PROJECT_OKF_PROFILE, EXPERIMENT_OKF_PROFILE],
        }
    )
    metadata.pop("okf_profile", None)
    write_json(metadata_path, metadata)
    changed.append(".wirenet/manager.json")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manager-dir", default="~/Manager")
    parser.add_argument(
        "--git-bin",
        default=os.environ.get("WIRENET_GIT_BIN"),
        help="Explicit Git executable, including a Codex-bundled fallback.",
    )
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    manager_dir = Path(args.manager_dir).expanduser().resolve(strict=False)
    git_bin = resolve_executable(args.git_bin, "git")
    result = plan_upgrade(manager_dir, git_bin=git_bin)
    result["runtime"] = {"python": sys.executable, "git": git_bin}
    result["dry_run"] = not args.apply
    if not result["ok"]:
        print(json.dumps(result, indent=2))
        return 2
    if result["state"] == "current" or not args.apply:
        print(json.dumps(result, indent=2))
        return 0
    if result.get("git_clean") is not True:
        result.update(
            {
                "ok": False,
                "state": "checkpoint-required",
                "error": result.get("git_detail"),
            }
        )
        print(json.dumps(result, indent=2))
        return 2

    try:
        changed = apply_v01_to_v02(manager_dir)
        diagnosis = inspect(manager_dir)
        if diagnosis["ok"] is not True:
            raise RuntimeError("Manager Doctor did not return ok=true after migration")
    except (OSError, RuntimeError, ValueError) as error:
        result.update(
            {
                "ok": False,
                "dry_run": False,
                "state": "migration-failed",
                "error": str(error),
                "recovery": "No cleanup was attempted; inspect the local Git diff and migration backup.",
            }
        )
        print(json.dumps(result, indent=2))
        return 1

    result.update(
        {
            "dry_run": False,
            "state": "upgraded",
            "workspace_schema": MANAGER_SCHEMA,
            "changed_paths": sorted(changed),
            "doctor": diagnosis,
            "next_action": "review and commit the local Manager migration",
        }
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
