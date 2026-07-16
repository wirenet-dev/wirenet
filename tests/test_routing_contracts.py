from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts/routing"
JASON = CONTRACTS / "jason-liu-original.json"
WIRENET = CONTRACTS / "wirenet-manager-v0.2.json"
COMPARE = ROOT / "scripts/compare_routing_contracts.py"
SEED = ROOT / "plugins/manager/templates/manager"


def test_repository_root_contains_only_product_scaffold() -> None:
    removed_reference_roots = (
        ".codex",
        "archive",
        "experiments",
        "notes",
        "outputs",
        "people",
        "projects",
        "sources",
        "templates",
    )
    assert not [name for name in removed_reference_roots if (ROOT / name).exists()]


def test_current_product_surfaces_use_only_manager_terminology() -> None:
    historical_files = {
        ROOT / "docs/routing/jason-liu-original.md",
        ROOT / "contracts/routing/jason-liu-original.json",
        ROOT / "docs/upstream-reference.md",
    }
    roots = (
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "docs",
        ROOT / "contracts/routing/wirenet-manager-v0.2.json",
        ROOT / "plugins",
        ROOT / "scripts",
    )
    files: set[Path] = set()
    for path in roots:
        if path.is_file():
            files.add(path)
        elif path.is_dir():
            files.update(
                candidate
                for candidate in path.rglob("*")
                if candidate.is_file()
                and candidate.suffix in {".md", ".json", ".py", ".html"}
            )

    deprecated_term = "va" + "ult"
    private_user_path = re.compile("/" + "Users/" + r"[^/\s]+/")
    violations: list[str] = []
    for path in sorted(files - historical_files):
        content = path.read_text(encoding="utf-8")
        if deprecated_term in content.casefold() or private_user_path.search(content):
            violations.append(str(path.relative_to(ROOT)))
    assert violations == []


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
    wirenet = load(WIRENET)
    assert jason["provenance"]["commit"] == "df863768495aaf524a2bf9b5b25ef2622a2591a1"
    assert jason["provenance"]["ref"] == "upstream/main"
    assert wirenet["provenance"] == {
        "repository": "https://github.com/wirenet-dev/wirenet-manager.git",
        "ref": "main",
        "lifecycle": "versioned-with-repository",
        "capture_rule": (
            "The contract describes the distributed plugin and generated canonical Manager runtime."
        ),
    }

    for contract in (jason, wirenet):
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
        path.relative_to(SEED).as_posix() for path in SEED.rglob("*") if path.is_file()
    }
    assert actual_seed_paths == declared_seed_paths

    for entity in entities.values():
        for evidence in entity["evidence"]:
            local = ROOT / str(evidence).split("#", 1)[0]
            assert local.exists(), f"missing wirenet contract evidence: {evidence}"


def test_projects_index_is_the_canonical_collection_router() -> None:
    entities = by_id(load(WIRENET)["entities"])
    assert entities["projects-collection"]["path"] == "projects/"
    assert entities["projects-okf-index"]["path"] == "projects/index.md"
    assert entities["project-status"]["path"] == "projects/<slug>/README.md"

    index = (SEED / "projects/index.md").read_text(encoding="utf-8")
    assert not index.startswith("---\n")
    assert "Manager-native and externally bound Project Packs" in index
    assert "## Active Project Packs" in index
    assert not (SEED / "projects/README.md").exists()


