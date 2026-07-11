"""Canonical renderers and reconciliation helpers for Assistant vault artifacts."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path


ACTIVE_PACKETS_HEADING = "## Active packets"


def today() -> str:
    return date.today().isoformat()


def with_metadata(body: str, edited: str | None = None) -> str:
    return f"---\nlast_edited: {edited or today()}\n---\n\n{body.lstrip()}"


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def normalize_slug(value: str) -> str:
    text = normalize_text(value).lower()
    text = re.sub(r"[^a-z0-9._-]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def render_projects_readme(edited: str | None = None) -> str:
    return with_metadata(
        """# Projects

This folder indexes Assistant workstream packets. A packet may point to an
external repository or workspace; it does not need to contain implementation code.

## Active packets
""",
        edited,
    )


def render_projects_agents(edited: str | None = None) -> str:
    return with_metadata(
        """# AGENTS.md

## Purpose

This folder holds canonical rolling project packets.

## Structure

- `projects/README.md` indexes active packets.
- `projects/<project>/README.md` holds durable state, owners, decisions, blockers, open loops, and evidence.
- `projects/<project>/AGENTS.md` holds recurring sources and update-routing instructions.
- Optional `GOAL.md` and `RESULT.md` files record durable outcomes and completed verification.

## Defaults

- Prefer updating an existing canonical packet over creating an adjacent status note.
- A packet may route to an external repository or workspace.
- Use absolute dates and label inference when it matters.
""",
        edited,
    )


def render_project_readme(title: str, summary: str = "", edited: str | None = None) -> str:
    stamp = edited or today()
    purpose = summary or "Replace with why this project matters and the outcome to track."
    return "\n".join(
        [
            "---",
            f"title: {json.dumps(title)}",
            'status: "active"',
            "owner:",
            f"created_at: {stamp}",
            f"updated_at: {stamp}",
            f"last_edited: {stamp}",
            "tags:",
            "  - project",
            "---",
            "",
            f"# {title}",
            "",
            "## Purpose",
            "",
            f"- {purpose}",
            "",
            "## Current Status",
            "",
            "- Replace with the latest durable status, dated when timing matters.",
            "",
            "## People",
            "",
            "- Replace with owners, decision makers, collaborators, and canonical people notes.",
            "",
            "## Open Loops",
            "",
            "- Replace with pending decisions, blockers, and follow-ups.",
            "",
            "## Sources",
            "",
            "- Add direct evidence links and external workspace or repository paths.",
            "",
            "## Update History",
            "",
            f"- `{stamp}`: Created project packet.",
            "",
        ]
    )


def render_project_agents(title: str, edited: str | None = None) -> str:
    return with_metadata(
        f"""# {title} Instructions

## Purpose

This packet tracks `{title}` as a canonical workstream.

## Canonical Files

- `README.md`: durable status, owners, decisions, blockers, open loops, and evidence links.
- Optional `GOAL.md`: stable long-running outcome contract.
- Optional `RESULT.md`: completed milestone and verification evidence.

## Recurring Sources To Revisit

- Slack, DMs, and email: Replace with recurring decision-bearing conversations.
- Docs, meetings, repos, and external workspaces: Replace with canonical working artifacts.

## Update Rules

- Update `README.md` when durable status, ownership, blockers, decisions, or open loops change.
- Update this file only when recurring sources or packet routing change.
- Preserve one-off evidence links in `README.md` under `Sources`.
""",
        edited,
    )


def render_person_note(name: str, role: str = "", edited: str | None = None) -> str:
    stamp = edited or today()
    role_text = role or "Replace with confirmed context when known."
    return "\n".join(
        [
            "---",
            f"title: {json.dumps(name)}",
            "usernames: []",
            "aliases: []",
            "emails: []",
            "github_usernames: []",
            "teams: []",
            "tags:",
            "  - people",
            "last_seen_at:",
            f"created_at: {stamp}",
            f"updated_at: {stamp}",
            f"last_edited: {stamp}",
            "---",
            "",
            f"# {name}",
            "",
            "## Snapshot",
            "",
            f"- Name: {name}",
            f"- Team / role: {role_text}",
            "- Slack: Replace with handle and user ID when known.",
            "- Email: Replace with a confirmed address when known.",
            "",
            "## Why They Matter Now",
            "",
            "- Replace with a short, dated reason this relationship matters.",
            "",
            "## Working Style & Interaction Notes",
            "",
            "- Replace with evidence-backed collaboration patterns.",
            "",
            "## Collaboration Guidance",
            "",
            "- Replace with practical guidance for future work with this person.",
            "",
            "## Evidence Log",
            "",
            "- Add dated links to relevant messages, email, docs, meetings, or project notes.",
            "",
            "## Open Questions",
            "",
        ]
    )


def insert_router_entry(content: str, slug: str, title: str) -> str:
    if ACTIVE_PACKETS_HEADING not in content:
        raise ValueError(
            "Existing projects/README.md does not contain '## Active packets'; "
            "inspect the nonstandard router before writing."
        )
    entry = f"- [[projects/{slug}/README|{title}]]"
    if entry in {line.rstrip() for line in content.splitlines()}:
        return content
    marker_index = content.index(ACTIVE_PACKETS_HEADING) + len(ACTIVE_PACKETS_HEADING)
    line_end = content.find("\n", marker_index)
    if line_end < 0:
        return content + f"\n\n{entry}\n"
    return content[: line_end + 1] + f"\n{entry}" + content[line_end + 1 :]


def ensure_project_router(vault_dir: Path, dry_run: bool = False) -> tuple[Path, str]:
    router_path = vault_dir / "projects" / "README.md"
    if router_path.exists():
        return router_path, router_path.read_text(encoding="utf-8")
    content = render_projects_readme()
    if not dry_run:
        router_path.parent.mkdir(parents=True, exist_ok=True)
        router_path.write_text(content, encoding="utf-8")
    return router_path, content
