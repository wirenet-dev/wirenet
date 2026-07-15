#!/usr/bin/env python3
"""Shared data model and renderers for WireNet Manager v0.1."""

from __future__ import annotations

import json
import re
import uuid
from datetime import UTC, datetime
from pathlib import Path


MANAGER_SCHEMA = "wirenet-manager/v0.1"
PROJECT_PACK_SCHEMA = "wirenet-project-pack/v0.1"
BINDINGS_SCHEMA = "wirenet-project-bindings/v0.1"
OKF_PROFILE = "wirenet-okf-project-pack/v0.1"
PLUGIN_VERSION = "0.1.0"


def now() -> datetime:
    return datetime.now(UTC).replace(microsecond=0)


def iso_timestamp(value: datetime | None = None) -> str:
    return (value or now()).isoformat().replace("+00:00", "Z")


def iso_date(value: datetime | None = None) -> str:
    return (value or now()).date().isoformat()


def normalize_slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return re.sub(r"-+", "-", slug)


def new_manager_id() -> str:
    return f"mgr_{uuid.uuid4()}"


def new_project_id() -> str:
    return f"prj_{uuid.uuid4()}"


def manager_metadata(manager_id: str | None = None) -> dict[str, object]:
    stamp = iso_timestamp()
    return {
        "schema_version": MANAGER_SCHEMA,
        "manager_id": manager_id or new_manager_id(),
        "created_at": stamp,
        "updated_at": stamp,
        "plugin_version": PLUGIN_VERSION,
        "project_pack_profile": PROJECT_PACK_SCHEMA,
        "okf_profile": OKF_PROFILE,
    }


def empty_bindings() -> dict[str, object]:
    return {
        "schema_version": BINDINGS_SCHEMA,
        "updated_at": iso_timestamp(),
        "bindings": [],
        "routes": [],
    }


