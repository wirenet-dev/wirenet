from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_repository_markdown_uses_ci_metadata_contract() -> None:
    validator = load_module(ROOT / "scripts" / "validate_markdown.py")
    assert validator.validate_tree(ROOT) == []


def test_markdown_validator_accepts_okf_index_and_log_structure(tmp_path: Path) -> None:
    validator = load_module(ROOT / "scripts" / "validate_markdown.py")
    (tmp_path / "index.md").write_text(
        "# Projects\n\n## Active Project Packs\n", encoding="utf-8"
    )
    (tmp_path / "log.md").write_text(
        "# Update Log\n\n## 2026-07-15\n\n- **Creation**: Started.\n",
        encoding="utf-8",
    )

    assert validator.validate_tree(tmp_path) == []


def test_onboarding_scripts_default_to_repo_root_vault() -> None:
    script_dir = ROOT / ".codex" / "skills" / "onboarding" / "scripts"
    for script_name in (
        "setup_shared_memory_vault.py",
        "new_person_note.py",
        "new_project_note.py",
        "vault_doctor.py",
    ):
        module = load_module(script_dir / script_name)
        assert module.default_vault_dir() == ROOT


def test_plugin_skill_frontmatter_uses_official_contract() -> None:
    validator = load_module(ROOT / "scripts" / "validate_markdown.py")
    skills = sorted((ROOT / "plugins/wirenet-manager/skills").glob("*/SKILL.md"))
    assert {skill.parent.name for skill in skills} == {
        "wirenet-manager",
        "wirenet-manager-bootstrap",
        "wirenet-manager-sync",
    }
    for skill in skills:
        assert validator.validate_markdown(skill, plugin_skill=True) == []
        assert "[TODO:" not in skill.read_text(encoding="utf-8")


def test_manager_seed_contains_content_but_no_embedded_skills() -> None:
    seed = ROOT / "plugins/wirenet-manager/templates/manager"
    assert (seed / "AGENTS.md").is_file()
    assert (seed / "projects/AGENTS.md").is_file()
    assert (seed / "projects/index.md").is_file()
    assert not (seed / "projects/README.md").exists()
    assert (seed / ".wirenet/project-bindings.json").is_file()
    assert not (seed / ".agents").exists()
    assert not (seed / ".codex").exists()


def test_plugin_manifest_and_marketplace_point_to_v01_package() -> None:
    manifest = json.loads(
        (ROOT / "plugins/wirenet-manager/.codex-plugin/plugin.json").read_text(encoding="utf-8")
    )
    marketplace = json.loads(
        (ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8")
    )
    assert manifest["name"] == "wirenet-manager"
    assert manifest["version"] == "0.1.1"
    assert manifest["skills"] == "./skills/"
    assert marketplace["plugins"] == [
        {
            "name": "wirenet-manager",
            "source": {"source": "local", "path": "./plugins/wirenet-manager"},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Productivity",
        }
    ]
