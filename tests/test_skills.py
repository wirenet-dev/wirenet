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
    expected = {
        "manager": {"manager", "manager-setup"},
        "workflows": {"loop", "ultragoal"},
        "content-tools": {"simple-html-artifact", "audit-ai-writing"},
    }
    for plugin, names in expected.items():
        skills = sorted((ROOT / f"plugins/{plugin}/skills").glob("*/SKILL.md"))
        assert {skill.parent.name for skill in skills} == names
        for skill in skills:
            assert validator.validate_markdown(skill, plugin_skill=True) == []
            assert "[TODO:" not in skill.read_text(encoding="utf-8")

    developer = sorted((ROOT / ".agents/skills").glob("*/SKILL.md"))
    assert {skill.parent.name for skill in developer} == {
        "audit-ai-code",
        "audit-ai-frontend",
        "yeet",
    }
    for skill in developer:
        assert validator.validate_markdown(skill, plugin_skill=True) == []


def test_public_skills_use_the_wirenet_globe_in_codex_ui() -> None:
    for plugin in ("manager", "workflows", "content-tools"):
        for skill in (ROOT / f"plugins/{plugin}/skills").iterdir():
            if not (skill / "SKILL.md").is_file():
                continue

            metadata = (skill / "agents/openai.yaml").read_text(encoding="utf-8")
            expected = '"./assets/wirenet-globe.svg"'
            assert f"icon_small: {expected}" in metadata
            assert f"icon_large: {expected}" in metadata
            assert 'brand_color: "#FF5C1A"' in metadata

            icon = skill / "assets/wirenet-globe.svg"
            assert icon.is_file()
            globe = icon.read_text(encoding="utf-8")
            assert 'viewBox="0 0 64 64"' in globe
            assert "<circle" in globe
            assert "<ellipse" in globe
            assert "#FF5C1A" not in globe


def test_manager_seed_contains_content_but_no_embedded_skills() -> None:
    seed = ROOT / "plugins/manager/templates/manager"
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
    skills = ROOT / "plugins/manager/skills"
    manager = (skills / "manager/SKILL.md").read_text(encoding="utf-8")
    sync = (skills / "manager/references/workspace-sync.md").read_text(
        encoding="utf-8"
    )
    bootstrap = (skills / "manager-setup/SKILL.md").read_text(
        encoding="utf-8"
    )
    contract = (skills / "manager/references/content-routing.md").read_text(
        encoding="utf-8"
    )

    assert "references/content-routing.md" in manager
    assert "content-routing.md" in sync
    assert "references/onboarding.md" in bootstrap
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
        ROOT / "plugins/manager/templates/manager/AGENTS.md"
    ).read_text(encoding="utf-8")


def test_bootstrap_resolves_runtime_for_non_developer_computers() -> None:
    bootstrap = (
        ROOT / "plugins/manager/skills/manager-setup/SKILL.md"
    ).read_text(encoding="utf-8")
    preflight = (
        ROOT
        / "plugins/manager/skills/manager-setup/references/runtime-preflight.md"
    ).read_text(encoding="utf-8")
    qmd = (ROOT / "plugins/manager/scripts/manager_qmd.py").read_text(
        encoding="utf-8"
    )

    assert "references/runtime-preflight.md" in bootstrap
    assert "--git-bin <resolved-git>" in bootstrap
    assert "bundled workspace dependencies" in preflight
    assert "stop before writing Manager files" in preflight
    assert "--npm-bin" in preflight
    assert "--pnpm-bin" in preflight
    assert 'parser.add_argument("--pnpm-bin")' in qmd


def test_manager_project_person_and_sync_have_distinct_roles() -> None:
    skills = ROOT / "plugins/manager/skills"
    manager = (skills / "manager/SKILL.md").read_text(encoding="utf-8")
    project = (skills / "manager/references/project-lifecycle.md").read_text(
        encoding="utf-8"
    )
    person = (skills / "manager/references/person-context.md").read_text(
        encoding="utf-8"
    )
    sync = (skills / "manager/references/workspace-sync.md").read_text(
        encoding="utf-8"
    )

    assert "references/project-lifecycle.md" in manager
    assert "references/person-context.md" in manager
    assert "references/workspace-sync.md" in manager
    assert "scripts/create_project_pack.py" in project
    assert "scripts/create_experiment_pack.py" in project
    assert "scripts/promote_experiment.py" in project
    assert "scripts/transition_packet.py" in project
    assert "scripts/create_person_note.py" in person
    assert "Do not create a person concept merely because a name appeared once" in person
    assert "External Workspace Sync" in sync
    assert "project-lifecycle.md" in sync
    assert "person-context.md" in sync


