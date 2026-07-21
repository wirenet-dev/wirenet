#!/usr/bin/env python3
"""Preview or apply removal of redundant timestamp frontmatter fields.

Project and Experiment Pack concepts (README, GOAL, RESULT) and their
packet-level AGENTS.md sidecars used to carry `timestamp` and `last_edited`
alongside `created_at` and `updated_at`, always set to the same value. This
tool removes the redundant keys so `created_at` (set once) and `updated_at`
(bumped on change) remain the single source of truth. It is idempotent,
touches only files it recognizes as generator-produced, and never changes a
document's `schema` value.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from manager_doctor import inspect
from manager_model import frontmatter, remove_frontmatter_keys
from upgrade_manager import git_worktree_status, resolve_executable


CONCEPT_REDUNDANT_KEYS = {"timestamp", "last_edited"}
RUNTIME_REDUNDANT_KEYS = {"last_edited"}
CONCEPT_GLOBS = ("README.md", "GOAL.md", "RESULT.md")


def find_candidates(manager_dir: Path) -> list[tuple[Path, set[str]]]:
    candidates: list[tuple[Path, set[str]]] = []
    for collection in ("projects", "experiments"):
        root = manager_dir / collection
        if not root.is_dir():
            continue
        for packet in sorted(path for path in root.iterdir() if path.is_dir()):
            for name in CONCEPT_GLOBS:
                path = packet / name
                if not path.is_file():
                    continue
                metadata = frontmatter(path)
                if "created_at" not in metadata:
                    continue
                present = CONCEPT_REDUNDANT_KEYS & metadata.keys()
                if present:
                    candidates.append((path, present))
            agents = packet / "AGENTS.md"
            if agents.is_file():
                metadata = frontmatter(agents)
                if "created_at" not in metadata:
                    continue
                present = RUNTIME_REDUNDANT_KEYS & metadata.keys()
                if present:
                    candidates.append((agents, present))
    return candidates


def apply_tidy(manager_dir: Path, candidates: list[tuple[Path, set[str]]]) -> list[str]:
    changed: list[str] = []
    for path, keys in candidates:
        content = path.read_text(encoding="utf-8")
        updated = remove_frontmatter_keys(content, keys)
        if updated != content:
            path.write_text(updated, encoding="utf-8")
            changed.append(path.relative_to(manager_dir).as_posix())
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manager-dir", default="~/Manager")
    parser.add_argument(
        "--git-bin",
        default=os.environ.get("WIRENET_GIT_BIN"),
        help="Explicit Git executable, including a Codex-bundled fallback.",
    )
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    manager_dir = Path(args.manager_dir).expanduser().resolve(strict=False)
    git_bin = resolve_executable(args.git_bin, "git")
    result: dict[str, object] = {
        "ok": True,
        "dry_run": not args.apply,
        "manager_dir": str(manager_dir),
        "runtime": {"python": sys.executable, "git": git_bin},
    }

    if not manager_dir.is_dir() or not (manager_dir / ".wirenet/manager.json").is_file():
        result.update(
            {
                "ok": False,
                "error": "Manager metadata is missing; bootstrap or repair the workspace first",
            }
        )
        print(json.dumps(result, indent=2))
        return 2

    candidates = find_candidates(manager_dir)
    result["candidate_paths"] = [str(path) for path, _ in candidates]

    if not candidates:
        result["state"] = "clean"
        print(json.dumps(result, indent=2))
        return 0

    result["state"] = "tidy-available"
    if not args.apply:
        print(json.dumps(result, indent=2))
        return 0

    clean, detail = git_worktree_status(manager_dir, git_bin)
    if not clean:
        result.update({"ok": False, "state": "checkpoint-required", "error": detail})
        print(json.dumps(result, indent=2))
        return 2

    changed = apply_tidy(manager_dir, candidates)
    diagnosis = inspect(manager_dir)
    if diagnosis["ok"] is not True:
        result.update(
            {
                "ok": False,
                "dry_run": False,
                "state": "tidy-failed",
                "error": "Manager Doctor did not return ok=true after tidy",
                "doctor": diagnosis,
            }
        )
        print(json.dumps(result, indent=2))
        return 1

    result.update(
        {
            "dry_run": False,
            "state": "tidied",
            "changed_paths": changed,
            "doctor": diagnosis,
            "next_action": "review and commit the local Manager timestamp cleanup",
        }
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
