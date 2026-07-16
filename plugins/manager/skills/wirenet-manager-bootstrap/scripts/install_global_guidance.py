#!/usr/bin/env python3
"""Preview or install WireNet Manager blocks in global Codex instructions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CORE_START = "<!-- wirenet-manager:core:start -->"
CORE_END = "<!-- wirenet-manager:core:end -->"
ROUTING_START = "<!-- wirenet-manager:routing:start -->"
ROUTING_END = "<!-- wirenet-manager:routing:end -->"

CORE_BLOCK = f"""{CORE_START}
## WireNet Manager

When `$wirenet-manager-sync` is installed and enabled, use it before the final
response in a project task only when a future task would otherwise misunderstand
durable goals, status, ownership, people, blockers, decisions, deadlines,
results, canonical sources, or next steps. Let the skill choose the canonical
Project Pack, Experiment Pack, or Manager shelf; the user should not need to
route ordinary context manually. Do not update the Manager for routine edits,
commands, or transient trials. If the workspace is untracked but appears
durable, ask once whether it is a project, bounded experiment, or ignored
folder. Preview packet changes and obtain approval before writing unless the
user already approved that exact update. If the skill is unavailable or disabled, do nothing
and do not block the user's task. Never copy raw media,
source dumps, secrets, or generated files into canonical Manager knowledge;
keep transient outputs local.
{CORE_END}"""


def routing_block(rules: list[str]) -> str:
    bullets = "\n".join(f"- {rule}" for rule in rules)
    return f"""{ROUTING_START}
## Workspace Routing

{bullets}
{ROUTING_END}"""


def validate_pair(existing: str, start: str, end: str) -> bool:
    starts = existing.count(start)
    ends = existing.count(end)
    if starts != ends or starts > 1:
        raise ValueError(f"managed block markers {start!r} and {end!r} are malformed")
    return starts == 1


def replace_managed(existing: str, start: str, end: str, block: str) -> str:
    if start in existing:
        before, remainder = existing.split(start, 1)
        _, after = remainder.split(end, 1)
        return before + block + after
    if not existing.strip():
        return block + "\n"
    return existing.rstrip() + "\n\n" + block + "\n"


def remove_managed(existing: str, start: str, end: str) -> str:
    if start not in existing:
        return existing
    before, remainder = existing.split(start, 1)
    _, after = remainder.split(end, 1)
    before = before.rstrip()
    after = after.lstrip("\n")
    if before and after:
        return before + "\n\n" + after
    if before:
        return before + "\n"
    return after


def normalize_rules(raw_rules: list[str]) -> list[str]:
    rules: list[str] = []
    for raw_rule in raw_rules:
        rule = raw_rule.strip()
        if rule.startswith("- "):
            rule = rule[2:].strip()
        if not rule:
            raise ValueError("routing rules must not be empty")
        if "\n" in rule or "\r" in rule:
            raise ValueError("each routing rule must be one line")
        if "<!-- wirenet-manager:" in rule:
            raise ValueError("routing rules must not contain managed block markers")
        rules.append(rule)
    return rules


def replace_blocks(
    existing: str,
    *,
    routing_rules: list[str] | None = None,
    clear_routing: bool = False,
) -> tuple[str, str | None, str]:
    validate_pair(existing, CORE_START, CORE_END)
    has_routing = validate_pair(existing, ROUTING_START, ROUTING_END)

    updated = replace_managed(existing, CORE_START, CORE_END, CORE_BLOCK)

    rendered_routing: str | None = None
    action = "preserved" if has_routing else "absent"
    if routing_rules is not None:
        normalized = normalize_rules(routing_rules)
        rendered_routing = routing_block(normalized)
        updated = replace_managed(
            updated,
            ROUTING_START,
            ROUTING_END,
            rendered_routing,
        )
        action = "updated" if has_routing else "installed"
    elif clear_routing:
        updated = remove_managed(updated, ROUTING_START, ROUTING_END)
        action = "removed" if has_routing else "absent"

    return updated, rendered_routing, action


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents-file", default="~/.codex/AGENTS.md")
    routing = parser.add_mutually_exclusive_group()
    routing.add_argument(
        "--routing-rule",
        action="append",
        help="Install or replace the optional routing block; repeat for each one-line rule.",
    )
    routing.add_argument(
        "--clear-routing",
        action="store_true",
        help="Remove only the optional WireNet Manager routing block.",
    )
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    path = Path(args.agents_file).expanduser().resolve(strict=False)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    try:
        updated, rendered_routing, routing_action = replace_blocks(
            existing,
            routing_rules=args.routing_rule,
            clear_routing=args.clear_routing,
        )
    except ValueError as error:
        print(json.dumps({"ok": False, "agents_file": str(path), "error": str(error)}, indent=2))
        return 2

    changed = updated != existing
    result = {
        "ok": True,
        "dry_run": not args.apply,
        "agents_file": str(path),
        "changed": changed,
        "core_managed_block": CORE_BLOCK,
        "routing_managed_block": rendered_routing,
        "routing_action": routing_action,
    }
    if args.apply and changed:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(updated, encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
