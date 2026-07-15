from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts/routing"
JASON = CONTRACTS / "jason-liu-original.json"
WIRENET = CONTRACTS / "wirenet-manager-v0.1.json"
COMPARE = ROOT / "scripts/compare_routing_contracts.py"
SEED = ROOT / "plugins/wirenet-manager/templates/manager"


def load_compare_module():
    spec = importlib.util.spec_from_file_location("compare_routing_contracts", COMPARE)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def by_id(rows: object) -> dict[str, dict[str, object]]:
    assert isinstance(rows, list)
    return {str(row["id"]): row for row in rows}


def test_frozen_routing_contracts_validate_and_have_evidence() -> None:
    module = load_compare_module()
    for path in (JASON, WIRENET):
        contract = module.load_contract(path)
        assert module.validate_contract(contract) == []

    jason = load(JASON)
    assert jason["snapshot"]["commit"] == "df863768495aaf524a2bf9b5b25ef2622a2591a1"
    assert jason["snapshot"]["ref"] == "upstream/main"

    for contract in (jason, load(WIRENET)):
        for row in [*contract["entities"], *contract["routes"]]:
            assert row["evidence"], row["id"]


def test_jason_contract_distinguishes_tree_presence_from_routing_semantics() -> None:
    entities = by_id(load(JASON)["entities"])

    assert entities["notes-collection"]["presence"] == "bootstrap-generated-directory"
    assert entities["notes-collection"]["authority"] == "scratch-state"
    assert entities["sources-collection"]["presence"] == "bootstrap-generated-directory"
    assert entities["sources-collection"]["authority"] == "retained-evidence"

    for identifier in ("outputs-collection", "archive-collection", "docs-collection"):
        assert entities[identifier]["presence"] == "seed-empty"
        assert entities[identifier]["authority"] == "none-defined"

    assert entities["project-goal"]["presence"] == "optional-manual"
    assert entities["project-result"]["presence"] == "optional-manual"


def test_wirenet_seed_paths_declared_by_contract_exist() -> None:
    contract = load(WIRENET)
    entities = by_id(contract["entities"])

    declared_seed_paths: set[str] = set()
    for entity in entities.values():
        path = str(entity["path"])
        presence = str(entity["presence"])
        if "seed" not in presence or "<" in path or path.startswith("installed "):
            continue
        declared_seed_paths.add(path)
        assert (SEED / path).exists(), f"missing declared seed entity: {path}"

    actual_seed_paths = {
        path.relative_to(SEED).as_posix()
        for path in SEED.rglob("*")
        if path.is_file()
    }
    assert actual_seed_paths == declared_seed_paths

    for entity in entities.values():
        for evidence in entity["evidence"]:
            local = ROOT / str(evidence).split("#", 1)[0]
            assert local.exists(), f"missing WireNet contract evidence: {evidence}"


def test_projects_index_is_additive_to_collection_router() -> None:
    entities = by_id(load(WIRENET)["entities"])
    assert entities["projects-collection"]["path"] == "projects/README.md"
    assert entities["projects-okf-index"]["path"] == "projects/index.md"
    assert entities["project-status"]["path"] == "projects/<slug>/README.md"

    index = (SEED / "projects/index.md").read_text(encoding="utf-8")
    router = (SEED / "projects/README.md").read_text(encoding="utf-8")
    assert not index.startswith("---\n")
    assert "progressive disclosure" in index
    assert "## Active Project Packs" in index
    assert "## Active Project Packs" in router
    assert "Jason-compatible collection guide" in router


def test_agents_files_remain_the_executable_routing_hierarchy() -> None:
    root_agents = (SEED / "AGENTS.md").read_text(encoding="utf-8")
    projects_agents = (SEED / "projects/AGENTS.md").read_text(encoding="utf-8")

    assert "## Read Order" in root_agents
    assert "projects/README.md" in root_agents
    assert "projects/index.md" in root_agents
    assert "The relevant Project Pack's `README.md` and `AGENTS.md`" in root_agents
    assert "## Minimum Contract" in projects_agents
    for filename in ("README.md", "AGENTS.md", "GOAL.md", "RESULT.md", "WORKLOG.md", "log.md"):
        assert filename in projects_agents

    entities = by_id(load(WIRENET)["entities"])
    assert entities["root-agent-instructions"]["authority"] == "routing"
    assert entities["project-agent-instructions"]["authority"] == "local-routing"
    assert entities["projects-collection"]["authority"] == "collection-guide"
    assert entities["projects-okf-index"]["authority"] == "navigation"


def test_contract_delta_exposes_wirenet_additions_and_changed_roles() -> None:
    result = subprocess.run(
        [sys.executable, str(COMPARE), "--json"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    report = json.loads(result.stdout)
    assert report["ok"] is True

    added_entities = set(report["entities"]["added"])
    assert {
        "project-log",
        "project-worklog",
        "projects-okf-index",
        "manager-okf-index",
        "local-bindings",
        "manager-metadata",
        "external-workspace",
        "viewer",
    } <= added_entities

    changed_entities = {row["id"]: set(row["fields"]) for row in report["entities"]["changed"]}
    assert "projects-collection" in changed_entities
    assert "project-goal" in changed_entities
    assert "presence" in changed_entities["project-goal"]
    assert "project-result" in changed_entities
    assert "presence" in changed_entities["project-result"]

    added_routes = set(report["routes"]["added"])
    assert {"cross-workspace-sync", "okf-navigation", "viewer-projection"} <= added_routes


def test_wirenet_contract_keeps_okf_as_overlay_not_instruction_replacement() -> None:
    contract = load(WIRENET)
    scope = contract["scope"]
    assert "OKF-compatible" in scope["okf"]
    assert "full-bundle OKF conformance is not yet claimed" in scope["okf"]

    routes = by_id(contract["routes"])
    assert "do not replace canonical prose or instructions" in routes["okf-navigation"]["description"]
    assert routes["viewer-projection"]["writes"] == ["temporary single-file HTML projection"]


def test_routing_contract_separates_read_only_and_approval_gated_routes() -> None:
    routes = by_id(load(WIRENET)["routes"])

    for identifier in ("discovery", "okf-navigation"):
        assert routes[identifier]["writes"] == []
        assert routes[identifier]["approval"] == "not-required-for-read"

    assert "explicit" in str(routes["project-create"]["approval"])
    assert "preview" in str(routes["project-state-routing"]["approval"])
    assert "preview" in str(routes["cross-workspace-sync"]["approval"])
    assert routes["viewer-projection"]["writes"] == ["temporary single-file HTML projection"]
    assert routes["viewer-projection"]["approval"] == "not-required-for-local-read-only-generation"
