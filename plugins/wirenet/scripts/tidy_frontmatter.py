#!/usr/bin/env python3
"""Preview or apply normalization of legacy Project Pack frontmatter.

Older Project and Experiment Pack concepts carried duplicate routing fields,
parallel name/summary aliases, an unused per-concept OKF profile, and legacy
timestamp aliases. This tool reduces recognized packet concepts to the current
portable contract while preserving producer-defined fields and document prose.
It is dry-run-first, idempotent, and never changes a document's schema value.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

from manager_doctor import inspect
from manager_model import (
    EXPERIMENT_PACK_SCHEMA,
    PROJECT_PACK_SCHEMA,
    RUNTIME_SCHEMA,
    frontmatter,
    yaml_string,
)
from upgrade_manager import git_worktree_status, resolve_executable


CONCEPT_REDUNDANT_KEYS = {
    "assembly_scope",
    "context_scope",
    "last_edited",
    "okf_profile",
    "scope",
    "timestamp",
}
RUNTIME_REDUNDANT_KEYS = {"last_edited"}
RESERVED_DOCUMENTS = {"AGENTS.md", "index.md", "log.md"}
PACKS = {
    "projects": (PROJECT_PACK_SCHEMA, "project_id"),
    "experiments": (EXPERIMENT_PACK_SCHEMA, "experiment_id"),
}
STATUS_TYPES = {"Project Status", "Experiment Status"}


def _frontmatter_lines(content: str) -> tuple[list[str], str]:
    if not content.startswith("---\n"):
        raise ValueError("document is missing YAML frontmatter")
    end = content.find("\n---\n", 4)
    if end < 0:
        raise ValueError("document has malformed YAML frontmatter")
    return content[4:end].splitlines(), content[end:]


def normalize_concept_frontmatter(
    content: str,
    metadata: dict[str, str],
    *,
    status_document: bool,
) -> str:
    """Remove legacy aliases while preserving unknown fields and their order."""
    lines, suffix = _frontmatter_lines(content)
    name = str(metadata.get("name") or "")
    has_title = bool(metadata.get("title"))
    has_description = "description" in metadata
    heading = re.search(r"(?m)^#\s+(.+?)\s*$", suffix)
    status_title = name or (heading.group(1).strip() if heading else "")
    normalized: list[str] = []

    for line in lines:
        if ":" not in line or line.startswith((" ", "-")):
            normalized.append(line)
            continue
        key, raw = line.split(":", 1)
        key = key.strip()
        if key in CONCEPT_REDUNDANT_KEYS:
            continue
        if key == "name":
            if not has_title:
                normalized.append(f"title: {yaml_string(name)}")
            continue
        if key == "title" and status_document and status_title:
            normalized.append(f"title: {yaml_string(status_title)}")
            continue
        if key == "summary":
            if not has_description:
                normalized.append(f"description:{raw}")
            continue
        normalized.append(line)

    return "---\n" + "\n".join(normalized) + suffix


def normalize_runtime_frontmatter(content: str) -> str:
    lines, suffix = _frontmatter_lines(content)
    normalized = [
        line
        for line in lines
        if not (
            ":" in line
            and not line.startswith((" ", "-"))
            and line.split(":", 1)[0].strip() in RUNTIME_REDUNDANT_KEYS
        )
    ]
    return "---\n" + "\n".join(normalized) + suffix


def find_candidates(manager_dir: Path) -> list[tuple[Path, bool]]:
    candidates: list[tuple[Path, bool]] = []
    for collection, (schema, identity_key) in PACKS.items():
        root = manager_dir / collection
        if not root.is_dir():
            continue
        for packet in sorted(path for path in root.iterdir() if path.is_dir()):
            identity = frontmatter(packet / "README.md").get(identity_key)
            if not identity:
                continue
            for path in sorted(packet.rglob("*.md")):
                metadata = frontmatter(path)
                if path.name == "AGENTS.md":
                    if (
                        metadata.get("schema") == RUNTIME_SCHEMA
                        and metadata.get(identity_key) == identity
                        and RUNTIME_REDUNDANT_KEYS & metadata.keys()
                    ):
                        candidates.append((path, True))
                    continue
                if path.name in RESERVED_DOCUMENTS:
                    continue
                if (
                    metadata.get("schema") != schema
                    or metadata.get(identity_key) != identity
                ):
                    continue
                legacy_keys = CONCEPT_REDUNDANT_KEYS | {"name", "summary"}
                if legacy_keys & metadata.keys():
                    candidates.append((path, False))
    return candidates


def apply_tidy(manager_dir: Path, candidates: list[tuple[Path, bool]]) -> list[str]:
    changed: list[str] = []
    for path, runtime in candidates:
        content = path.read_text(encoding="utf-8")
        if runtime:
            updated = normalize_runtime_frontmatter(content)
        else:
            metadata = frontmatter(path)
            updated = normalize_concept_frontmatter(
                content,
                metadata,
                status_document=metadata.get("type") in STATUS_TYPES,
            )
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

    if not manager_dir.is_dir() or not (
        manager_dir / ".wirenet/manager.json"
    ).is_file():
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

    result["state"] = "frontmatter-tidy-available"
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
                "state": "frontmatter-tidy-failed",
                "error": "Manager Doctor did not return ok=true after frontmatter tidy",
                "doctor": diagnosis,
            }
        )
        print(json.dumps(result, indent=2))
        return 1

    result.update(
        {
            "dry_run": False,
            "state": "frontmatter-tidied",
            "changed_paths": changed,
            "doctor": diagnosis,
            "next_action": "review and commit the local Manager frontmatter cleanup",
        }
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