def test_manager_keeps_jason_style_proactive_entry_triggers() -> None:
    skill = (
        ROOT / "plugins/manager/skills/manager/SKILL.md"
    ).read_text(encoding="utf-8")

    for trigger in (
        "what they should know",
        "proactive work awareness",
        "keep an eye on work",
        "follow-up or check-in help",
    ):
        assert trigger in skill


def test_manager_current_stack_uses_a_fresh_calendar_signal() -> None:
    skill = (
        ROOT / "plugins/manager/skills/manager/SKILL.md"
    ).read_text(encoding="utf-8")
    normalized = " ".join(skill.split())

    assert "## Fresh Live Signals" in normalized
    assert "approved connected calendar" in normalized
    assert "at most 30 minutes old" in normalized
    assert "same local date and window" in normalized
    assert "live calendar was not checked" in normalized
    assert "Do not persist a shadow" in normalized


def test_loop_is_general_task_automation_with_clean_completion() -> None:
    skill = (ROOT / "plugins/workflows/skills/loop/SKILL.md").read_text(
        encoding="utf-8"
    )
    metadata = (
        ROOT / "plugins/workflows/skills/loop/agents/openai.yaml"
    ).read_text(encoding="utf-8")

    assert "current Codex task" in skill.split("---", 2)[1]
    assert "Continue immediately instead" in skill
    assert "one active heartbeat" in skill
    assert "delete the active" in skill
    assert "`done: <short task>`" in skill
    assert "changes timing, not authorization" in skill
    assert "$loop" in metadata
    assert "allow_implicit_invocation: true" in metadata


def test_ultragoal_is_installed_but_explicit_only() -> None:
    skill = ROOT / "plugins/workflows/skills/ultragoal"
    metadata = (skill / "agents/openai.yaml").read_text(encoding="utf-8")
    instructions = (skill / "SKILL.md").read_text(encoding="utf-8")

    assert "allow_implicit_invocation: false" in metadata
    assert "Never infer activation" in instructions
    assert 'producer: "ultragoal"' in instructions


def test_optional_plugins_and_developer_shelf_remain_separate() -> None:
    content = ROOT / "plugins/content-tools/skills"
    html = (content / "simple-html-artifact/SKILL.md").read_text(encoding="utf-8")
    writing = (content / "audit-ai-writing/SKILL.md").read_text(encoding="utf-8")
    yeet = ROOT / ".agents/skills/yeet"

    assert "self-contained" in html.split("---", 2)[1]
    assert "information-first" in html
    assert "reader model" in writing.lower()
    assert "detector" in writing.lower()
    assert "allow_implicit_invocation: false" in (
        yeet / "agents/openai.yaml"
    ).read_text(encoding="utf-8")
    assert not (ROOT / "plugins/content-tools/skills/yeet").exists()
    assert not (ROOT / "plugins/manager/skills/loop").exists()


