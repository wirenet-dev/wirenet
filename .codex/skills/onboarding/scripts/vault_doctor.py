#!/usr/bin/env python3
"""Audit and optionally reconcile the canonical Assistant vault scaffold."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import date
from pathlib import Path

from setup_shared_memory_vault import (
    ROOT_AGENTS_TEMPLATE,
    TODO_TEMPLATE,
    USER_CONTEXT_TEMPLATE,
)
from vault_model import (
    insert_router_entry,
    render_projects_agents,
    render_projects_readme,
    with_metadata,
)


REQUIRED_DIRS = ("agent", "people", "projects", "notes", "sources")
SCAFFOLD = {
    "AGENTS.md": lambda stamp: with_metadata(ROOT_AGENTS_TEMPLATE, stamp),
    "TODO.md": lambda stamp: with_metadata(TODO_TEMPLATE, stamp),
    "agent/USER_CONTEXT.md": lambda stamp: with_metadata(USER_CONTEXT_TEMPLATE, stamp),
    "projects/README.md": render_projects_readme,
    "projects/AGENTS.md": render_projects_agents,
    "notes/.gitkeep": lambda _stamp: "",
    "sources/.gitkeep": lambda _stamp: "",
}
TEMPORARY_HANDOFF_NAMES = ("MIGRATION_HANDOFF.md", "VAULT_MIGRATION_HANDOFF.md")


def default_vault_dir() -> Path:
    return Path(__file__).resolve().parents[4]


def has_iso_last_edited(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or text.count("---") < 2:
        return False
    raw = text.split("---", 2)[1]
    for line in raw.splitlines():
        if line.startswith("last_edited:"):
            value = line.partition(":")[2].strip().strip('"\'')
            try:
                date.fromisoformat(value)
            except ValueError:
                return False
            return True
    return False


def is_plugin_skill(path: Path, vault_dir: Path) -> bool:
    relative = path.relative_to(vault_dir)
    return path.name == "SKILL.md" and "plugins" in relative.parts and "skills" in relative.parts


def configured_remotes(vault_dir: Path) -> dict[str, str]:
    if not (vault_dir / ".git").exists():
        return {}
    result = subprocess.run(
        ["git", "remote", "-v"],
        cwd=vault_dir,
        check=False,
        capture_output=True,
        text=True,
    )
    remotes: dict[str, str] = {}
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0] not in remotes:
            remotes[parts[0]] = parts[1]
    return remotes


def reconcile(vault_dir: Path) -> list[str]:
    created: list[str] = []
    stamp = date.today().isoformat()
    for rel_dir in REQUIRED_DIRS:
        path = vault_dir / rel_dir
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            created.append(rel_dir + "/")
    for relative, renderer in SCAFFOLD.items():
        path = vault_dir / relative
        if path.exists():
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(renderer(stamp), encoding="utf-8")
        created.append(relative)

    router_path = vault_dir / "projects" / "README.md"
    router = router_path.read_text(encoding="utf-8")
    original_router = router
    if "## Active packets" in router:
        for packet in sorted((vault_dir / "projects").iterdir()):
            if not packet.is_dir() or not (packet / "README.md").exists():
                continue
            title = packet.name.replace("-", " ").title()
            packet_text = (packet / "README.md").read_text(encoding="utf-8")
            for line in packet_text.splitlines():
                if line.startswith("# "):
                    title = line[2:].strip()
                    break
            updated = insert_router_entry(router, packet.name, title)
            if updated != router:
                router = updated
                created.append(f"projects/README.md entry: {packet.name}")
    if router != original_router:
        router_path.write_text(router, encoding="utf-8")
    return created


def inspect(vault_dir: Path) -> dict[str, object]:
    missing_dirs = [rel for rel in REQUIRED_DIRS if not (vault_dir / rel).is_dir()]
    missing_files = [rel for rel in SCAFFOLD if not (vault_dir / rel).is_file()]
    invalid_markdown = [
        path.relative_to(vault_dir).as_posix()
        for path in sorted(vault_dir.rglob("*.md"))
        if not is_plugin_skill(path, vault_dir) and not has_iso_last_edited(path)
    ]
    ignored_caches = [
        path.relative_to(vault_dir).as_posix()
        for path in sorted(vault_dir.rglob("*"))
        if path.name == "__pycache__" or path.suffix in {".pyc", ".pyo"}
    ]
    stale_handoffs = [name for name in TEMPORARY_HANDOFF_NAMES if (vault_dir / name).exists()]
    router_issues: list[str] = []
    router_schema_issue = False
    router_path = vault_dir / "projects" / "README.md"
    if router_path.exists():
        router = router_path.read_text(encoding="utf-8")
        router_schema_issue = "## Active packets" not in router
        for packet in sorted((vault_dir / "projects").glob("*/README.md")):
            slug = packet.parent.name
            if f"[[projects/{slug}/README|" not in router:
                router_issues.append(slug)

    errors = missing_dirs + missing_files + invalid_markdown + ignored_caches + stale_handoffs + router_issues
    if router_schema_issue:
        errors.append("projects/README.md: missing Active packets heading")
    return {
        "ok": not errors,
        "vault_dir": str(vault_dir),
        "missing_dirs": missing_dirs,
        "missing_files": missing_files,
        "invalid_markdown": invalid_markdown,
        "missing_router_entries": router_issues,
        "nonstandard_project_router": router_schema_issue,
        "ignored_caches": ignored_caches,
        "stale_handoffs": stale_handoffs,
        "repository": (vault_dir / ".git").exists(),
        "remotes": configured_remotes(vault_dir),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit an Assistant shared-memory vault.")
    parser.add_argument("--vault-dir", default=str(default_vault_dir()))
    parser.add_argument(
        "--repair",
        action="store_true",
        help="Create only missing canonical scaffold and router entries; preserve existing files.",
    )
    args = parser.parse_args()
    vault_dir = Path(args.vault_dir).expanduser().resolve(strict=False)
    created = reconcile(vault_dir) if args.repair else []
    result = inspect(vault_dir)
    result["repair"] = bool(args.repair)
    result["created"] = created
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
