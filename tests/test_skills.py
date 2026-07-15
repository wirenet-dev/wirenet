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


def test_plugin_skill_frontmatter_uses_official_contract() -> None:
    validator = load_module(ROOT / "scripts" / "validate_markdown.py")
    skills = sorted((ROOT / "plugins/wirenet-manager/skills").glob("*/SKILL.md"))
    assert {skill.parent.name for skill in skills} == {
        "ultragoal",
        "wirenet-manager",
        "wirenet-manager-bootstrap",
        "wirenet-manager-sync",
    }
    for skill in skills:
        assert validator.validate_markdown(skill, plugin_skill=True) == []
        assert "[TODO:" not in skill.read_text(encoding="utf-8")


def test_manager_seed_contains_content_but_no_embedded_skills() -> None:
    seed = ROOT / "plugins/wirenet-manager/templates/manager"
    assert (seed / ".gitignore").is_file()
    assert (seed / "AGENTS.md").is_file()
    assert (seed / "index.md").is_file()
    assert 'type: "Manager Overview"' in (seed / "README.md").read_text(
        encoding="utf-8"
    )
    assert (seed / "projects/AGENTS.md").is_file()
    assert (seed / "projects/index.md").is_file()
    for shelf in (
        "archive",
        "docs",
        "experiments",
        "notes",
        "outputs",
        "people",
        "projects",
        "sources",
    ):
        assert not (seed / shelf / "README.md").exists()
    assert not (seed / "templates").exists()
    assert (seed / ".wirenet/workspace-bindings.json").is_file()
    assert not (seed / ".wirenet/project-bindings.json").exists()
    assert not (seed / ".agents").exists()
    assert not (seed / ".codex").exists()


def test_manager_skills_share_one_content_routing_contract() -> None:
    skills = ROOT / "plugins/wirenet-manager/skills"
    manager = (skills / "wirenet-manager/SKILL.md").read_text(encoding="utf-8")
    sync = (skills / "wirenet-manager-sync/SKILL.md").read_text(encoding="utf-8")
    bootstrap = (skills / "wirenet-manager-bootstrap/SKILL.md").read_text(
        encoding="utf-8"
    )
    contract = (skills / "wirenet-manager/references/content-routing.md").read_text(
        encoding="utf-8"
    )

    assert "references/content-routing.md" in manager
    assert "../wirenet-manager/references/content-routing.md" in sync
    assert "README.md" in bootstrap and "AGENTS.md" in bootstrap
    assert (
        "Keep this shared reference instead of creating a separate routing skill"
        in contract
    )
    assert "Manager `index.md` declares OKF 0.1" in contract
    assert "Every other Markdown document" in contract
    assert "Neither file is required merely because a packet exists" in contract
    assert "File-World Heuristic" in contract
    assert "Short-lived work is not automatically an experiment" in contract
    assert "`outputs/<task-slug>/`" in (
        ROOT / "plugins/wirenet-manager/templates/manager/AGENTS.md"
    ).read_text(encoding="utf-8")


def test_ultragoal_is_installed_but_explicit_only() -> None:
    skill = ROOT / "plugins/wirenet-manager/skills/ultragoal"
    metadata = (skill / "agents/openai.yaml").read_text(encoding="utf-8")
    instructions = (skill / "SKILL.md").read_text(encoding="utf-8")

    assert "allow_implicit_invocation: false" in metadata
    assert "Never infer activation" in instructions
    assert 'producer: "ultragoal"' in instructions


def test_plugin_manifest_and_marketplace_point_to_v02_package() -> None:
    manifest = json.loads(
        (ROOT / "plugins/wirenet-manager/.codex-plugin/plugin.json").read_text(
            encoding="utf-8"
        )
    )
    marketplace = json.loads(
        (ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8")
    )
    assert manifest["name"] == "wirenet-manager"
    assert manifest["version"] == "0.2.3"
    assert manifest["skills"] == "./skills/"
    assert manifest["interface"]["brandColor"] == "#FF5C1A"
    for asset_key in ("composerIcon", "logo", "logoDark"):
        asset = ROOT / "plugins/wirenet-manager" / manifest["interface"][asset_key]
        assert asset.is_file()
    assert marketplace["plugins"] == [
        {
            "name": "wirenet-manager",
            "source": {"source": "local", "path": "./plugins/wirenet-manager"},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Productivity",
        }
    ]


def test_clean_codex_install_contract_is_complete_and_repo_readable() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    install = (ROOT / "docs/installing-wirenet-manager.md").read_text(
        encoding="utf-8"
    )
    prompt = (
        "Set me up with wirenet-dev/wirenet-manager as ~/Manager. Read the "
        "repository README first"
    )

    for document in (readme, install):
        assert prompt in document
        assert "press both Command keys" in document
        assert (
            "codex plugin marketplace add wirenet-dev/wirenet-manager --ref main"
            in document
        )
        assert "codex plugin add wirenet-manager@wirenet-manager" in document
        assert "$wirenet-manager-bootstrap Start my guided first run." in document

    assert "never cloned into `~/Manager`" in readme
    assert "does not install a plugin by itself" in install


def test_guided_first_run_contract_covers_map_sources_and_automation() -> None:
    skill = (
        ROOT
        / "plugins/wirenet-manager/skills/wirenet-manager-bootstrap/SKILL.md"
    ).read_text(encoding="utf-8")
    reference = (
        ROOT
        / "plugins/wirenet-manager/skills/wirenet-manager-bootstrap/references/first-run-experience.md"
    ).read_text(encoding="utf-8")

    assert "references/first-run-experience.md" in skill
    assert "brand new, partial, or established" in skill
    assert "installation, connection, source reading" in skill
    assert "current task as the Manager home" in skill
    assert "What's on your plate right now?" in reference
    assert "Communication And Work Sources" in reference
    assert "install or enable a plugin" in reference
    assert "connect an account or service" in reference
    assert "read approved sources" in reference
    assert "Use the scheduled-task or automation tool" in reference
    assert "current task as destination" in reference
    assert "Recommend an hourly quiet heartbeat" in reference
    assert "If local Manager files are part of the check" in reference
    assert "You can just talk to your Manager" in reference
