#!/usr/bin/env python3
"""Materialize a wirenet Manager from the plugin's seed.

Copies the seed (templates/manager) into the target directory without ever
overwriting existing files, initializes git when absent, and creates the
first commit so the user's history starts with their own content.
Dry-run-first: preview with --dry-run, then run for real after approval.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
SEED = PLUGIN_ROOT / "templates" / "manager"


def default_manager_dir() -> Path:
    configured = os.environ.get("WIRENET_MANAGER_DIR")
    return Path(configured).expanduser() if configured else Path.home() / "Manager"


def git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(cwd), *args], check=False, capture_output=True, text=True
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manager-dir", type=Path, default=default_manager_dir())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    target = args.manager_dir.expanduser().resolve(strict=False)
    if not SEED.is_dir():
        print(json.dumps({"ok": False, "error": f"seed missing: {SEED}"}))
        return 1
    if target != target.parent / target.name or (SEED in target.parents):
        pass  # normalized
    # Never nest a Manager inside an existing one.
    for parent in target.parents:
        if (parent / ".wirenet" / "workspace-bindings.json").is_file():
            print(json.dumps({
                "ok": False,
                "error": f"{parent} already looks like a Manager; refusing to nest one at {target}",
            }))
            return 1

    created: list[str] = []
    skipped: list[str] = []
    for source in sorted(SEED.rglob("*")):
        rel = source.relative_to(SEED)
        dest = target / rel
        if source.is_dir():
            if not dest.exists():
                created.append(str(rel) + "/")
                if not args.dry_run:
                    dest.mkdir(parents=True, exist_ok=True)
        else:
            if dest.exists():
                skipped.append(str(rel))
            else:
                created.append(str(rel))
                if not args.dry_run:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, dest)

    git_initialized = False
    committed = False
    if not args.dry_run:
        if not (target / ".git").exists():
            if git(target, "init", "-q").returncode == 0:
                git_initialized = True
        if (target / ".git").exists():
            git(target, "add", "-A")
            status = git(target, "status", "--porcelain")
            if status.stdout.strip():
                result = git(
                    target, "-c", "user.name=wirenet setup",
                    "-c", "user.email=setup@wirenet.dev",
                    "commit", "-q", "-m", "manager: materialize v0.5 seed",
                )
                committed = result.returncode == 0

    print(json.dumps({
        "ok": True,
        "dry_run": args.dry_run,
        "manager_dir": str(target),
        "created": created,
        "skipped_existing": skipped,
        "git_initialized": git_initialized,
        "committed": committed,
        "next_steps": [
            "Personalize AGENTS.md (Collaboration) and agent/USER_CONTEXT.md from the calibrated interview.",
            "Propose initial packs, areas, and people files; create only explicitly approved items.",
            "Offer global wiring, bindings, qmd, and continuity — each with its own approval.",
        ],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