def load_json(path: Path) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read valid JSON from {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object in {path}")
    return value


def write_json(path: Path, value: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_bindings(manager_dir: Path) -> dict[str, object]:
    path = manager_dir / ".wirenet/project-bindings.json"
    if not path.exists():
        return empty_bindings()
    value = load_json(path)
    value.setdefault("bindings", [])
    value.setdefault("routes", [])
    return value


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def common_frontmatter(
    *,
    concept_type: str,
    title: str,
    project_id: str,
    status: str,
    stamp: datetime,
    visibility: str = "private",
) -> list[str]:
    return [
        "---",
        f"type: {yaml_string(concept_type)}",
        f"schema: {yaml_string(PROJECT_PACK_SCHEMA)}",
        f"okf_profile: {yaml_string(OKF_PROFILE)}",
        f"project_id: {yaml_string(project_id)}",
        f"title: {yaml_string(title)}",
        "scope: projects",
        "context_scope: project",
        f"visibility: {visibility}",
        "assembly_scope: project_context",
        f"status: {status}",
        f"timestamp: {iso_timestamp(stamp)}",
        f"created_at: {iso_date(stamp)}",
        f"updated_at: {iso_date(stamp)}",
        f"last_edited: {iso_date(stamp)}",
        "---",
        "",
    ]


def render_project_readme(title: str, summary: str, project_id: str, stamp: datetime) -> str:
    lines = common_frontmatter(
        concept_type="Project Status",
        title=f"{title} Status",
        project_id=project_id,
        status="active",
        stamp=stamp,
    )
    lines.extend(
        [
            f"# {title}",
            "",
            "## Purpose",
            "",
            summary or "Describe why this project matters.",
            "",
            "## Current Status",
            "",
            "Describe the latest durable state and date it when timing matters.",
            "",
            "## Next Move",
            "",
            "- [ ] Add the smallest useful next action.",
            "",
            "## Owners And Collaborators",
            "",
            "- Add owners, decision makers, and links to canonical people notes.",
            "",
            "## Decisions And Blockers",
            "",
            "- Add only decisions or blockers that change future work.",
            "",
            "## Sources",
            "",
            "- Add canonical documents, repositories, conversations, or datasets.",
            "- Device-local workspace paths belong in `.wirenet/project-bindings.json`.",
            "",
            "## Update History",
            "",
            f"- `{iso_date(stamp)}`: Project Pack created.",
            "",
        ]
    )
    return "\n".join(lines)


def render_project_agents(title: str, project_id: str, stamp: datetime) -> str:
    lines = common_frontmatter(
        concept_type="Runtime Adapter",
        title=f"{title} Agent Instructions",
        project_id=project_id,
        status="active",
        stamp=stamp,
        visibility="local",
    )
    lines.extend(
        [
            f"# {title} Agent Instructions",
            "",
            "## Purpose",
            "",
            "Keep this Project Pack useful as a durable handoff, not an activity log.",
            "",
            "## Read Order",
            "",
            "1. `GOAL.md` for the stable outcome and completion contract.",
            "2. `README.md` for current status, next move, decisions, and blockers.",
            "3. `RESULT.md` for completed outcomes and verification.",
            "4. Revisit the canonical sources listed below only when needed.",
            "",
            "## Recurring Sources",
            "",
            "- Add decision-bearing mail, messages, meetings, docs, repositories, or media workspaces.",
            "",
            "## Update Rules",
            "",
            "- Update `README.md` only when future work would otherwise misunderstand the project.",
            "- Update `GOAL.md` only when the desired outcome, constraints, or completion criteria change.",
            "- Update `RESULT.md` only for completed outcomes with evidence or verification.",
            "- Update this file only when read order, recurring sources, safety gates, or routing changes.",
            "- Do not record routine edits, command logs, raw source material, secrets, or generated files.",
            "",
            "## Safety Gates",
            "",
            "- Add project-specific actions that require explicit approval.",
            "",
        ]
    )
    return "\n".join(lines)


def render_project_goal(title: str, summary: str, project_id: str, stamp: datetime) -> str:
    lines = common_frontmatter(
        concept_type="Project Brief",
        title=f"{title} Goal",
        project_id=project_id,
        status="active",
        stamp=stamp,
    )
    lines.extend(
        [
            f"# {title} Goal",
            "",
            "## Outcome",
            "",
            summary or "Describe the observable outcome that means this project succeeded.",
            "",
            "## Baseline",
            "",
            "Describe the state before the current project phase.",
            "",
            "## Completion Criteria",
            "",
            "- [ ] Add an observable completion criterion.",
            "",
            "## Constraints And Non-Goals",
            "",
            "- Add important limits, dependencies, and explicit non-goals.",
            "",
            "## Approval Gates",
            "",
            "- Add decisions or external actions that require explicit approval.",
            "",
        ]
    )
    return "\n".join(lines)


def render_project_result(title: str, project_id: str, stamp: datetime) -> str:
    lines = common_frontmatter(
        concept_type="Project Result",
        title=f"{title} Results",
        project_id=project_id,
        status="pending",
        stamp=stamp,
    )
    lines.extend(
        [
            f"# {title} Results",
            "",
            "## Completed Outcomes",
            "",
            "- No completed outcome recorded yet.",
            "",
            "## Verification",
            "",
            "- Add commands, reviews, approvals, screenshots, or artifact links that prove completion.",
            "",
            "## Remaining Work",
            "",
            "- Refer to `README.md` for the active next move.",
            "",
        ]
    )
    return "\n".join(lines)


def project_id_from_readme(path: Path) -> str | None:
    if not path.is_file():
        return None
    match = re.search(r"(?m)^project_id:\s*[\"']?(?P<id>[^\"'\s]+)", path.read_text(encoding="utf-8"))
    return match.group("id") if match else None


def project_packet_for_id(manager_dir: Path, project_id: str) -> Path | None:
    for readme in sorted((manager_dir / "projects").glob("*/README.md")):
        if project_id_from_readme(readme) == project_id:
            return readme.parent
    return None


def insert_project_index(
    content: str,
    slug: str,
    title: str,
    stamp: datetime | None = None,
) -> str:
    heading = "## Active Project Packs"
    if heading not in content:
        raise ValueError(f"project index is missing {heading!r}")
    entry = f"- [[projects/{slug}/README|{title}]]"
    if entry in content.splitlines():
        updated = content
    else:
        marker = content.index(heading) + len(heading)
        line_end = content.find("\n", marker)
        if line_end < 0:
            updated = content + f"\n\n{entry}\n"
        else:
            updated = content[: line_end + 1] + f"\n{entry}" + content[line_end + 1 :]
    return re.sub(
        r"(?m)^last_edited:\s*.*$",
        f"last_edited: {iso_date(stamp)}",
        updated,
        count=1,
    )
