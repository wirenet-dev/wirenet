from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/wirenet-manager"
PLUGIN_SCRIPTS = PLUGIN / "scripts"
BOOTSTRAP = PLUGIN / "skills/wirenet-manager-bootstrap/scripts/bootstrap_manager.py"
GUIDANCE = PLUGIN / "skills/wirenet-manager-bootstrap/scripts/install_global_guidance.py"
INSPECT = PLUGIN / "skills/wirenet-manager-sync/scripts/inspect_workspace.py"
ROUTING = PLUGIN / "skills/wirenet-manager-sync/scripts/record_routing.py"
CREATE_PROJECT = PLUGIN_SCRIPTS / "create_project_pack.py"
DISCOVER = PLUGIN_SCRIPTS / "discover_projects.py"
DOCTOR = PLUGIN_SCRIPTS / "manager_doctor.py"


def run_script(script: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=True,
    )


def bootstrap(manager: Path) -> dict[str, object]:
    return json.loads(run_script(BOOTSTRAP, "--manager-dir", str(manager), "--apply").stdout)


def frontmatter_value(path: Path, key: str) -> str | None:
    match = re.search(
        rf"(?m)^{re.escape(key)}:\s*[\"']?(?P<value>[^\"'\n]+)",
        path.read_text(encoding="utf-8"),
    )
    return match.group("value").strip() if match else None


def test_global_guidance_preserves_content_and_is_idempotent(tmp_path: Path) -> None:
    agents = tmp_path / "AGENTS.md"
    agents.write_text("# Existing rules\n\nKeep this.\n", encoding="utf-8")

    preview = json.loads(run_script(GUIDANCE, "--agents-file", str(agents)).stdout)
    assert preview["dry_run"] is True
    assert agents.read_text(encoding="utf-8") == "# Existing rules\n\nKeep this.\n"

    first = json.loads(run_script(GUIDANCE, "--agents-file", str(agents), "--apply").stdout)
    first_content = agents.read_text(encoding="utf-8")
    second = json.loads(run_script(GUIDANCE, "--agents-file", str(agents), "--apply").stdout)

    assert first["changed"] is True
    assert second["changed"] is False
    assert agents.read_text(encoding="utf-8") == first_content
    assert "# Existing rules" in first_content
    assert first_content.count("<!-- wirenet-manager:core:start -->") == 1
    assert "<!-- wirenet-manager:routing:start -->" not in first_content
    assert "$wirenet-manager-sync" in first_content
    assert "installed and enabled" in first_content
    assert "unavailable or disabled, do nothing" in first_content
    assert "routine edits" in first_content


def test_global_guidance_installs_optional_routing_without_second_source(
    tmp_path: Path,
) -> None:
    agents = tmp_path / "AGENTS.md"
    rules = (
        "`~/Projects`: default location for new active work.",
        "`~/Developer`: long-running code and systems.",
    )

    preview = json.loads(
        run_script(
            GUIDANCE,
            "--agents-file",
            str(agents),
            "--routing-rule",
            rules[0],
            "--routing-rule",
            rules[1],
        ).stdout
    )
    assert preview["routing_action"] == "installed"
    assert preview["routing_managed_block"] is not None
    assert not agents.exists()

    applied = json.loads(
        run_script(
            GUIDANCE,
            "--agents-file",
            str(agents),
            "--routing-rule",
            rules[0],
            "--routing-rule",
            rules[1],
            "--apply",
        ).stdout
    )
    content = agents.read_text(encoding="utf-8")
    assert applied["routing_action"] == "installed"
    assert content.count("<!-- wirenet-manager:core:start -->") == 1
    assert content.count("<!-- wirenet-manager:routing:start -->") == 1
    assert content.count("## Workspace Routing") == 1
    assert all(rule in content for rule in rules)

    repeated = json.loads(
        run_script(GUIDANCE, "--agents-file", str(agents), "--apply").stdout
    )
    assert repeated["changed"] is False
    assert repeated["routing_action"] == "preserved"


def test_global_guidance_can_remove_only_optional_routing(tmp_path: Path) -> None:
    agents = tmp_path / "AGENTS.md"
    run_script(
        GUIDANCE,
        "--agents-file",
        str(agents),
        "--routing-rule",
        "`~/Projects`: default project location.",
        "--apply",
    )

    result = json.loads(
        run_script(
            GUIDANCE,
            "--agents-file",
            str(agents),
            "--clear-routing",
            "--apply",
        ).stdout
    )
    content = agents.read_text(encoding="utf-8")
    assert result["routing_action"] == "removed"
    assert "<!-- wirenet-manager:core:start -->" in content
    assert "<!-- wirenet-manager:routing:start -->" not in content


