#!/usr/bin/env python3
"""Validate and compare two frozen workspace-routing contracts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


CONTRACT_VERSIONS = {
    "wirenet-routing-contract/v0.1",
    "wirenet-routing-contract/v0.2",
}
ENTITY_FIELDS = {
    "id",
    "path",
    "kind",
    "presence",
    "authority",
    "audience",
    "description",
    "produced_by",
    "consumed_by",
    "evidence",
}
ROUTE_FIELDS = {
    "id",
    "trigger",
    "reads",
    "writes",
    "approval",
    "description",
    "evidence",
}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def load_contract(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read routing contract {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"routing contract must be a JSON object: {path}")
    return value


def _validate_rows(
    rows: object,
    *,
    row_name: str,
    fields: set[str],
) -> list[str]:
    errors: list[str] = []
    if not isinstance(rows, list):
        return [f"{row_name} must be a list"]
    seen: set[str] = set()
    for index, row in enumerate(rows):
        prefix = f"{row_name}[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = fields - set(row)
        if missing:
            errors.append(f"{prefix} is missing fields: {sorted(missing)}")
        identifier = row.get("id")
        if not isinstance(identifier, str) or not identifier:
            errors.append(f"{prefix}.id must be a non-empty string")
        elif identifier in seen:
            errors.append(f"duplicate {row_name} id: {identifier}")
        else:
            seen.add(identifier)
        for field in {"produced_by", "consumed_by", "evidence", "reads", "writes"} & fields:
            value = row.get(field)
            if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                errors.append(f"{prefix}.{field} must be a list of strings")
        evidence = row.get("evidence")
        if isinstance(evidence, list) and not evidence:
            errors.append(f"{prefix}.evidence must not be empty")
    return errors


def validate_contract(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if contract.get("contract_version") not in CONTRACT_VERSIONS:
        errors.append(f"contract_version must be one of {sorted(CONTRACT_VERSIONS)!r}")
    for key in ("system_id", "title"):
        if not isinstance(contract.get(key), str) or not contract[key]:
            errors.append(f"{key} must be a non-empty string")
    for key in ("provenance", "scope"):
        if not isinstance(contract.get(key), dict):
            errors.append(f"{key} must be an object")
    provenance = contract.get("provenance", {})
    if isinstance(provenance, dict):
        commit = provenance.get("commit")
        if commit is not None and (
            not isinstance(commit, str) or not SHA_RE.fullmatch(commit)
        ):
            errors.append("provenance.commit must be a 40-character Git SHA when present")
    errors.extend(_validate_rows(contract.get("entities"), row_name="entities", fields=ENTITY_FIELDS))
    errors.extend(_validate_rows(contract.get("routes"), row_name="routes", fields=ROUTE_FIELDS))
    ambiguities = contract.get("known_ambiguities")
    if not isinstance(ambiguities, list) or not all(isinstance(item, str) for item in ambiguities):
        errors.append("known_ambiguities must be a list of strings")
    return errors


def _row_delta(before: list[dict[str, Any]], after: list[dict[str, Any]]) -> dict[str, Any]:
    old = {row["id"]: row for row in before}
    new = {row["id"]: row for row in after}
    shared = sorted(old.keys() & new.keys())
    changed: list[dict[str, Any]] = []
    unchanged: list[str] = []
    for identifier in shared:
        fields = sorted(
            key
            for key in old[identifier].keys() | new[identifier].keys()
            if key != "evidence" and old[identifier].get(key) != new[identifier].get(key)
        )
        if fields:
            changed.append({"id": identifier, "fields": fields})
        else:
            unchanged.append(identifier)
    return {
        "added": sorted(new.keys() - old.keys()),
        "removed": sorted(old.keys() - new.keys()),
        "changed": changed,
        "unchanged": unchanged,
    }


def compare_contracts(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    return {
        "contract_version": after.get("contract_version"),
        "before": before["system_id"],
        "after": after["system_id"],
        "entities": _row_delta(before["entities"], after["entities"]),
        "routes": _row_delta(before["routes"], after["routes"]),
        "after_known_ambiguities": after["known_ambiguities"],
    }


def render_human(report: dict[str, Any]) -> str:
    lines = [f"Routing comparison: {report['before']} -> {report['after']}"]
    for section in ("entities", "routes"):
        delta = report[section]
        lines.append(f"\n{section.title()}:")
        for label in ("added", "removed", "unchanged"):
            values = delta[label]
            lines.append(f"- {label}: {', '.join(values) if values else 'none'}")
        if delta["changed"]:
            lines.append("- changed:")
            for item in delta["changed"]:
                lines.append(f"  - {item['id']}: {', '.join(item['fields'])}")
        else:
            lines.append("- changed: none")
    lines.append("\nOpen WireNet ambiguities:")
    lines.extend(f"- {item}" for item in report["after_known_ambiguities"])
    return "\n".join(lines)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "before",
        nargs="?",
        default=str(root / "contracts/routing/jason-liu-original.json"),
    )
    parser.add_argument(
        "after",
        nargs="?",
        default=str(root / "contracts/routing/wirenet-manager-v0.2.json"),
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    before = load_contract(Path(args.before))
    after = load_contract(Path(args.after))
    validation = {
        str(args.before): validate_contract(before),
        str(args.after): validate_contract(after),
    }
    errors = [f"{path}: {error}" for path, items in validation.items() for error in items]
    if errors:
        print(json.dumps({"ok": False, "errors": errors}, indent=2) if args.json else "\n".join(errors))
        return 1

    report = compare_contracts(before, after)
    if args.json:
        print(json.dumps({"ok": True, **report}, indent=2))
    else:
        print(render_human(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
