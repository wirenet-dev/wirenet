#!/usr/bin/env python3
"""Preview, create, or conservatively repair a WireNet Manager v0.2."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[3]
PLUGIN_SCRIPTS = PLUGIN_ROOT / "scripts"
sys.path.insert(0, str(PLUGIN_SCRIPTS))

from manager_doctor import inspect  # noqa: E402
from manager_model import manager_metadata, write_json  # noqa: E402
from upgrade_manager import plan_upgrade  # noqa: E402


DEFAULT_TEMPLATE = PLUGIN_ROOT / "templates/manager"
CANONICAL_DIRECTORIES = (
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


def run(
    command: list[str],
    *,
    cwd: Path,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        command,
        cwd=cwd,
        check=check,
        capture_output=True,
        text=True,
        env=environment,
    )


def copy_missing(template: Path, destination: Path) -> list[str]:
    created: list[str] = []
    for source in sorted(path for path in template.rglob("*") if path.is_file()):
        relative = source.relative_to(template)
        target = destination / relative
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        created.append(relative.as_posix())
    return created


def create_missing_directories(destination: Path) -> list[str]:
    created: list[str] = []
    for relative in CANONICAL_DIRECTORIES:
        target = destination / relative
        if target.is_dir():
            continue
        target.mkdir(parents=True, exist_ok=True)
        created.append(f"{relative}/")
    return created


def initialize_git(manager_dir: Path) -> str:
    try:
        run(["git", "init", "-b", "main"], cwd=manager_dir)
    except subprocess.CalledProcessError:
        run(["git", "init"], cwd=manager_dir)
        run(["git", "branch", "-M", "main"], cwd=manager_dir)

    if not run(
        ["git", "config", "user.name"], cwd=manager_dir, check=False
    ).stdout.strip():
        run(["git", "config", "user.name", "WireNet Manager"], cwd=manager_dir)
    if not run(
        ["git", "config", "user.email"], cwd=manager_dir, check=False
    ).stdout.strip():
        run(
            ["git", "config", "user.email", "manager@localhost.invalid"],
            cwd=manager_dir,
        )

    run(["git", "add", "."], cwd=manager_dir)
    run(
        [
            "git",
            "-c",
            "commit.gpgsign=false",
            "commit",
            "-m",
            "chore(manager): bootstrap local workspace",
        ],
        cwd=manager_dir,
    )
    return run(["git", "rev-parse", "HEAD"], cwd=manager_dir).stdout.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manager-dir", default="~/Manager")
    parser.add_argument("--template-dir", default=str(DEFAULT_TEMPLATE))
    parser.add_argument("--repair", action="store_true")
    parser.add_argument("--apply", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manager_dir = Path(args.manager_dir).expanduser().resolve(strict=False)
    template_dir = Path(args.template_dir).expanduser().resolve(strict=False)
    exists = manager_dir.exists()
    result: dict[str, object] = {
        "ok": True,
        "dry_run": not args.apply,
        "manager_dir": str(manager_dir),
        "template_dir": str(template_dir),
        "state": "existing" if exists else "new",
        "actions": [],
    }

    if not template_dir.is_dir():
        result.update({"ok": False, "error": "bundled Manager template is missing"})
        print(json.dumps(result, indent=2))
        return 2

    if exists and not manager_dir.is_dir():
        result.update(
            {"ok": False, "error": "destination exists and is not a directory"}
        )
        print(json.dumps(result, indent=2))
        return 2

    if exists and (manager_dir / ".wirenet/manager.json").is_file():
        upgrade = plan_upgrade(manager_dir)
        if upgrade.get("state") != "current":
            result.update(
                {
                    "ok": False,
                    "state": upgrade.get("state"),
                    "upgrade": upgrade,
                    "next_action": "review upgrade_manager.py, then rerun it with --apply",
                }
            )
            print(json.dumps(result, indent=2))
            return 2

    if exists and not args.repair:
        diagnosis = inspect(manager_dir)
        result.update(
            {
                "ok": diagnosis["ok"],
                "state": "healthy" if diagnosis["ok"] else "needs-repair",
                "doctor": diagnosis,
                "next_action": None
                if diagnosis["ok"]
                else "review and rerun with --repair",
            }
        )
        print(json.dumps(result, indent=2))
        return 0 if diagnosis["ok"] else 2

    if exists:
        diagnosis = inspect(manager_dir)
        result["actions"] = [
            f"create missing scaffold path: {path}" for path in diagnosis["missing"]
        ]
        if not args.apply:
            result["doctor"] = diagnosis
            print(json.dumps(result, indent=2))
            return 0
    else:
        result["actions"] = [
            "copy the bundled content-only Manager template",
            "write local Manager metadata and bindings",
            "initialize a local Git repository on main",
            "create an initial local commit without configuring a remote",
            "run the Manager doctor and require ok=true",
        ]
        if not args.apply:
            print(json.dumps(result, indent=2))
            return 0

    created_new = not exists
    if created_new:
        manager_dir.mkdir(parents=True)

    try:
        created_paths = create_missing_directories(manager_dir)
        created_paths.extend(copy_missing(template_dir, manager_dir))
        metadata_path = manager_dir / ".wirenet/manager.json"
        if not metadata_path.exists():
            write_json(metadata_path, manager_metadata())
            created_paths.append(".wirenet/manager.json")

        commit = initialize_git(manager_dir) if created_new else None
        diagnosis = inspect(manager_dir)
        if diagnosis["ok"] is not True:
            raise RuntimeError("Manager doctor did not return ok=true")
    except (OSError, subprocess.CalledProcessError, RuntimeError, ValueError) as error:
        result.update(
            {
                "ok": False,
                "dry_run": False,
                "error": str(error),
                "recovery": "No cleanup was attempted; inspect the destination before retrying.",
            }
        )
        print(json.dumps(result, indent=2))
        return 1

    result.update(
        {
            "dry_run": False,
            "state": "created" if created_new else "repaired",
            "created_paths": sorted(created_paths),
            "initial_commit": commit,
            "doctor": diagnosis,
            "next_steps": [
                "Open the Manager directory as a ChatGPT Work or Codex project.",
                "Continue the guided first run with a calibrated work map.",
                "Review relevant communication and work-source capabilities.",
                "Preview QMD registration of the Manager knowledge collection.",
                "Choose explicit roots for shallow project discovery.",
                "Classify candidates before creating Project Packs.",
                "Preview the global core guidance block before installing it.",
                "Add optional global routing only if the user wants a stable convention.",
                "Offer one quiet recurring check-in in the current Manager task.",
            ],
        }
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