def test_agents_files_remain_the_executable_routing_hierarchy() -> None:
    root_agents = (SEED / "AGENTS.md").read_text(encoding="utf-8")
    projects_agents = (SEED / "projects/AGENTS.md").read_text(encoding="utf-8")

    assert "## Read Order" in root_agents
    assert "projects/README.md" not in root_agents
    assert "projects/index.md" in root_agents
    assert (
        "The relevant Project or Experiment Pack's `README.md` and `AGENTS.md`"
        in root_agents
    )
    assert "## Minimum Contract" in projects_agents
    for filename in (
        "README.md",
        "AGENTS.md",
        "GOAL.md",
        "RESULT.md",
        "WORKLOG.md",
        "log.md",
    ):
        assert filename in projects_agents

    entities = by_id(load(WIRENET)["entities"])
    assert entities["root-agent-instructions"]["authority"] == "routing"
    assert entities["root-agent-instructions"]["kind"] == "runtime-instruction"
    assert entities["project-agent-instructions"]["authority"] == "local-routing"
    assert entities["project-agent-instructions"]["kind"] == "runtime-instruction"
    assert entities["projects-collection"]["authority"] == "project-collection"
    assert entities["projects-collection"]["kind"] == "knowledge-shelf"
    assert entities["projects-okf-index"]["authority"] == "navigation"
    assert "\ntype:" not in root_agents
    assert "\ntype:" not in projects_agents
    assert 'schema: "wirenet-runtime/v0.1"' in root_agents
    assert 'schema: "wirenet-runtime/v0.1"' in projects_agents
    assert entities["root-manager-overview"]["kind"] == "concept"
    assert 'type: "Manager Overview"' in (SEED / "README.md").read_text(
        encoding="utf-8"
    )


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
        "root-manager-overview",
        "project-log",
        "project-worklog",
        "projects-okf-index",
        "manager-okf-index",
        "local-bindings",
        "manager-metadata",
        "external-workspace",
        "viewer",
        "experiments-okf-index",
        "experiment-status",
        "experiment-agent-instructions",
        "experiment-result",
    } <= added_entities
    assert "root-human-guide" in set(report["entities"]["removed"])

    changed_entities = {
        row["id"]: set(row["fields"]) for row in report["entities"]["changed"]
    }
    assert "projects-collection" in changed_entities
    assert "project-goal" in changed_entities
    assert "presence" in changed_entities["project-goal"]
    assert "project-result" in changed_entities
    assert "presence" in changed_entities["project-result"]

    routes = by_id(load(WIRENET)["routes"])
    assert "technical-bootstrap" in routes
    assert "personal-onboarding" in routes
    assert "writing-voice-bootstrap" in routes
    assert "recurring-loop" in routes
    assert "onboarding" not in routes

    entities = by_id(load(WIRENET)["entities"])
    assert entities["personal-writing-skill"]["path"] == (
        "~/.agents/skills/write-like-me/"
    )
    assert "create_person_note.py" in " ".join(entities["person-note"]["evidence"])
    assert "relationship context" in str(entities["person-note"]["description"])
    assert "project-lifecycle.md" in " ".join(routes["project-create"]["evidence"])
    assert "person-context.md" in " ".join(routes["person-create"]["evidence"])
    assert "delegate untracked classification" in str(
        routes["cross-workspace-sync"]["approval"]
    )

    added_routes = set(report["routes"]["added"])
    assert {
        "cross-workspace-sync",
        "experiment-create",
        "experiment-promote",
        "packet-lifecycle-transition",
        "recurring-loop",
        "ultragoal-activation",
        "workspace-upgrade",
        "okf-navigation",
        "viewer-projection",
    } <= added_routes


def test_wirenet_contract_separates_workspace_runtime_and_okf_projection() -> None:
    contract = load(WIRENET)
    scope = contract["scope"]
    assert "canonical OKF bundle" in scope["okf"]
    assert "one canonical OKF bundle" in scope["okf"]
    assert (
        "every other in-scope Markdown file requires a non-empty type" in scope["okf"]
    )

    routes = by_id(contract["routes"])
    assert (
        "without interpreting runtime instructions as knowledge"
        in routes["okf-navigation"]["description"]
    )
    assert "AGENTS.md" in routes["viewer-projection"]["description"]
    assert routes["viewer-projection"]["writes"] == [
        "temporary single-file HTML projection"
    ]


def test_routing_contract_separates_read_only_and_approval_gated_routes() -> None:
    routes = by_id(load(WIRENET)["routes"])

    for identifier in ("discovery", "okf-navigation"):
        assert routes[identifier]["writes"] == []
        assert routes[identifier]["approval"] == "not-required-for-read"

    assert "explicit" in str(routes["project-create"]["approval"])
    assert "preview" in str(routes["project-state-routing"]["approval"])
    assert "explicit" in str(routes["workspace-upgrade"]["approval"])
    assert "clean local Git" in str(routes["workspace-upgrade"]["approval"])
    assert "preview" in str(routes["cross-workspace-sync"]["approval"])
    assert "explicit loop request" in str(routes["recurring-loop"]["approval"])
    assert routes["recurring-loop"]["writes"] == [
        "one current-task heartbeat automation",
        "optional loop or done task title",
    ]
    assert routes["viewer-projection"]["writes"] == [
        "temporary single-file HTML projection"
    ]
    assert (
        routes["viewer-projection"]["approval"]
        == "not-required-for-local-read-only-generation"
    )
