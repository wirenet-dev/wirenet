#!/usr/bin/env python3
"""Create and list a project packet in an Assistant vault."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from vault_model import (
    ensure_project_router,
    insert_router_entry,
    normalize_slug,
    normalize_text,
    render_project_agents,
    render_project_readme,
)


def default_vault_dir() -> Path:
    return Path(__file__).resolve().parents[4]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create and list a new project packet.")
    parser.add_argument(
        "--vault-dir",
        default=str(default_vault_dir()),
        help="Vault root path. Defaults to the personal monorepo root containing this script.",
    )
    parser.add_argument("--title", required=True, help="Human-readable project title.")
    parser.add_argument(
        "--slug",
        default="",
        help="Optional file-system slug; defaults to the normalized title.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Report the proposed creation without writing.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    vault_dir = Path(args.vault_dir).expanduser().resolve(strict=False)
    title = normalize_text(args.title)
    if not title:
        raise SystemExit("Invalid --title value after normalization.")
    slug = normalize_slug(args.slug or title)
    if not slug:
        raise SystemExit("Invalid --slug value after normalization.")

    projects_dir = vault_dir / "projects"
    packet_dir = projects_dir / slug
    packet_path = packet_dir / "README.md"
    routing_path = packet_dir / "AGENTS.md"
    if packet_dir.exists():
        raise SystemExit(f"Project packet already exists; inspect and update that packet instead: {packet_dir}")
    router_path, router_content = ensure_project_router(vault_dir, dry_run=True)
    entry = f"- [[projects/{slug}/README|{title}]]\n"
    try:
        updated_router = insert_router_entry(router_content, slug, title)
    except ValueError as error:
        raise SystemExit(str(error)) from error

    packet = render_project_readme(title)
    routing = render_project_agents(title)

    result = {
        "ok": True,
        "dry_run": bool(args.dry_run),
        "packet_path": str(packet_path),
        "routing_path": str(routing_path),
        "router_path": str(router_path),
        "router_entry": entry.rstrip(),
        "slug": slug,
    }
    if not args.dry_run:
        packet_dir.mkdir(parents=True, exist_ok=False)
        packet_path.write_text(packet, encoding="utf-8")
        routing_path.write_text(routing, encoding="utf-8")
        router_path.parent.mkdir(parents=True, exist_ok=True)
        router_path.write_text(updated_router, encoding="utf-8")
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
