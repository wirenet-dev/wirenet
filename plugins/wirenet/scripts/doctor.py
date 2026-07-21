#!/usr/bin/env python3
"""wirenet Manager doctor: validate conventions, never content.

Read-only. Reports findings as proposals; exit code 1 only on structural
errors (missing root files, unreadable bindings, broken index links).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT_FILES = ["AGENTS.md", "README.md", "TODO.md", "projects/index.md"]
TODO_SECTIONS = ["## Now", "## Next", "## Waiting", "## Later", "## Someday"]
INDEX_GROUPS = ["## Active", "## Waiting / Blocked", "## Later", "## Ongoing", "## Archived"]
PACK_SIZE_LIMIT = 120
ORIENTATION_BUDGET = 250
STALE_DAYS = 90
PLUGIN_ROOT = Path(__file__).resolve().parents[1]


def default_manager_dir() -> Path:
    configured = os.environ.get("WIRENET_MANAGER_DIR")
    return Path(configured).expanduser() if configured else Path.home() / "Manager"


def line_count(path: Path) -> int:
    try:
        return len(path.read_text(encoding="utf-8").splitlines())
    except OSError:
        return 0


def last_commit_age_days(repo: Path, path: Path) -> float | None:
    result = subprocess.run(
        ["git", "-C", str(repo), "log", "-1", "--format=%ct", "--", str(path)],
        check=False, capture_output=True, text=True,
    )
    stamp = result.stdout.strip()
    if result.returncode != 0 or not stamp:
        return None
    return (time.time() - int(stamp)) / 86400


def check(manager: Path) -> tuple[list[dict], list[dict]]:
    errors: list[dict] = []
    findings: list[dict] = []

    for rel in ROOT_FILES:
        if not (manager / rel).is_file():
            errors.append({"check": "root-files", "detail": f"missing {rel}"})
    todo = manager / "TODO.md"
    if todo.is_file():
        text = todo.read_text(encoding="utf-8")
        missing = [s for s in TODO_SECTIONS if s not in text]
        if missing:
            findings.append({"check": "todo-sections", "detail": f"missing {', '.join(missing)}"})

    bindings_path = manager / ".wirenet" / "workspace-bindings.json"
    if bindings_path.is_file():
        try:
            data = json.loads(bindings_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append({"check": "bindings", "detail": f"unreadable: {error}"})
            data = None
        if isinstance(data, dict):
            version = data.get("schema_version", "")
            if version == "wirenet-bindings/v1":
                for slug, paths in (data.get("bindings") or {}).items():
                    for raw in paths:
                        if not Path(raw).expanduser().exists():
                            findings.append({"check": "bindings", "detail": f"{slug}: {raw} does not exist"})
            elif version.startswith("wirenet-workspace-bindings"):
                findings.append({"check": "bindings", "detail": "legacy v0.2 format; run the v0.5 migration"})
            else:
                errors.append({"check": "bindings", "detail": f"unknown schema_version {version!r}"})

    index = manager / "projects" / "index.md"
    listed: set[Path] = set()
    if index.is_file():
        text = index.read_text(encoding="utf-8")
        group = None
        for line in text.splitlines():
            if line.startswith("## "):
                group = line.strip()
            for target in re.findall(r"\]\(([^)]+)\)", line):
                if target.startswith("http"):
                    continue
                resolved = (index.parent / target).resolve()
                if not resolved.exists():
                    errors.append({"check": "index", "detail": f"broken link: {target}"})
                    continue
                pack = resolved.parent if resolved.name == "README.md" else resolved
                listed.add(pack)
                in_archive = "archive/" in target
                if group == "## Archived" and not in_archive:
                    findings.append({"check": "index", "detail": f"{target} listed Archived but not in archive/"})
                if group not in (None, "## Archived") and in_archive:
                    findings.append({"check": "index", "detail": f"{target} in archive/ but listed under {group}"})
        for container in ("projects", "areas"):
            base = manager / container
            if base.is_dir():
                for pack in base.iterdir():
                    if pack.is_dir() and (pack / "README.md").is_file() and pack.resolve() not in listed:
                        findings.append({"check": "index", "detail": f"{container}/{pack.name} has no index entry"})

    for container in ("projects", "areas", "experiments", "archive"):
        base = manager / container
        if not base.is_dir():
            continue
        for readme in base.glob("*/README.md"):
            count = line_count(readme)
            if count > PACK_SIZE_LIMIT:
                findings.append({"check": "pack-size", "detail": f"{readme.relative_to(manager)}: {count} lines (> {PACK_SIZE_LIMIT})"})
        for md in base.rglob("*.md"):
            if md.stat().st_size == 0:
                findings.append({"check": "placeholders", "detail": f"empty file {md.relative_to(manager)}"})

    if (manager / ".git").exists():
        base = manager / "projects"
        if base.is_dir():
            for pack in base.iterdir():
                if not pack.is_dir():
                    continue
                age = last_commit_age_days(manager, pack)
                if age is not None and age > STALE_DAYS:
                    findings.append({"check": "staleness", "detail": f"projects/{pack.name}: last change {int(age)}d ago — review, archive, or reaffirm (or reclassify as area)"})

    budget = sum(line_count(manager / rel) for rel in ROOT_FILES)
    largest = 0
    for container in ("projects", "areas"):
        base = manager / container
        if base.is_dir():
            for readme in base.glob("*/README.md"):
                largest = max(largest, line_count(readme))
    orientation = budget + largest
    if orientation > ORIENTATION_BUDGET:
        findings.append({"check": "orientation-budget", "detail": f"{orientation} lines (root files + largest pack) > {ORIENTATION_BUDGET}"})
    findings.append({"check": "orientation-budget-info", "detail": f"current orientation read: {orientation} lines"})
    return errors, findings


def check_updates() -> dict:
    manifest = json.loads((PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text())
    current = manifest["version"]
    url = "https://api.github.com/repos/wirenet-dev/wirenet/releases/latest"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            latest = json.load(response)
    except Exception as error:  # network optional by design
        return {"available": None, "current": current, "error": str(error)}
    tag = latest.get("tag_name", "").lstrip("v")
    notes = [line for line in (latest.get("body") or "").splitlines() if line.startswith("- ")][:3]
    return {
        "available": tag != current if tag else None,
        "current": current,
        "latest": tag,
        "notes": notes,
        "update_command": "claude: /plugin marketplace update wirenet · codex: codex plugin marketplace upgrade",
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manager-dir", type=Path, default=default_manager_dir())
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--check-updates", action="store_true")
    args = parser.parse_args(argv)

    manager = args.manager_dir.expanduser().resolve(strict=False)
    if not manager.is_dir():
        print(json.dumps({"ok": False, "error": f"no Manager at {manager}"}))
        return 1
    errors, findings = check(manager)
    result: dict = {"ok": not errors, "manager_dir": str(manager), "errors": errors, "findings": findings}
    if args.check_updates:
        result["updates"] = check_updates()
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"wirenet doctor — {manager}")
        for item in errors:
            print(f"  ERROR   {item['check']}: {item['detail']}")
        for item in findings:
            print(f"  finding {item['check']}: {item['detail']}")
        if not errors:
            print("  structure: healthy" if not findings else f"  structure: healthy, {len(findings)} finding(s) to review")
        if "updates" in result:
            print(f"  updates: {result['updates']}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
