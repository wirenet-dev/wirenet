#!/usr/bin/env python3
"""Preview, create, or conservatively repair a wirenet Manager v0.2."""

from __future__ import annotations

import argparse
import json
import os
import re
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


def normalize_content_language(value: str) -> str:
    """Validate and normalize a compact BCP 47-style language tag."""
    candidate = value.strip().replace("_", "-")
    if not re.fullmatch(r"[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*", candidate):
        raise ValueError(
            "content language must be a BCP 47-style tag such as en, de, or en-US"
        )
    parts = candidate.split("-")
    normalized = [parts[0].lower()]
    for part in parts[1:]:
        normalized.append(part.upper() if len(part) == 2 and part.isalpha() else part)
    return "-".join(normalized)


def set_content_language(readme: Path, language: str) -> None:
    """Set portable content language policy in the Manager overview."""
    content = readme.read_text(encoding="utf-8")
    replacement = f'content_language: "{language}"'
    if re.search(r"(?m)^content_language:\s*.+$", content):
        updated = re.sub(
            r"(?m)^content_language:\s*.+$", replacement, content, count=1
        )
    elif content.startswith("---\n"):
        closing = content.find("\n---\n", 4)
        if closing < 0:
            raise ValueError("Manager README.md has invalid YAML frontmatter")
        updated = content[:closing] + f"\n{replacement}" + content[closing:]
    else:
        raise ValueError("Manager README.md is missing YAML frontmatter")
    readme.write_text(updated, encoding="utf-8")


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


def resolve_executable(explicit: str | None, name: str) -> str | None:
    if explicit:
        candidate = Path(explicit).expanduser().resolve(strict=False)
        return str(candidate) if candidate.is_file() and os.access(candidate, os.X_OK) else None
    return shutil.which(name)


def initialize_git(manager_dir: Path, git_bin: str) -> str:
    try:
        run([git_bin, "init", "-b", "main"], cwd=manager_dir)
    except subprocess.CalledProcessError:
        run([git_bin, "init"], cwd=manager_dir)
        run([git_bin, "branch", "-M", "main"], cwd=manager_dir)

    if not run(
        [git_bin, "config", "user.name"], cwd=manager_dir, check=False
    ).stdout.strip():
        run(
            [git_bin, "config", "user.name", "wirenet Manager"], cwd=manager_dir
        )
    if not run(
        [git_bin, "config", "user.email"], cwd=manager_dir, check=False
    ).stdout.strip():
        run(
            [git_bin, "config", "user.email", "manager@localhost.invalid"],
            cwd=manager_dir,
        )

    run([git_bin, "add", "."], cwd=manager_dir)
    run(
        [
            git_bin,
            "-c",
            "commit.gpgsign=false",
            "commit",
            "-m",
            "chore(manager): bootstrap local workspace",
        ],
        cwd=manager_dir,
    )
    return run([git_bin, "rev-parse", "HEAD"], cwd=manager_dir).stdout.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manager-dir", default="~/Manager")
    parser.add_argument("--template-dir", default=str(DEFAULT_TEMPLATE))
    parser.add_argument(
        "--content-language",
        default="en",
        help=(
            "Language for human-readable Manager content, using a BCP 47-style "
            "tag. Stable file names, schemas, metadata keys, and enum values remain English."
        ),
    )
    parser.add_argument("--repair", action="store_true")
    parser.add_argument(
        "--git-bin",
        default=os.environ.get("WIRENET_GIT_BIN"),
        help="Explicit Git executable, including a Codex-bundled fallback.",
    )
    parser.add_argument("--apply", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        content_language = normalize_content_language(args.content_language)
    except ValueError as error:
        print(json.dumps({"ok": False, "error": str(error)}, indent=2))
        return 2
    manager_dir = Path(args.manager_dir).expanduser().resolve(strict=False)
    template_dir = Path(args.template_dir).expanduser().resolve(strict=False)
    git_bin = resolve_executable(args.git_bin, "git")
    exists = manager_dir.exists()
    result: dict[str, object] = {
        "ok": True,
        "dry_run": not args.apply,
        "manager_dir": str(manager_dir),
        "template_dir": str(template_dir),
        "state": "existing" if exists else "new",
        "content_language": content_language,
        "runtime": {"python": sys.executable, "git": git_bin},
        "actions": [],
    }

    if not git_bin:
        result.update(
            {
                "ok": False,
                "state": "runtime-missing",
                "error": "Git is unavailable",
                "next_action": (
                    "load the Codex workspace dependencies or provide --git-bin; "
                    "no Manager files were written"
                ),
            }
        )
        print(json.dumps(result, indent=2))
        return 2

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
        upgrade = plan_upgrade(manager_dir, git_bin=git_bin)
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
            f"set human-readable Manager content language to {content_language}",
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
        if created_new or "README.md" in created_paths:
            set_content_language(manager_dir / "README.md", content_language)
        metadata_path = manager_dir / ".wirenet/manager.json"
        if not metadata_path.exists():
            write_json(metadata_path, manager_metadata())
            created_paths.append(".wirenet/manager.json")

        commit = initialize_git(manager_dir, git_bin) if created_new else None
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
                "Preview QMD registration of the Manager knowledge collection.",
                "Continue with $manager-setup for the personal first meeting.",
            ],
        }
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
