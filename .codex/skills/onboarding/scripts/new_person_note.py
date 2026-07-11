#!/usr/bin/env python3
"""Create a replaceable person-note scaffold in an Assistant vault."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from vault_model import normalize_slug, normalize_text, render_person_note


def default_vault_dir() -> Path:
    return Path(__file__).resolve().parents[4]


def normalize_key(value: str) -> str:
    text = normalize_text(value).lower()
    if "@" in text:
        text = text.split("@", 1)[0]
    return normalize_slug(text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a new person note. Optionally choose a stable key when a durable handle is known."
    )
    parser.add_argument(
        "--vault-dir",
        default=str(default_vault_dir()),
        help="Vault root path. Defaults to the personal monorepo root containing this script.",
    )
    parser.add_argument("--name", required=True, help="Display name.")
    parser.add_argument(
        "--key",
        default="",
        help="Optional stable file key; defaults to the normalized name. Prefer a durable handle when known.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Report the proposed creation without writing.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    vault_dir = Path(args.vault_dir).expanduser().resolve(strict=False)
    name = normalize_text(args.name)
    if not name:
        raise SystemExit("Invalid --name value after normalization.")
    key = normalize_key(args.key or name)
    if not key:
        raise SystemExit("Invalid stable key after normalization.")

    note_path = vault_dir / "people" / f"{key}.md"
    if note_path.exists():
        raise SystemExit(f"Person note already exists; update the canonical note instead: {note_path}")

    content = render_person_note(name)

    result = {"ok": True, "dry_run": bool(args.dry_run), "path": str(note_path), "stable_key": key}
    if not args.dry_run:
        note_path.parent.mkdir(parents=True, exist_ok=True)
        note_path.write_text(content, encoding="utf-8")
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
