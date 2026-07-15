#!/usr/bin/env python3
"""Detect QMD and register a WireNet Manager knowledge collection safely."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path


QMD_PACKAGE = "@tobilu/qmd@2.5.3"
DEFAULT_COLLECTION = "manager"
REQUIRED_IGNORE = {"**/AGENTS.md", "outputs/**"}
KNOWLEDGE_PATTERN = (
    "{README.md,TODO.md,index.md,log.md,"
    "agent/**/!(*AGENTS).md,archive/**/!(*AGENTS).md,"
    "docs/**/!(*AGENTS).md,experiments/**/!(*AGENTS).md,"
    "notes/**/!(*AGENTS).md,people/**/!(*AGENTS).md,"
    "projects/**/!(*AGENTS).md,sources/**/!(*AGENTS).md}"
)
COLLECTION_CONTEXT = (
    "WireNet Manager durable work knowledge. Prefer current Project and "
    "Experiment Pack status, goals, results, tasks, people, notes, docs, "
    "sources, indexes, and sparse logs. Runtime AGENTS instructions and "
    "device-local outputs are outside this collection."
)


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )


def compact_error(process: subprocess.CompletedProcess[str]) -> str:
    message = (process.stderr or process.stdout).strip()
    return message[-2000:] if message else f"command exited {process.returncode}"


def resolve_command(explicit: str | None, name: str) -> str | None:
    if explicit:
        path = Path(explicit).expanduser().resolve(strict=False)
        return str(path) if path.is_file() and os.access(path, os.X_OK) else None
    return shutil.which(name)


def inspect_qmd(qmd: str | None) -> dict[str, object]:
    if not qmd:
        return {"state": "missing", "executable": None, "version": None}
    version = run([qmd, "--version"])
    if version.returncode != 0:
        return {
            "state": "unhealthy",
            "executable": qmd,
            "version": None,
            "error": compact_error(version),
        }
    doctor = run([qmd, "doctor"])
    if doctor.returncode != 0:
        return {
            "state": "unhealthy",
            "executable": qmd,
            "version": version.stdout.strip(),
            "error": compact_error(doctor),
        }
    return {
        "state": "ready",
        "executable": qmd,
        "version": version.stdout.strip(),
    }


def installed_qmd_from_npm(npm: str) -> str | None:
    prefix = run([npm, "prefix", "-g"])
    if prefix.returncode != 0:
        return None
    root = Path(prefix.stdout.strip()).expanduser().resolve(strict=False)
    candidates = (
        root / "bin/qmd",
        root / "qmd",
        root / "qmd.cmd",
    )
    return next(
        (
            str(path)
            for path in candidates
            if path.is_file() and os.access(path, os.X_OK)
        ),
        None,
    )


def install_qmd(npm: str) -> tuple[str | None, str | None]:
    installed = run([npm, "install", "-g", QMD_PACKAGE])
    if installed.returncode != 0:
        return None, compact_error(installed)
    return installed_qmd_from_npm(npm) or shutil.which("qmd"), None


def parse_collection(output: str) -> dict[str, str] | None:
    path_match = re.search(r"(?m)^\s*Path:\s+(.+?)\s*$", output)
    pattern_match = re.search(r"(?m)^\s*Pattern:\s+(.+?)\s*$", output)
    if not path_match or not pattern_match:
        return None
    return {
        "path": path_match.group(1).strip(),
        "pattern": pattern_match.group(1).strip(),
    }


def inspect_collection(qmd: str, name: str) -> dict[str, object]:
    shown = run([qmd, "collection", "show", name])
    if shown.returncode != 0:
        message = compact_error(shown)
        if "not found" in message.lower():
            return {"state": "missing", "name": name}
        return {"state": "error", "name": name, "error": message}
    parsed = parse_collection(shown.stdout)
    if not parsed:
        return {
            "state": "error",
            "name": name,
            "error": "could not parse qmd collection details",
        }
    details: dict[str, object] = {"state": "present", "name": name, **parsed}
    listed = run([qmd, "collection", "list"])
    if listed.returncode == 0:
        block_match = re.search(
            rf"(?ms)^\s*{re.escape(name)}\s+\(qmd://{re.escape(name)}/\).*?(?=\n\s*\n|\Z)",
            listed.stdout,
        )
        if block_match:
            ignore_match = re.search(
                r"(?m)^\s*Ignore:\s+(.+?)\s*$", block_match.group(0)
            )
            if ignore_match:
                details["ignore"] = [
                    item.strip()
                    for item in ignore_match.group(1).split(",")
                    if item.strip()
                ]
    return details


def has_knowledge_boundary(collection: dict[str, object]) -> bool:
    if collection.get("pattern") == KNOWLEDGE_PATTERN:
        return True
    ignore = {
        str(item) for item in collection.get("ignore", []) if isinstance(item, str)
    }
    return collection.get("pattern") == "**/*.md" and REQUIRED_IGNORE <= ignore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manager-dir", default="~/Manager")
    parser.add_argument("--collection-name", default=DEFAULT_COLLECTION)
    parser.add_argument("--qmd-bin")
    parser.add_argument("--npm-bin")
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--embed", action="store_true")
    parser.add_argument("--apply", action="store_true")
    return parser.parse_args()


def print_result(result: dict[str, object], code: int = 0) -> int:
    print(json.dumps(result, indent=2))
    return code


def main() -> int:
    args = parse_args()
    manager_dir = Path(args.manager_dir).expanduser().resolve(strict=False)
    collection_name = args.collection_name.strip()
    result: dict[str, object] = {
        "ok": True,
        "dry_run": not args.apply,
        "manager_dir": str(manager_dir),
        "collection_name": collection_name,
        "knowledge_pattern": KNOWLEDGE_PATTERN,
        "actions": [],
    }

    if not manager_dir.is_dir():
        result.update(
            {
                "ok": False,
                "state": "manager-missing",
                "error": "Manager directory does not exist",
            }
        )
        return print_result(result, 2)
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", collection_name):
        result.update(
            {
                "ok": False,
                "state": "invalid-collection-name",
                "error": "collection name must use lowercase letters, digits, _ or -",
            }
        )
        return print_result(result, 2)

    qmd = resolve_command(args.qmd_bin, "qmd")
    qmd_status = inspect_qmd(qmd)
    result["qmd"] = qmd_status

    if qmd_status["state"] != "ready":
        result["actions"] = [
            f"install or repair QMD with: npm install -g {QMD_PACKAGE}",
            f"register {manager_dir} as qmd://{collection_name}/",
            "attach WireNet Manager retrieval context",
        ]
        if args.embed:
            result["actions"].append("embed the Manager collection")
        if not args.apply:
            result.update(
                {
                    "state": f"qmd-{qmd_status['state']}",
                    "install_required": True,
                    "next_action": "obtain approval, then rerun with --install --apply",
                }
            )
            return print_result(result)
        if not args.install:
            result.update(
                {
                    "ok": False,
                    "state": f"qmd-{qmd_status['state']}",
                    "install_required": True,
                    "next_action": "rerun with --install only after explicit approval",
                }
            )
            return print_result(result, 2)
        npm = resolve_command(args.npm_bin, "npm")
        if not npm:
            result.update(
                {
                    "ok": False,
                    "state": "npm-missing",
                    "error": "npm is required to install QMD",
                }
            )
            return print_result(result, 2)
        qmd, install_error = install_qmd(npm)
        if install_error:
            result.update(
                {
                    "ok": False,
                    "state": "qmd-install-failed",
                    "error": install_error,
                }
            )
            return print_result(result, 1)
        qmd_status = inspect_qmd(qmd)
        result["qmd"] = qmd_status
        if qmd_status["state"] != "ready":
            result.update(
                {
                    "ok": False,
                    "state": "qmd-unhealthy-after-install",
                    "error": qmd_status.get("error"),
                }
            )
            return print_result(result, 1)

    assert qmd is not None
    collection = inspect_collection(qmd, collection_name)
    result["collection"] = collection
    if collection["state"] == "error":
        result.update(
            {"ok": False, "state": "collection-inspection-failed"}
        )
        return print_result(result, 1)
    if collection["state"] == "present":
        configured_path = Path(str(collection["path"])).expanduser().resolve(
            strict=False
        )
        if configured_path != manager_dir:
            result.update(
                {
                    "ok": False,
                    "state": "collection-name-conflict",
                    "error": (
                        f"qmd://{collection_name}/ already points to "
                        f"{configured_path}"
                    ),
                    "next_action": "choose another --collection-name; do not overwrite the existing collection",
                }
            )
            return print_result(result, 2)

    actions = []
    if collection["state"] == "missing":
        actions.append(
            f"register {manager_dir} as qmd://{collection_name}/ with the Manager knowledge mask"
        )
    custom_pattern = (
        collection["state"] == "present"
        and not has_knowledge_boundary(collection)
    )
    if custom_pattern:
        result["warning"] = (
            "the existing collection uses a custom pattern; it was preserved. "
            "Verify separately that runtime AGENTS.md and outputs are excluded."
        )
    actions.append("attach or refresh WireNet Manager retrieval context")
    if args.embed:
        actions.append("embed the Manager collection")
    result["actions"] = actions

    if not args.apply:
        result.update(
            {
                "state": "collection-missing"
                if collection["state"] == "missing"
                else "ready-custom"
                if custom_pattern
                else "ready",
                "next_action": "review the plan, then rerun with --apply",
            }
        )
        return print_result(result)

    if collection["state"] == "missing":
        added = run(
            [
                qmd,
                "collection",
                "add",
                str(manager_dir),
                "--name",
                collection_name,
                "--mask",
                KNOWLEDGE_PATTERN,
            ]
        )
        if added.returncode != 0:
            result.update(
                {
                    "ok": False,
                    "state": "collection-create-failed",
                    "error": compact_error(added),
                }
            )
            return print_result(result, 1)

    context = run(
        [
            qmd,
            "context",
            "add",
            f"qmd://{collection_name}",
            COLLECTION_CONTEXT,
        ]
    )
    if context.returncode != 0:
        result.update(
            {
                "ok": False,
                "state": "context-update-failed",
                "error": compact_error(context),
            }
        )
        return print_result(result, 1)

    if args.embed:
        embedded = run([qmd, "embed", "-c", collection_name])
        if embedded.returncode != 0:
            result.update(
                {
                    "ok": False,
                    "state": "embedding-failed",
                    "error": compact_error(embedded),
                }
            )
            return print_result(result, 1)

    final_qmd = inspect_qmd(qmd)
    final_collection = inspect_collection(qmd, collection_name)
    final_custom_pattern = (
        final_collection["state"] == "present"
        and not has_knowledge_boundary(final_collection)
    )
    result.update(
        {
            "ok": final_qmd["state"] == "ready"
            and final_collection["state"] == "present",
            "dry_run": False,
            "state": "ready-custom" if final_custom_pattern else "ready",
            "qmd": final_qmd,
            "collection": final_collection,
            "embedded": args.embed,
            "next_action": None
            if args.embed
            else "optionally rerun with --embed to add semantic retrieval",
        }
    )
    return print_result(result, 0 if result["ok"] else 1)


if __name__ == "__main__":
    raise SystemExit(main())
