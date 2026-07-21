#!/usr/bin/env python3
"""Shared data model and renderers for wirenet Manager v0.2."""

from __future__ import annotations

import json
import re
import uuid
from datetime import UTC, datetime
from pathlib import Path


MANAGER_SCHEMA = "wirenet-manager/v0.2"
PROJECT_PACK_SCHEMA = "wirenet-project-pack/v0.1"
EXPERIMENT_PACK_SCHEMA = "wirenet-experiment-pack/v0.1"
BINDINGS_SCHEMA = "wirenet-workspace-bindings/v0.2"
PROJECT_OKF_PROFILE = "wirenet-okf-project-pack/v0.1"
EXPERIMENT_OKF_PROFILE = "wirenet-okf-experiment-pack/v0.1"
RUNTIME_SCHEMA = "wirenet-runtime/v0.1"


def installed_plugin_version() -> str:
    """Read the installed package version from the canonical plugin manifest."""
    manifest = Path(__file__).resolve().parents[1] / ".codex-plugin/plugin.json"
    try:
        payload = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(
            f"cannot read plugin version from {manifest}: {error}"
        ) from error
    version = payload.get("version")
    if not isinstance(version, str) or not version.strip():
        raise RuntimeError(f"plugin manifest {manifest} has no version")
    return version.strip()


PLUGIN_VERSION = installed_plugin_version()

PROJECT_STATUSES = ("active", "waiting", "blocked", "completed", "archived")
EXPERIMENT_STATUSES = ("active", "concluded", "promoted", "archived")


def manager_schema_version(value: str) -> tuple[int, int] | None:
    match = re.fullmatch(r"wirenet-manager/v(\d+)\.(\d+)", value)
    return (int(match.group(1)), int(match.group(2))) if match else None


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


def new_experiment_id() -> str:
    return f"exp_{uuid.uuid4()}"


def manager_metadata(manager_id: str | None = None) -> dict[str, object]:
    stamp = iso_timestamp()
    return {
        "schema_version": MANAGER_SCHEMA,
        "manager_id": manager_id or new_manager_id(),
        "created_at": stamp,
        "updated_at": stamp,
        "plugin_version": PLUGIN_VERSION,
        "project_pack_profile": PROJECT_PACK_SCHEMA,
        "experiment_pack_profile": EXPERIMENT_PACK_SCHEMA,
        "okf_profiles": [PROJECT_OKF_PROFILE, EXPERIMENT_OKF_PROFILE],
    }