def test_plugin_manifest_and_marketplace_use_core_namespace() -> None:
    manifest = json.loads(
        (ROOT / "plugins/manager/.codex-plugin/plugin.json").read_text(
            encoding="utf-8"
        )
    )
    marketplace = json.loads(
        (ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8")
    )
    assert manifest["name"] == "manager"
    assert manifest["version"] == "0.4.2"
    assert manifest["skills"] == "./skills/"
    assert manifest["interface"]["brandColor"] == "#FF5C1A"
    prompts = manifest["interface"]["defaultPrompt"]
    assert len(prompts) == 3
    assert all(len(prompt) <= 128 for prompt in prompts)
    assert manifest["interface"]["capabilities"] == [
        "Personal onboarding",
        "Project and experiment tracking",
        "Cross-workspace context routing",
        "Personal context and people",
        "Local knowledge search",
    ]
    for asset_key in ("composerIcon", "logo", "logoDark"):
        asset = ROOT / "plugins/manager" / manifest["interface"][asset_key]
        assert asset.is_file()
    for logo_key in ("logo", "logoDark"):
        logo = (
            ROOT / "plugins/manager" / manifest["interface"][logo_key]
        ).read_text(encoding="utf-8")
        assert 'viewBox="0 0 128 128"' in logo
        assert "<text" not in logo
        assert "#FF5C1A" not in logo
    assert marketplace["name"] == "wirenet"
    assert marketplace["interface"]["displayName"] == "wirenet"
    assert [entry["name"] for entry in marketplace["plugins"]] == [
        "manager",
        "workflows",
        "content-tools",
    ]
    for entry in marketplace["plugins"]:
        assert entry["source"] == {
            "source": "local",
            "path": f"./plugins/{entry['name']}",
        }
        assert entry["policy"] == {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        }


def test_clean_codex_install_contract_is_complete_and_repo_readable() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    install = (ROOT / "docs/installing-wirenet-manager.md").read_text(
        encoding="utf-8"
    )
    for document in (readme, install):
        assert "Set me up." in document
        assert "Richte das für mich ein." in document
        assert "press both Command keys" in document
        assert (
            "codex plugin marketplace add wirenet-dev/wirenet --ref stable"
            in document
        )
        assert "codex plugin add manager@wirenet" in document
        assert (
            "$manager-setup Set up my local Manager, then continue "
            "with onboarding." in document
        )

    assert "never cloned into `~/Manager`" in readme
    assert "does not install a plugin by itself" in install


def test_personal_onboarding_preserves_jason_sequence_with_explicit_gates() -> None:
    bootstrap = (
        ROOT
        / "plugins/manager/skills/manager-setup/SKILL.md"
    ).read_text(encoding="utf-8")
    skill = (
        ROOT
        / "plugins/manager/skills/manager-setup/references/onboarding.md"
    ).read_text(encoding="utf-8")
    reference = (
        ROOT
        / "plugins/manager/skills/manager-setup/references/first-meeting-flow.md"
    ).read_text(encoding="utf-8")
    task_template = (
        ROOT
        / "plugins/manager/skills/manager-setup/references/manager-task-template.md"
    ).read_text(encoding="utf-8")

    assert "references/onboarding.md" in bootstrap
    assert "personal first meeting" in bootstrap
    assert "references/first-meeting-flow.md" in skill
    for state in ("`brand_new`", "`partial`", "`established`"):
        assert state in skill
    assert "Hi, I'm your Manager." in reference
    assert "Hi, ich bin dein Manager." in reference
    assert "What's on your plate right now?" in reference
    assert "before its first connected-source scan" in reference
    assert "Interview And Targeted Rereads" in reference
    assert "install or enable a plugin" in reference
    assert "connect an account or service" in reference
    assert "the last 90 days" in reference
    assert "docs/communication-and-files.md" in reference
    assert "current task as destination" in reference
    assert "09:00 and 16:00" in reference
    assert "write-like-me.md" in reference
    assert "never scan the whole home directory for personal skills" in reference
    assert "offer to migrate and validate it" in reference
    assert "You can just talk to your Manager" in reference
    assert "references/manager-task-template.md" in skill
    assert "~/Manager as the canonical" in task_template
    assert "do not duplicate Manager content" in task_template
    assert "Work first and notify second" in task_template
    assert "otherwise stay quiet" in task_template

    headings = (
        "## 1. Hello",
        "## 3. First Map",
        "## 4. Interview And Targeted Rereads",
        "## 5. Source Pass And Durable Proposals",
        "## 6. Core Check-In",
        "## 7. Optional Monitor Tasks",
        "## 8. Write Like Me",
        "## 9. Shared Memory And Daily Use",
        "## 10. Close",
    )
    positions = [reference.index(heading) for heading in headings]
    assert positions == sorted(positions)


def test_write_like_me_bootstrap_generates_behavior_outside_manager() -> None:
    skill = (
        ROOT / "plugins/manager/skills/manager-setup/references/write-like-me.md"
    ).read_text(encoding="utf-8")
    assert "~/.agents/skills/write-like-me/" in skill
    assert "Never place it inside `~/Manager`" in skill
    assert "last 90–180 days" in skill
    assert "Never store raw Slack or email excerpts" in skill
    assert "separate approvals" in skill
    assert "## Existing Skill First" in skill
    assert ".agents/skills/write-like-me/" in skill
    assert ".codex/skills/write-like-me/" in skill
    assert "Never scan the whole home directory" in skill
    assert "Never overwrite" in skill
    assert "legacy" in skill
    assert "`last_edited`" in skill

    template = (
        ROOT
        / "plugins/manager/skills/manager-setup/references/write-like-me-skill-template.md"
    ).read_text(encoding="utf-8")
    generated_skill = template.split("```md", 1)[1].split("```", 1)[0]
    assert "last_edited" not in generated_skill
    assert "name: write-like-me" in generated_skill
    assert "description:" in generated_skill
    assert "allow_implicit_invocation: true" in template


def test_language_and_communication_policy_stays_in_the_right_layers() -> None:
    seed_readme = (
        ROOT / "plugins/manager/templates/manager/README.md"
    ).read_text(encoding="utf-8")
    seed_agents = (
        ROOT / "plugins/manager/templates/manager/AGENTS.md"
    ).read_text(encoding="utf-8")
    routing = (
        ROOT
        / "plugins/manager/skills/manager/references/content-routing.md"
    ).read_text(encoding="utf-8")
    seed_docs = ROOT / "plugins/manager/templates/manager/docs"

    assert 'content_language: "en"' in seed_readme
    assert "Read `content_language` from the root `README.md`" in seed_agents
    assert "docs/communication-and-files.md" in routing
    assert not (seed_docs / "communication-and-files.md").exists()
