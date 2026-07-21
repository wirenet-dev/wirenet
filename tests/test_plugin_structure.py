"""Structure tests: manifests, skills, seed, and retired surfaces."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "wirenet"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{path} missing frontmatter"
    raw = text.split("---", 2)[1]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if line.strip() and not line[0].isspace():
            key, _, value = line.partition(":")
            data[key.strip()] = value.strip()
    return data


def test_manifests_exist_and_match() -> None:
    claude = read_json(PLUGIN / ".claude-plugin" / "plugin.json")
    codex = read_json(PLUGIN / ".codex-plugin" / "plugin.json")
    assert claude["name"] == codex["name"] == "wirenet"
    assert claude["version"] == codex["version"]
    assert codex["skills"] == "./skills/"
    assert codex["interface"]["displayName"] == "wirenet"


def test_marketplaces_list_single_wirenet_plugin() -> None:
    claude = read_json(ROOT / ".claude-plugin" / "marketplace.json")
    assert [p["name"] for p in claude["plugins"]] == ["wirenet"]
    assert (ROOT / claude["plugins"][0]["source"]).is_dir()
    codex = read_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    assert [p["name"] for p in codex["plugins"]] == ["wirenet"]
    assert (ROOT / codex["plugins"][0]["source"]["path"]).is_dir()


def test_skills_have_frontmatter_and_references_resolve() -> None:
    skills = sorted(p.name for p in (PLUGIN / "skills").iterdir() if p.is_dir())
    assert skills == ["manager", "manager-setup"]
    for skill in skills:
        md = PLUGIN / "skills" / skill / "SKILL.md"
        data = frontmatter(md)
        assert data["name"] == skill
        assert len(data["description"]) > 40
        for ref in set(re.findall(r"references/[a-z0-9-]+\.md", md.read_text())):
            assert (md.parent / ref).is_file(), f"{skill}: missing {ref}"


def test_seed_is_complete_and_conventional() -> None:
    seed = PLUGIN / "templates" / "manager"
    for rel in [
        "AGENTS.md", "README.md", "TODO.md", "agent/USER_CONTEXT.md",
        "projects/index.md", ".wirenet/workspace-bindings.json", ".gitignore",
    ]:
        assert (seed / rel).is_file(), rel
    agents = (seed / "AGENTS.md").read_text(encoding="utf-8")
    assert not agents.startswith("---"), "personal core must not require frontmatter"
    for heading in [
        "## Start Here", "## What Lives Where", "## Keeping This Current",
        "## Lifecycle", "## Safety", "## Collaboration",
    ]:
        assert heading in agents, heading
    todo = (seed / "TODO.md").read_text(encoding="utf-8")
    for section in ["## Now", "## Next", "## Waiting", "## Later", "## Someday"]:
        assert section in todo, section
    index = (seed / "projects" / "index.md").read_text(encoding="utf-8")
    for group in ["## Active", "## Waiting / Blocked", "## Later", "## Ongoing", "## Archived"]:
        assert group in index, group
    bindings = read_json(seed / ".wirenet" / "workspace-bindings.json")
    assert bindings == {"schema_version": "wirenet-bindings/v1", "bindings": {}, "ignored": []}
    assert not (seed / "index.md").exists()
    assert not (seed / "projects" / "AGENTS.md").exists()


def test_retired_surfaces_are_gone() -> None:
    assert not (PLUGIN / "viewer").exists()
    assert not (PLUGIN / "contracts").exists()
    scripts = sorted(p.name for p in (PLUGIN / "scripts").iterdir() if p.suffix == ".py")
    assert scripts == ["doctor.py", "qmd_sync.py"]
    assert not (ROOT / "plugins" / "manager").exists()
    assert not (ROOT / "contracts" / "routing").exists()


def test_bindings_schema_enforces_v1() -> None:
    schema = read_json(ROOT / "contracts" / "manager" / "workspace-bindings-v1.json")
    assert schema["properties"]["schema_version"]["const"] == "wirenet-bindings/v1"
    assert schema["additionalProperties"] is False
