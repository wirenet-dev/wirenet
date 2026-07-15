#!/usr/bin/env python3
"""Preview or apply a validated Project or Experiment Pack status transition."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from manager_model import (
    experiment_packet_for_id,
    frontmatter,
    iso_date,
    iso_timestamp,
    load_json,
    project_packet_for_id,
    render_experiments_index,
    render_projects_index,
    update_frontmatter,
    write_json,
)


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = PLUGIN_ROOT / "contracts/lifecycle-v0.2.json"


def resolve_packet(manager_dir: Path, kind: str, identity: str) -> Path | None:
    if kind == "project":
        packet = project_packet_for_id(manager_dir, identity)
        if packet:
            return packet
        candidate = manager_dir / "projects" / identity
    else:
        packet = experiment_packet_for_id(manager_dir, identity)
        if packet:
            return packet
        candidate = manager_dir / "experiments" / identity
    return candidate if (candidate / "README.md").is_file() else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=["project", "experiment"])
    parser.add_argument("identity", help="Stable ID or packet slug")
    parser.add_argument("--to", required=True, dest="target")
    parser.add_argument("--manager-dir", default="~/Manager")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    manager_dir = Path(args.manager_dir).expanduser().resolve(strict=False)
    contract = load_json(CONTRACT_PATH)
    policy = contract[args.kind]
    assert isinstance(policy, dict)
    allowed_statuses = policy.get("statuses", [])
    if args.target not in allowed_statuses:
        print(json.dumps({"ok": False, "error": f"unsupported target status: {args.target}"}, indent=2))
        return 2
    packet = resolve_packet(manager_dir, args.kind, args.identity)
    if not packet:
        print(json.dumps({"ok": False, "error": f"{args.kind} packet not found"}, indent=2))
        return 2
    readme = packet / "README.md"
    metadata = frontmatter(readme)
    current = metadata.get("status", "active")
    transitions = policy.get("transitions", {})
    assert isinstance(transitions, dict)
    allowed_targets = transitions.get(current, [])
    if args.target == current:
        changed = False
    elif args.target not in allowed_targets:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": f"invalid {args.kind} transition: {current} -> {args.target}",
                    "allowed": allowed_targets,
                },
                indent=2,
            )
        )
        return 2
    else:
        changed = True

    result = {
        "ok": True,
        "dry_run": not args.apply,
        "kind": args.kind,
        "packet": str(packet),
        "from": current,
        "to": args.target,
        "changed": changed,
    }
    if not args.apply or not changed:
        print(json.dumps(result, indent=2))
        return 0

    content = readme.read_text(encoding="utf-8")
    readme.write_text(
        update_frontmatter(
            content,
            {
                "status": args.target,
                "updated_at": iso_date(),
                "last_edited": iso_date(),
            },
        ),
        encoding="utf-8",
    )
    if args.kind == "project":
        (manager_dir / "projects/index.md").write_text(
            render_projects_index(manager_dir), encoding="utf-8"
        )
    else:
        (manager_dir / "experiments/index.md").write_text(
            render_experiments_index(manager_dir), encoding="utf-8"
        )
    manager_metadata_path = manager_dir / ".wirenet/manager.json"
    manager_metadata = load_json(manager_metadata_path)
    manager_metadata["updated_at"] = iso_timestamp()
    write_json(manager_metadata_path, manager_metadata)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