def empty_workspace_bindings() -> dict[str, object]:
    return {
        "schema_version": BINDINGS_SCHEMA,
        "updated_at": iso_timestamp(),
        "projects": [],
        "experiments": [],
        "ignored": [],
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


def load_workspace_bindings(manager_dir: Path) -> dict[str, object]:
    path = manager_dir / ".wirenet/workspace-bindings.json"
    if not path.exists():
        return empty_workspace_bindings()
    value = load_json(path)
    value.setdefault("projects", [])
    value.setdefault("experiments", [])
    value.setdefault("ignored", [])
    return value


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def concept_frontmatter(
    *,
    concept_type: str,
    schema: str,
    identity_key: str,
    identity: str,
    title: str,
    description: str,
    status: str,
    stamp: datetime,
    visibility: str = "private",
    producer: str | None = None,
) -> list[str]:
    lines = [
        "---",
        f"type: {yaml_string(concept_type)}",
        f"schema: {yaml_string(schema)}",
        f"{identity_key}: {yaml_string(identity)}",
        f"title: {yaml_string(title)}",
        f"description: {yaml_string(' '.join(description.split()))}",
        f"visibility: {visibility}",
        f"status: {status}",
    ]
    if producer:
        lines.append(f"producer: {yaml_string(producer)}")
    lines.extend(
        [
            f"created_at: {yaml_string(iso_date(stamp))}",
            f"updated_at: {yaml_string(iso_date(stamp))}",
            "---",
            "",
        ]
    )
    return lines


def project_frontmatter(
    *,
    concept_type: str,
    title: str,
    description: str,
    project_id: str,
    status: str,
    stamp: datetime,
    producer: str | None = None,
) -> list[str]:
    return concept_frontmatter(
        concept_type=concept_type,
        schema=PROJECT_PACK_SCHEMA,
        identity_key="project_id",
        identity=project_id,
        title=title,
        description=description,
        status=status,
        stamp=stamp,
        producer=producer,
    )


def experiment_frontmatter(
    *,
    concept_type: str,
    title: str,
    description: str,
    experiment_id: str,
    status: str,
    stamp: datetime,
) -> list[str]:
    return concept_frontmatter(
        concept_type=concept_type,
        schema=EXPERIMENT_PACK_SCHEMA,
        identity_key="experiment_id",
        identity=experiment_id,
        title=title,
        description=description,
        status=status,
        stamp=stamp,
    )


def runtime_frontmatter(
    *,
    title: str,
    identity_key: str,
    identity: str,
    stamp: datetime,
) -> list[str]:
    return [
        "---",
        f"schema: {yaml_string(RUNTIME_SCHEMA)}",
        f"{identity_key}: {yaml_string(identity)}",
        f"title: {yaml_string(title)}",
        "audience: agent",
        "visibility: local",
        "status: active",
        f"created_at: {yaml_string(iso_date(stamp))}",
        f"updated_at: {yaml_string(iso_date(stamp))}",
        "---",
        "",
    ]


def render_project_readme(
    title: str,
    description: str,
    project_id: str,
    stamp: datetime,
    *,
    source_experiment: str = "",
) -> str:
    lines = project_frontmatter(
        concept_type="Project Status",
        title=title,
        description=description,
        project_id=project_id,
        status="active",
        stamp=stamp,
    )
    if source_experiment:
        lines.insert(-2, f"source_experiment_id: {yaml_string(source_experiment)}")
    lines.extend(
        [
            f"# {title}",
            "",
            "## Purpose",
            "",
            description or "Describe why this project matters.",
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
            "- Device-local workspace paths belong in `.wirenet/workspace-bindings.json`.",
            "",
        ]
    )
    return "\n".join(lines)


def render_project_agents(title: str, project_id: str, stamp: datetime) -> str:
    lines = runtime_frontmatter(
        title=f"{title} Agent Instructions",
        identity_key="project_id",
        identity=project_id,
        stamp=stamp,
    )
    lines.extend(
        [
            f"# {title} Agent Instructions",
            "",
            "## Purpose",
            "",
            "Keep this Project Pack useful as an open, durable handoff rather than a fixed form or activity log.",
            "",
            "## Read Order",
            "",
            "1. `README.md` for the current state, next move, decisions, and blockers.",
            "2. This `AGENTS.md` for recurring sources, safety, and routing.",
            "3. Read `GOAL.md`, `RESULT.md`, `WORKLOG.md`, or `log.md` only when present and relevant.",
            "4. Follow links to additional Project Pack concepts only as the task needs them.",
            "5. Revisit canonical external sources selectively when a workspace is bound.",
            "",
            "## Recurring Sources",
            "",
            "- Add decision-bearing mail, messages, meetings, docs, repositories, or media workspaces.",
            "",
            "## Update Rules",
            "",
            "- Update `README.md` only when future work would otherwise misunderstand the project.",
            "- Create or update `GOAL.md` only when a separate durable outcome contract improves the handoff.",
            "- Create or update `RESULT.md` only when completed outcomes deserve durable evidence or verification.",
            "- Only an explicitly invoked UltraGoal may create or update `WORKLOG.md`.",
            "- Create or update `log.md` only when sparse chronology materially improves navigation or synchronization.",
            "- Never mirror detailed UltraGoal WORKLOG entries into `log.md`.",
            "- Additional Markdown concepts are allowed when they have a clear purpose, OKF `type`, and this packet's `project_id`.",
            "- Update this file only when read order, recurring sources, safety gates, or routing changes.",
            "- Do not record raw source material, secrets, or generated files.",
            "",
            "## Safety Gates",
            "",
            "- Add project-specific actions that require explicit approval.",
            "",
        ]
    )
    return "\n".join(lines)


def render_project_goal(
    title: str, description: str, project_id: str, stamp: datetime
) -> str:
    lines = project_frontmatter(
        concept_type="Project Brief",
        title=f"{title} Goal",
        description=description,
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
            description
            or "Describe the observable outcome that means this project succeeded.",
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
    lines = project_frontmatter(
        concept_type="Project Result",
        title=f"{title} Results",
        description=f"Completed outcomes and verification for {title}.",
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


def render_project_log(title: str, stamp: datetime) -> str:
    return "\n".join(
        [
            f"# {title} Update Log",
            "",
            f"## {iso_date(stamp)}",
            "",
            "- **Creation**: Created the Project Pack; see [current status](README.md).",
            "",
        ]
    )


def render_experiment_readme(
    title: str,
    question: str,
    decision_criterion: str,
    experiment_id: str,
    stamp: datetime,
) -> str:
    lines = experiment_frontmatter(
        concept_type="Experiment Status",
        title=title,
        description=question,
        experiment_id=experiment_id,
        status="active",
        stamp=stamp,
    )
    lines.extend(
        [
            f"# {title}",
            "",
            "## Question",
            "",
            question,
            "",
            "## Bound",
            "",
            "Describe the smallest useful spike and its time, evidence, or scope limit.",
            "",
            "## Decision Criterion",
            "",
            decision_criterion,
            "",
            "## Current State",
            "",
            "Describe the latest durable observation without turning this into an activity log.",
            "",
            "## Next Move",
            "",
            "- [ ] Run the smallest useful next experiment.",
            "",
            "## Sources",
            "",
            "- Add links to relevant evidence or an optional `RESULT.md` when the conclusion deserves it.",
            "- Device-local workspace paths belong in `.wirenet/workspace-bindings.json`.",
            "",
        ]
    )
    return "\n".join(lines)


def render_experiment_agents(title: str, experiment_id: str, stamp: datetime) -> str:
    lines = runtime_frontmatter(
        title=f"{title} Experiment Instructions",
        identity_key="experiment_id",
        identity=experiment_id,
        stamp=stamp,
    )
    lines.extend(
        [
            f"# {title} Experiment Instructions",
            "",
            "## Purpose",
            "",
            "Keep this spike bounded, decision-oriented, and lighter than a Project Pack.",
            "",
            "## Read Order",
            "",
            "1. `README.md` for the question, bound, decision criterion, and next move.",
            "2. This `AGENTS.md` for routing and safety.",
            "3. Read optional `RESULT.md` or other typed concepts only when present and relevant.",
            "",
            "## Update Rules",
            "",
            "- Record durable observations, not every trial or command.",
            "- Conclude, archive, or promote the experiment when the decision criterion is met.",
            "- Promote before using UltraGoal; persistent multi-iteration work belongs in a Project Pack.",
            "- Preserve this packet as historical evidence after promotion.",
            "- Do not record raw source material, secrets, or generated files.",
            "",
        ]
    )
    return "\n".join(lines)


def render_experiment_result(title: str, experiment_id: str, stamp: datetime) -> str:
    lines = experiment_frontmatter(
        concept_type="Experiment Result",
        title=f"{title} Result",
        description=f"Conclusion and decision evidence for {title}.",
        experiment_id=experiment_id,
        status="pending",
        stamp=stamp,
    )
    lines.extend(
        [
            f"# {title} Result",
            "",
            "## Observation",
            "",
            "- Record the durable finding.",
            "",
            "## Evidence",
            "",
            "- Link the smallest evidence needed to support the conclusion.",
            "",
            "## Decision",
            "",
            "- Conclude, archive, or promote this experiment.",
            "",
        ]
    )
    return "\n".join(lines)


def frontmatter(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        return {}
    end = content.find("\n---\n", 4)
    if end < 0:
        return {}
    values: dict[str, str] = {}
    for line in content[4:end].splitlines():
        if ":" not in line or line.startswith((" ", "-")):
            continue
        key, raw = line.split(":", 1)
        value = raw.strip()
        if value.startswith('"') and value.endswith('"'):
            try:
                decoded = json.loads(value)
                if isinstance(decoded, str):
                    value = decoded
            except json.JSONDecodeError:
                value = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        values[key.strip()] = value
    return values


def update_frontmatter(content: str, updates: dict[str, str]) -> str:
    if not content.startswith("---\n"):
        raise ValueError("document is missing YAML frontmatter")
    end = content.find("\n---\n", 4)
    if end < 0:
        raise ValueError("document has malformed YAML frontmatter")
    lines = content[4:end].splitlines()
    positions = {
        line.split(":", 1)[0].strip(): index
        for index, line in enumerate(lines)
        if ":" in line and not line.startswith((" ", "-"))
    }
    for key, value in updates.items():
        rendered = (
            f"{key}: {yaml_string(value)}"
            if key
            in {
                "name",
                "title",
                "description",
                "created_at",
                "summary",
                "producer",
                "promoted_to_project_id",
                "source_experiment_id",
                "updated_at",
            }
            else f"{key}: {value}"
        )
        if key in positions:
            lines[positions[key]] = rendered
        else:
            lines.append(rendered)
    return "---\n" + "\n".join(lines) + content[end:]


def remove_frontmatter_keys(content: str, keys: set[str]) -> str:
    if not content.startswith("---\n"):
        raise ValueError("document is missing YAML frontmatter")
    end = content.find("\n---\n", 4)
    if end < 0:
        raise ValueError("document has malformed YAML frontmatter")
    lines = content[4:end].splitlines()
    kept = [
        line
        for line in lines
        if not (
            ":" in line
            and not line.startswith((" ", "-"))
            and line.split(":", 1)[0].strip() in keys
        )
    ]
    return "---\n" + "\n".join(kept) + content[end:]


def project_id_from_readme(path: Path) -> str | None:
    return frontmatter(path).get("project_id")


def experiment_id_from_readme(path: Path) -> str | None:
    return frontmatter(path).get("experiment_id")


def project_packet_for_id(manager_dir: Path, project_id: str) -> Path | None:
    for readme in sorted((manager_dir / "projects").glob("*/README.md")):
        if project_id_from_readme(readme) == project_id:
            return readme.parent
    return None


def experiment_packet_for_id(manager_dir: Path, experiment_id: str) -> Path | None:
    for readme in sorted((manager_dir / "experiments").glob("*/README.md")):
        if experiment_id_from_readme(readme) == experiment_id:
            return readme.parent
    return None


def workspace_paths(bindings: dict[str, object]) -> set[str]:
    rows = [
        *bindings.get("projects", []),
        *bindings.get("experiments", []),
        *bindings.get("ignored", []),
    ]
    return {
        str(row.get("path"))
        for row in rows
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }


def render_projects_index(manager_dir: Path) -> str:
    sections = {
        "active": "Active Project Packs",
        "waiting": "Waiting And Blocked",
        "blocked": "Waiting And Blocked",
        "completed": "Completed Project Packs",
        "archived": "Archived Project Packs",
    }
    grouped: dict[str, list[str]] = {
        heading: [] for heading in dict.fromkeys(sections.values())
    }
    for readme in sorted((manager_dir / "projects").glob("*/README.md")):
        metadata = frontmatter(readme)
        status = metadata.get("status", "active")
        heading = sections.get(status, "Active Project Packs")
        title = (
            metadata.get("title") or metadata.get("name") or readme.parent.name
        )
        description = metadata.get("description") or metadata.get("summary", "")
        entry = f"- [{title}]({readme.parent.name}/README.md)"
        if description:
            entry += f" — {description}"
        grouped[heading].append(entry)
    lines = [
        "# Projects",
        "",
        "This index catalogs Manager-native and externally bound Project Packs.",
        "External code, media, data, and deliverables remain in their own workspaces.",
        "",
    ]
    for heading in dict.fromkeys(sections.values()):
        lines.extend([f"## {heading}", "", *grouped[heading], ""])
    return "\n".join(lines).rstrip() + "\n"


def render_experiments_index(manager_dir: Path) -> str:
    sections = {
        "active": "Active Experiments",
        "concluded": "Concluded Experiments",
        "promoted": "Promoted Experiments",
        "archived": "Archived Experiments",
    }
    grouped: dict[str, list[str]] = {heading: [] for heading in sections.values()}
    for readme in sorted((manager_dir / "experiments").glob("*/README.md")):
        metadata = frontmatter(readme)
        status = metadata.get("status", "active")
        heading = sections.get(status, "Active Experiments")
        title = (
            metadata.get("title") or metadata.get("name") or readme.parent.name
        )
        description = metadata.get("description") or metadata.get("summary", "")
        entry = f"- [{title}]({readme.parent.name}/README.md)"
        if description:
            entry += f" — {description}"
        grouped[heading].append(entry)
    lines = [
        "---",
        "okf_version: 0.1",
        "---",
        "",
        "# Experiments",
        "",
        "This index catalogs bounded spikes and their outcomes.",
        "",
    ]
    for status, heading in sections.items():
        lines.extend([f"## {heading}", "", *grouped[heading], ""])
    return "\n".join(lines).rstrip() + "\n"
