from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SHARED_SCRIPTS = Path(__file__).resolve().parents[2] / "onboarding" / "scripts"
sys.path.insert(0, str(SHARED_SCRIPTS))

from vault_model import render_person_note  # noqa: E402


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "new-person"


def build_note(name: str, role: str) -> str:
    return render_person_note(name, role)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a people note.")
    parser.add_argument("name")
    parser.add_argument("--role", default="")
    parser.add_argument("--slug", default="")
    parser.add_argument(
        "--vault-dir",
        default=str(ROOT),
        help="Vault root path. Defaults to the repository containing this script.",
    )
    args = parser.parse_args()

    vault_dir = Path(args.vault_dir).expanduser().resolve(strict=False)
    people_dir = vault_dir / "people"
    slug = args.slug or slugify(args.name)
    path = people_dir / f"{slug}.md"
    if path.exists():
        print(f"exists: {path.relative_to(vault_dir)}")
        return 0

    people_dir.mkdir(parents=True, exist_ok=True)
    path.write_text(build_note(args.name, args.role), encoding="utf-8")
    print(f"created: {path.relative_to(vault_dir)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