def test_global_guidance_migrates_legacy_core_markers(tmp_path: Path) -> None:
    agents = tmp_path / "AGENTS.md"
    agents.write_text(
        "<!-- wirenet-manager:start -->\nOld rule\n<!-- wirenet-manager:end -->\n",
        encoding="utf-8",
    )

    result = json.loads(
        run_script(GUIDANCE, "--agents-file", str(agents), "--apply").stdout
    )
    content = agents.read_text(encoding="utf-8")
    assert result["changed"] is True
    assert "<!-- wirenet-manager:start -->" not in content
    assert content.count("<!-- wirenet-manager:core:start -->") == 1


def test_bootstrap_materializes_content_only_manager_with_local_git(tmp_path: Path) -> None:
    destination = tmp_path / "Manager"
    preview = json.loads(run_script(BOOTSTRAP, "--manager-dir", str(destination)).stdout)
    assert preview["dry_run"] is True
    assert preview["state"] == "new"
    assert not destination.exists()

    applied = bootstrap(destination)
    assert applied["ok"] is True
    assert applied["state"] == "created"
    assert applied["doctor"]["ok"] is True
    assert (destination / ".git").is_dir()
    assert not (destination / ".codex").exists()
    assert not (destination / ".agents").exists()
    assert not (destination / "plugins").exists()
    assert not (destination / "scripts").exists()
    assert subprocess.run(
        ["git", "remote"], cwd=destination, check=True, capture_output=True, text=True
    ).stdout.strip() == ""
    assert subprocess.run(
        ["git", "rev-list", "--count", "HEAD"],
        cwd=destination,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip() == "1"

    metadata = json.loads((destination / ".wirenet/manager.json").read_text(encoding="utf-8"))
    assert metadata["schema_version"] == "wirenet-manager/v0.1"
    assert metadata["project_pack_profile"] == "wirenet-project-pack/v0.1"
    assert metadata["plugin_version"] == "0.1.2"
    assert metadata["manager_id"].startswith("mgr_")

    repeated = json.loads(run_script(BOOTSTRAP, "--manager-dir", str(destination)).stdout)
    assert repeated["state"] == "healthy"
    assert repeated["doctor"]["ok"] is True


def test_repair_fills_an_empty_existing_manager_without_overwrite(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    manager.mkdir()
    existing = manager / "custom.txt"
    existing.write_text("keep me", encoding="utf-8")

    preview = json.loads(
        run_script(BOOTSTRAP, "--manager-dir", str(manager), "--repair").stdout
    )
    assert preview["dry_run"] is True
    assert not (manager / "README.md").exists()

    repaired = json.loads(
        run_script(BOOTSTRAP, "--manager-dir", str(manager), "--repair", "--apply").stdout
    )
    assert repaired["state"] == "repaired"
    assert repaired["doctor"]["ok"] is True
    assert existing.read_text(encoding="utf-8") == "keep me"
    assert not (manager / ".git").exists()


def test_project_pack_is_open_and_supports_optional_concepts_and_local_routing(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    parent = tmp_path / "projects/client"
    child = parent / "campaign"
    child.mkdir(parents=True)

    parent_result = json.loads(
        run_script(
            CREATE_PROJECT,
            "Client",
            "--summary",
            "Parent packet",
            "--workspace",
            str(parent),
            "--manager-dir",
            str(manager),
            "--apply",
        ).stdout
    )
    child_result = json.loads(
        run_script(
            CREATE_PROJECT,
            "Campaign",
            "--summary",
            "Nested packet",
            "--workspace",
            str(child),
            "--manager-dir",
            str(manager),
            "--with-goal",
            "--with-result",
            "--with-log",
            "--apply",
        ).stdout
    )

    parent_packet = Path(str(parent_result["packet"]))
    assert {path.name for path in parent_packet.iterdir()} == {"README.md", "AGENTS.md"}
    assert {
        frontmatter_value(parent_packet / name, "project_id")
        for name in ("README.md", "AGENTS.md")
    } == {parent_result["project_id"]}

    child_packet = Path(str(child_result["packet"]))
    assert {path.name for path in child_packet.iterdir()} == {
        "README.md",
        "AGENTS.md",
        "GOAL.md",
        "RESULT.md",
        "log.md",
    }
    assert {
        frontmatter_value(child_packet / name, "project_id")
        for name in ("README.md", "AGENTS.md", "GOAL.md", "RESULT.md")
    } == {child_result["project_id"]}
    assert frontmatter_value(child_packet / "GOAL.md", "type") == "Project Brief"
    assert frontmatter_value(child_packet / "README.md", "type") == "Project Status"
    assert frontmatter_value(child_packet / "RESULT.md", "type") == "Project Result"
    assert frontmatter_value(child_packet / "AGENTS.md", "type") == "Runtime Adapter"
    log = (child_packet / "log.md").read_text(encoding="utf-8")
    assert not log.startswith("---")
    assert re.search(r"(?m)^## \d{4}-\d{2}-\d{2}$", log)
    assert "**Creation**" in log

    (parent_packet / "DECISION.md").write_text(
        "\n".join(
            [
                "---",
                'type: "Project Decision"',
                'schema: "wirenet-project-pack/v0.1"',
                f'project_id: "{parent_result["project_id"]}"',
                "---",
                "",
                "# Decision",
                "",
                "Keep the Project Pack open.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    campaign_readme = Path(str(child_result["packet"])) / "README.md"
    assert str(child.resolve()) not in campaign_readme.read_text(encoding="utf-8")
    index = (manager / "projects/index.md").read_text(encoding="utf-8")
    router = (manager / "projects/README.md").read_text(encoding="utf-8")
    assert not index.startswith("---")
    assert index.endswith("\n")
    assert "[Client](client/README.md) — Parent packet" in index
    assert "[Campaign](campaign/README.md) — Nested packet" in index
    assert "[Client](client/README.md) — Parent packet" in router
    assert "[Campaign](campaign/README.md) — Nested packet" in router
    registry = json.loads(
        (manager / ".wirenet/project-bindings.json").read_text(encoding="utf-8")
    )
    assert {row["path"] for row in registry["bindings"]} == {
        str(parent.resolve()),
        str(child.resolve()),
    }

    result = json.loads(
        run_script(INSPECT, "--manager-dir", str(manager), "--workspace", str(child / "edit")).stdout
    )
    assert result["classification"] == "tracked"
    assert result["project_id"] == child_result["project_id"]
    assert result["project_packet"].endswith("projects/campaign")

    ignored = child / "scratch"
    ignored.mkdir()
    run_script(
        ROUTING,
        str(ignored),
        "--classification",
        "ignored",
        "--manager-dir",
        str(manager),
        "--apply",
    )
    repeated_route = json.loads(
        run_script(
            ROUTING,
            str(ignored),
            "--classification",
            "ignored",
            "--manager-dir",
            str(manager),
            "--apply",
        ).stdout
    )
    assert repeated_route["changed"] is False
    routed = json.loads(
        run_script(INSPECT, "--manager-dir", str(manager), "--workspace", str(ignored)).stdout
    )
    assert routed["classification"] == "ignored"

    diagnosis = json.loads(run_script(DOCTOR, "--manager-dir", str(manager)).stdout)
    assert diagnosis["ok"] is True
    assert len(diagnosis["project_packs"]) == 2


def test_manager_doctor_rejects_an_untyped_project_concept(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    result = json.loads(
        run_script(
            CREATE_PROJECT,
            "Untyped",
            "--summary",
            "Doctor fixture",
            "--manager-dir",
            str(manager),
            "--apply",
        ).stdout
    )
    packet = Path(str(result["packet"]))
    (packet / "NOTE.md").write_text(
        "\n".join(
            [
                "---",
                'schema: "wirenet-project-pack/v0.1"',
                f'project_id: "{result["project_id"]}"',
                "---",
                "",
                "# Untyped note",
                "",
            ]
        ),
        encoding="utf-8",
    )

    diagnosis = json.loads(
        run_script(DOCTOR, "--manager-dir", str(manager), check=False).stdout
    )
    assert diagnosis["ok"] is False
    assert any("NOTE.md is missing a non-empty OKF type" in error for error in diagnosis["errors"])


def test_project_preview_and_rejected_overlap_are_side_effect_free(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    tracked_paths = (
        manager / "projects/README.md",
        manager / "projects/index.md",
        manager / ".wirenet/project-bindings.json",
    )
    before = {path: path.read_bytes() for path in tracked_paths}

    preview = json.loads(
        run_script(
            CREATE_PROJECT,
            "Preview Only",
            "--summary",
            "No writes yet",
            "--workspace",
            str(workspace),
            "--manager-dir",
            str(manager),
        ).stdout
    )
    assert preview["dry_run"] is True
    assert not Path(str(preview["packet"])).exists()
    assert {path: path.read_bytes() for path in tracked_paths} == before

    created = json.loads(
        run_script(
            CREATE_PROJECT,
            "Tracked",
            "--summary",
            "Owns the workspace",
            "--workspace",
            str(workspace),
            "--manager-dir",
            str(manager),
            "--apply",
        ).stdout
    )
    after_create = {path: path.read_bytes() for path in tracked_paths}
    rejected = run_script(
        CREATE_PROJECT,
        "Duplicate Route",
        "--summary",
        "Must not be created",
        "--workspace",
        str(workspace),
        "--manager-dir",
        str(manager),
        "--apply",
        check=False,
    )
    rejected_result = json.loads(rejected.stdout)
    assert rejected.returncode == 2
    assert "already classified" in rejected_result["error"]
    assert not (manager / "projects/duplicate-route").exists()
    assert {path: path.read_bytes() for path in tracked_paths} == after_create
    assert Path(str(created["packet"])).is_dir()


def test_manager_doctor_detects_collection_router_drift(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    result = json.loads(
        run_script(
            CREATE_PROJECT,
            "Router Drift",
            "--summary",
            "Must appear in both routes",
            "--manager-dir",
            str(manager),
            "--apply",
        ).stdout
    )
    index = manager / "projects/index.md"
    entry = "- [Router Drift](router-drift/README.md) — Must appear in both routes\n"
    index.write_text(index.read_text(encoding="utf-8").replace(entry, ""), encoding="utf-8")

    diagnosis = json.loads(
        run_script(DOCTOR, "--manager-dir", str(manager), check=False).stdout
    )
    assert diagnosis["ok"] is False
    assert any(
        "router-drift: Project Pack is missing from projects/index.md" in error
        for error in diagnosis["errors"]
    )
    assert Path(str(result["packet"])).is_dir()


def test_manager_doctor_detects_project_identity_drift(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    first = json.loads(
        run_script(
            CREATE_PROJECT,
            "First",
            "--summary",
            "First packet",
            "--manager-dir",
            str(manager),
            "--apply",
        ).stdout
    )
    second = json.loads(
        run_script(
            CREATE_PROJECT,
            "Second",
            "--summary",
            "Second packet",
            "--manager-dir",
            str(manager),
            "--apply",
        ).stdout
    )
    second_readme = Path(str(second["packet"])) / "README.md"
    second_readme.write_text(
        second_readme.read_text(encoding="utf-8").replace(
            str(second["project_id"]), str(first["project_id"])
        ),
        encoding="utf-8",
    )

    diagnosis = json.loads(
        run_script(DOCTOR, "--manager-dir", str(manager), check=False).stdout
    )
    assert diagnosis["ok"] is False
    assert any("duplicate project_id" in error for error in diagnosis["errors"])
    assert any(
        "all Project Pack concept files must share one project_id" in error
        for error in diagnosis["errors"]
    )


def test_manager_doctor_detects_invalid_log_chronology(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    result = json.loads(
        run_script(
            CREATE_PROJECT,
            "Chronology",
            "--summary",
            "Dates must be newest first",
            "--manager-dir",
            str(manager),
            "--with-log",
            "--apply",
        ).stdout
    )
    log = Path(str(result["packet"])) / "log.md"
    log.write_text(
        "# Chronology Update Log\n\n"
        "## 2026-07-14\n\n- **Creation**: Started.\n\n"
        "## 2026-07-15\n\n- **Update**: Continued.\n",
        encoding="utf-8",
    )

    diagnosis = json.loads(
        run_script(DOCTOR, "--manager-dir", str(manager), check=False).stdout
    )
    assert diagnosis["ok"] is False
    assert any("log.md date headings must be newest first" in error for error in diagnosis["errors"])


def test_project_discovery_is_shallow_and_marker_only(tmp_path: Path) -> None:
    root = tmp_path / "Projects"
    marked = root / "client"
    unmarked = root / "scratch"
    nested = unmarked / "nested"
    marked.mkdir(parents=True)
    nested.mkdir(parents=True)
    (marked / "README.md").write_text("project", encoding="utf-8")
    (nested / "package.json").write_text("{}", encoding="utf-8")

    result = json.loads(run_script(DISCOVER, str(root), "--max-depth", "1").stdout)
    assert result["ok"] is True
    assert [row["path"] for row in result["candidates"]] == [str(marked.resolve())]
