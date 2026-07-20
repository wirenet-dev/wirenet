from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/manager"
PLUGIN_SCRIPTS = PLUGIN / "scripts"
BOOTSTRAP = PLUGIN / "skills/manager-setup/scripts/bootstrap_manager.py"
GUIDANCE = (
    PLUGIN / "skills/manager-setup/scripts/install_global_guidance.py"
)
INSPECT = PLUGIN_SCRIPTS / "inspect_workspace.py"
IGNORE = PLUGIN_SCRIPTS / "record_ignored_workspace.py"
CREATE_PROJECT = PLUGIN_SCRIPTS / "create_project_pack.py"
CREATE_EXPERIMENT = PLUGIN_SCRIPTS / "create_experiment_pack.py"
CREATE_PERSON = PLUGIN_SCRIPTS / "create_person_note.py"
PROMOTE_EXPERIMENT = PLUGIN_SCRIPTS / "promote_experiment.py"
TRANSITION = PLUGIN_SCRIPTS / "transition_packet.py"
DISCOVER = PLUGIN_SCRIPTS / "discover_projects.py"
DOCTOR = PLUGIN_SCRIPTS / "manager_doctor.py"
UPGRADE = PLUGIN_SCRIPTS / "upgrade_manager.py"
TIDY_TIMESTAMPS = PLUGIN_SCRIPTS / "tidy_timestamps.py"
UPDATE_CHECK = PLUGIN_SCRIPTS / "manager_update.py"


def run_script(
    script: Path,
    *args: str,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=ROOT,
        env=env,
        check=check,
        capture_output=True,
        text=True,
    )


def bootstrap(manager: Path) -> dict[str, object]:
    return json.loads(
        run_script(BOOTSTRAP, "--manager-dir", str(manager), "--apply").stdout
    )


def frontmatter_value(path: Path, key: str) -> str | None:
    match = re.search(
        rf"(?m)^{re.escape(key)}:\s*[\"']?(?P<value>[^\"'\n]+)",
        path.read_text(encoding="utf-8"),
    )
    return match.group("value").strip() if match else None


def commit_manager(manager: Path, message: str) -> None:
    subprocess.run(["git", "add", "."], cwd=manager, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=wirenet Test",
            "-c",
            "user.email=test@wirenet.invalid",
            "-c",
            "commit.gpgsign=false",
            "commit",
            "-m",
            message,
        ],
        cwd=manager,
        check=True,
        capture_output=True,
        text=True,
    )


def make_legacy_v01_manager(
    manager: Path,
    *,
    experiment_route: Path | None = None,
) -> None:
    metadata_path = manager / ".wirenet/manager.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["schema_version"] = "wirenet-manager/v0.1"
    metadata["plugin_version"] = "0.1.2"
    metadata["okf_profile"] = "wirenet-okf-project-pack/v0.1"
    metadata.pop("experiment_pack_profile", None)
    metadata.pop("okf_profiles", None)
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    current_path = manager / ".wirenet/workspace-bindings.json"
    current = json.loads(current_path.read_text(encoding="utf-8"))
    legacy_path = manager / ".wirenet/project-bindings.json"
    current_path.replace(legacy_path)
    routes = [
        {"path": row["path"], "classification": "ignored"}
        for row in current.get("ignored", [])
    ]
    if experiment_route is not None:
        routes.append(
            {"path": str(experiment_route.resolve()), "classification": "experiment"}
        )
    legacy = {
        "schema_version": "wirenet-project-bindings/v0.1",
        "updated_at": current["updated_at"],
        "bindings": current.get("projects", []),
        "routes": routes,
    }
    legacy_path.write_text(json.dumps(legacy, indent=2) + "\n", encoding="utf-8")

    for relative in ("README.md", "TODO.md", "agent/USER_CONTEXT.md"):
        path = manager / relative
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                'schema: "wirenet-manager/v0.2"',
                'schema: "wirenet-manager/v0.1"',
            ),
            encoding="utf-8",
        )

    for readme in sorted((manager / "projects").glob("*/README.md")):
        content = readme.read_text(encoding="utf-8")
        lines = content.splitlines()
        filtered = [
            line
            for line in lines
            if not line.startswith("name:") and not line.startswith("summary:")
        ]
        readme.write_text("\n".join(filtered) + "\n", encoding="utf-8")

    for agents in (
        manager / "AGENTS.md",
        manager / "projects/AGENTS.md",
        *sorted((manager / "projects").glob("*/AGENTS.md")),
    ):
        content = agents.read_text(encoding="utf-8")
        content = content.replace(
            "- Only an explicitly invoked UltraGoal may create or update `WORKLOG.md` for\n"
            "  detailed attempts and recovery state.",
            "- Detailed UltraGoal attempts belong in optional `WORKLOG.md`.",
        )
        content = content.replace(
            "- Update `projects/index.md` after every packet creation or lifecycle transition.",
            "- Update `projects/index.md` when creating or archiving a packet.",
        )
        content = content.replace(
            "- Only an explicitly invoked UltraGoal may create or update `WORKLOG.md`.\n"
            "- Create or update `log.md` only when sparse chronology materially improves navigation or synchronization.\n"
            "- Never mirror detailed UltraGoal WORKLOG entries into `log.md`.",
            "- Let an active UltraGoal use `WORKLOG.md` for detailed attempts; do not mirror that detail into `log.md`.\n"
            "- Create or update `log.md` only when a sparse OKF chronology materially improves navigation or synchronization.",
        )
        agents.write_text(content, encoding="utf-8")

    index_path = manager / "projects/index.md"
    packet_entries = [
        line
        for line in index_path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- [")
    ]
    index_path.write_text(
        "# Projects\n\n"
        "This index links active Project Packs.\n\n"
        "## Active Project Packs\n\n" + "\n".join(packet_entries) + "\n",
        encoding="utf-8",
    )
    commit_manager(manager, "test: create legacy v0.1 fixture")


def test_global_guidance_preserves_content_and_is_idempotent(tmp_path: Path) -> None:
    agents = tmp_path / "AGENTS.md"
    agents.write_text("# Existing rules\n\nKeep this.\n", encoding="utf-8")

    preview = json.loads(run_script(GUIDANCE, "--agents-file", str(agents)).stdout)
    assert preview["dry_run"] is True
    assert agents.read_text(encoding="utf-8") == "# Existing rules\n\nKeep this.\n"

    first = json.loads(
        run_script(GUIDANCE, "--agents-file", str(agents), "--apply").stdout
    )
    first_content = agents.read_text(encoding="utf-8")
    second = json.loads(
        run_script(GUIDANCE, "--agents-file", str(agents), "--apply").stdout
    )

    assert first["changed"] is True
    assert second["changed"] is False
    assert agents.read_text(encoding="utf-8") == first_content
    assert "# Existing rules" in first_content
    assert first_content.count("<!-- wirenet-manager:core:start -->") == 1
    assert "<!-- wirenet-manager:routing:start -->" not in first_content
    assert "$manager" in first_content
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


def test_bootstrap_materializes_content_only_manager_with_local_git(
    tmp_path: Path,
) -> None:
    destination = tmp_path / "Manager"
    preview = json.loads(
        run_script(BOOTSTRAP, "--manager-dir", str(destination)).stdout
    )
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
    for shelf in (
        "agent",
        "archive",
        "docs",
        "experiments",
        "notes",
        "outputs",
        "people",
        "projects",
        "sources",
    ):
        assert (destination / shelf).is_dir()
    assert not (destination / "templates").exists()
    assert frontmatter_value(destination / "README.md", "type") == "Manager Overview"
    assert (
        subprocess.run(
            ["git", "remote"],
            cwd=destination,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        == ""
    )
    assert (
        subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            cwd=destination,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        == "1"
    )

    metadata = json.loads(
        (destination / ".wirenet/manager.json").read_text(encoding="utf-8")
    )
    assert metadata["schema_version"] == "wirenet-manager/v0.2"
    assert metadata["project_pack_profile"] == "wirenet-project-pack/v0.1"
    assert metadata["experiment_pack_profile"] == "wirenet-experiment-pack/v0.1"
    assert metadata["plugin_version"] == "0.4.5"
    assert metadata["manager_id"].startswith("mgr_")
    assert (
        "Continue with $manager-setup for the personal first meeting."
        in applied["next_steps"]
    )

    repeated = json.loads(
        run_script(BOOTSTRAP, "--manager-dir", str(destination)).stdout
    )
    assert repeated["state"] == "healthy"
    assert repeated["doctor"]["ok"] is True


def test_bootstrap_records_selected_human_content_language(tmp_path: Path) -> None:
    destination = tmp_path / "Manager"
    preview = json.loads(
        run_script(
            BOOTSTRAP,
            "--manager-dir",
            str(destination),
            "--content-language",
            "de_DE",
        ).stdout
    )
    assert preview["content_language"] == "de-DE"
    assert "set human-readable Manager content language to de-DE" in preview[
        "actions"
    ]
    assert not destination.exists()

    applied = json.loads(
        run_script(
            BOOTSTRAP,
            "--manager-dir",
            str(destination),
            "--content-language",
            "de_DE",
            "--apply",
        ).stdout
    )
    assert applied["ok"] is True
    assert frontmatter_value(destination / "README.md", "content_language") == "de-DE"
    committed = subprocess.run(
        ["git", "show", "HEAD:README.md"],
        cwd=destination,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert 'content_language: "de-DE"' in committed


def test_bootstrap_rejects_invalid_content_language_without_writing(
    tmp_path: Path,
) -> None:
    destination = tmp_path / "Manager"
    result = run_script(
        BOOTSTRAP,
        "--manager-dir",
        str(destination),
        "--content-language",
        "german!",
        check=False,
    )
    payload = json.loads(result.stdout)
    assert result.returncode == 2
    assert payload["ok"] is False
    assert "BCP 47-style tag" in payload["error"]
    assert not destination.exists()


def test_bootstrap_runtime_preflight_stops_before_writing_without_git(
    tmp_path: Path,
) -> None:
    manager = tmp_path / "Manager"
    empty_path = tmp_path / "empty-path"
    empty_path.mkdir()
    process = run_script(
        BOOTSTRAP,
        "--manager-dir",
        str(manager),
        "--git-bin",
        str(tmp_path / "missing-git"),
        check=False,
        env={**os.environ, "PATH": str(empty_path)},
    )
    result = json.loads(process.stdout)

    assert process.returncode == 2
    assert result["state"] == "runtime-missing"
    assert result["runtime"]["python"] == sys.executable
    assert result["runtime"]["git"] is None
    assert not manager.exists()


def test_bootstrap_uses_explicit_git_when_path_has_no_developer_tools(
    tmp_path: Path,
) -> None:
    git_bin = shutil.which("git")
    assert git_bin is not None
    manager = tmp_path / "Manager"
    empty_path = tmp_path / "empty-path"
    empty_path.mkdir()
    result = json.loads(
        run_script(
            BOOTSTRAP,
            "--manager-dir",
            str(manager),
            "--git-bin",
            git_bin,
            "--apply",
            env={**os.environ, "PATH": str(empty_path)},
        ).stdout
    )

    assert result["ok"] is True
    assert result["runtime"] == {"python": sys.executable, "git": git_bin}
    assert result["doctor"]["ok"] is True
    assert (manager / ".git").is_dir()


def test_generated_project_pack_uses_created_and_updated_only(
    tmp_path: Path,
) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    workspace = tmp_path / "client-project"
    workspace.mkdir()
    project = json.loads(
        run_script(
            CREATE_PROJECT,
            "Timestamp Fixture",
            "--summary",
            "Verify the trimmed timestamp shape",
            "--workspace",
            str(workspace),
            "--manager-dir",
            str(manager),
            "--with-goal",
            "--with-result",
            "--apply",
        ).stdout
    )
    packet = Path(str(project["packet"]))
    for name in ("README.md", "GOAL.md", "RESULT.md", "AGENTS.md"):
        content = (packet / name).read_text(encoding="utf-8")
        assert frontmatter_value(Path(packet / name), "created_at") is not None
        assert frontmatter_value(Path(packet / name), "updated_at") is not None
        assert "\ntimestamp:" not in content
        assert "\nlast_edited:" not in content


def test_tidy_timestamps_reports_clean_for_freshly_generated_manager(
    tmp_path: Path,
) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    workspace = tmp_path / "client-project"
    workspace.mkdir()
    run_script(
        CREATE_PROJECT,
        "Timestamp Fixture",
        "--summary",
        "Verify the trimmed timestamp shape",
        "--workspace",
        str(workspace),
        "--manager-dir",
        str(manager),
        "--with-goal",
        "--with-result",
        "--apply",
    )

    result = json.loads(
        run_script(TIDY_TIMESTAMPS, "--manager-dir", str(manager)).stdout
    )

    assert result["ok"] is True
    assert result["dry_run"] is True
    assert result["state"] == "clean"
    assert result["candidate_paths"] == []


def test_tidy_timestamps_removes_redundant_fields_after_checkpoint(
    tmp_path: Path,
) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    workspace = tmp_path / "client-project"
    workspace.mkdir()
    project = json.loads(
        run_script(
            CREATE_PROJECT,
            "Timestamp Fixture",
            "--summary",
            "Verify the trimmed timestamp shape",
            "--workspace",
            str(workspace),
            "--manager-dir",
            str(manager),
            "--with-goal",
            "--with-result",
            "--apply",
        ).stdout
    )
    packet = Path(str(project["packet"]))
    for name in ("README.md", "GOAL.md", "RESULT.md"):
        path = packet / name
        content = path.read_text(encoding="utf-8")
        path.write_text(
            content.replace(
                "created_at: 2026",
                "timestamp: 2026-01-01T00:00:00Z\nlast_edited: 2026-01-01\ncreated_at: 2026",
                1,
            ),
            encoding="utf-8",
        )
    agents = packet / "AGENTS.md"
    agents.write_text(
        agents.read_text(encoding="utf-8").replace(
            "\n---\n\n", "\nlast_edited: 2026-01-01\n---\n\n", 1
        ),
        encoding="utf-8",
    )

    preview = json.loads(
        run_script(TIDY_TIMESTAMPS, "--manager-dir", str(manager)).stdout
    )
    assert preview["ok"] is True
    assert preview["state"] == "tidy-available"
    assert len(preview["candidate_paths"]) == 4

    blocked = run_script(
        TIDY_TIMESTAMPS, "--manager-dir", str(manager), "--apply", check=False
    )
    blocked_result = json.loads(blocked.stdout)
    assert blocked.returncode == 2
    assert blocked_result["state"] == "checkpoint-required"

    commit_manager(manager, "checkpoint before tidy")
    applied = json.loads(
        run_script(TIDY_TIMESTAMPS, "--manager-dir", str(manager), "--apply").stdout
    )
    assert applied["ok"] is True
    assert applied["state"] == "tidied"
    assert applied["doctor"]["ok"] is True
    assert sorted(applied["changed_paths"]) == sorted(
        [
            f"{packet.relative_to(manager).as_posix()}/README.md",
            f"{packet.relative_to(manager).as_posix()}/GOAL.md",
            f"{packet.relative_to(manager).as_posix()}/RESULT.md",
            f"{packet.relative_to(manager).as_posix()}/AGENTS.md",
        ]
    )

    for name in ("README.md", "GOAL.md", "RESULT.md", "AGENTS.md"):
        content = (packet / name).read_text(encoding="utf-8")
        assert "\ntimestamp:" not in content
        assert "\nlast_edited:" not in content
    created_at = frontmatter_value(packet / "README.md", "created_at")
    assert created_at is not None and re.fullmatch(r"\d{4}-\d{2}-\d{2}", created_at)
    assert (
        frontmatter_value(packet / "README.md", "schema") == "wirenet-project-pack/v0.1"
    )

    idle = json.loads(
        run_script(TIDY_TIMESTAMPS, "--manager-dir", str(manager)).stdout
    )
    assert idle["state"] == "clean"


def test_upgrade_reports_current_manager_without_writes(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    metadata_path = manager / ".wirenet/manager.json"
    before = metadata_path.read_bytes()

    result = json.loads(run_script(UPGRADE, "--manager-dir", str(manager)).stdout)

    assert result["ok"] is True
    assert result["dry_run"] is True
    assert result["state"] == "current"
    assert result["actions"] == []
    assert metadata_path.read_bytes() == before


def test_manager_update_check_reports_release_notes_without_writing(
    tmp_path: Path,
) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    release = tmp_path / "release.json"
    release.write_text(
        json.dumps(
            {
                "tag_name": "v0.4.6",
                "name": "wirenet Manager v0.4.6",
                "body": (
                    "- First user change that wraps\n"
                    "  onto a second line.\n"
                    "- Second user change.\n"
                    "- Third user change.\n"
                    "- Hidden fourth change."
                ),
                "html_url": (
                    "https://github.com/wirenet-dev/wirenet/releases/tag/v0.4.6"
                ),
            }
        ),
        encoding="utf-8",
    )
    before = subprocess.run(
        ["git", "status", "--porcelain=v1"],
        cwd=manager,
        check=True,
        capture_output=True,
        text=True,
    ).stdout

    result = json.loads(
        run_script(
            DOCTOR,
            "--manager-dir",
            str(manager),
            "--check-updates",
            "--release-json",
            str(release),
        ).stdout
    )

    assert result["ok"] is True
    assert result["update"] == {
        "ok": True,
        "state": "available",
        "current_version": "0.4.5",
        "latest_version": "0.4.6",
        "update_available": True,
        "release_name": "wirenet Manager v0.4.6",
        "release_notes": [
            "First user change that wraps onto a second line.",
            "Second user change.",
            "Third user change.",
        ],
        "release_url": (
            "https://github.com/wirenet-dev/wirenet/releases/tag/v0.4.6"
        ),
        "update_command": "codex plugin marketplace upgrade wirenet",
        "post_update_action": "Start a fresh task and run $manager-setup.",
    }
    after = subprocess.run(
        ["git", "status", "--porcelain=v1"],
        cwd=manager,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert after == before


def test_manager_update_check_is_non_blocking_when_release_is_unavailable(
    tmp_path: Path,
) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    release = tmp_path / "release.json"
    release.write_text("{}", encoding="utf-8")

    result = json.loads(
        run_script(
            DOCTOR,
            "--manager-dir",
            str(manager),
            "--check-updates",
            "--release-json",
            str(release),
        ).stdout
    )

    assert result["ok"] is True
    assert result["update"]["ok"] is False
    assert result["update"]["state"] == "unavailable"
    assert result["update"]["update_available"] is False


def test_manager_update_script_reports_current_release(tmp_path: Path) -> None:
    release = tmp_path / "release.json"
    release.write_text(
        json.dumps(
            {
                "tag_name": "v0.4.5",
                "name": "wirenet Manager v0.4.5",
                "body": "- Current release.",
                "html_url": (
                    "https://github.com/wirenet-dev/wirenet/releases/tag/v0.4.5"
                ),
            }
        ),
        encoding="utf-8",
    )

    result = json.loads(
        run_script(UPDATE_CHECK, "--release-json", str(release)).stdout
    )

    assert result["state"] == "current"
    assert result["current_version"] == "0.4.5"
    assert result["latest_version"] == "0.4.5"
    assert result["update_available"] is False


def test_upgrade_migrates_v01_without_rewriting_personal_content(
    tmp_path: Path,
) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    workspace = tmp_path / "client-project"
    ignored = tmp_path / "scratch"
    workspace.mkdir()
    ignored.mkdir()
    project = json.loads(
        run_script(
            CREATE_PROJECT,
            "Migration Fixture",
            "--summary",
            "Preserve this packet",
            "--workspace",
            str(workspace),
            "--manager-dir",
            str(manager),
            "--apply",
        ).stdout
    )
    run_script(IGNORE, str(ignored), "--manager-dir", str(manager), "--apply")
    readme = manager / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8") + "\nPersonal migration marker.\n",
        encoding="utf-8",
    )
    make_legacy_v01_manager(manager)

    preview = json.loads(run_script(UPGRADE, "--manager-dir", str(manager)).stdout)
    assert preview["ok"] is True
    assert preview["state"] == "upgrade-available"
    assert preview["git_clean"] is True
    assert not (manager / ".wirenet/workspace-bindings.json").exists()

    applied = json.loads(
        run_script(UPGRADE, "--manager-dir", str(manager), "--apply").stdout
    )
    assert applied["ok"] is True
    assert applied["state"] == "upgraded"
    assert applied["doctor"]["ok"] is True
    assert applied["next_action"] == "review and commit the local Manager migration"

    metadata = json.loads(
        (manager / ".wirenet/manager.json").read_text(encoding="utf-8")
    )
    assert metadata["schema_version"] == "wirenet-manager/v0.2"
    assert metadata["plugin_version"] == "0.4.5"
    assert metadata["experiment_pack_profile"] == "wirenet-experiment-pack/v0.1"
    assert metadata["okf_profiles"] == [
        "wirenet-okf-project-pack/v0.1",
        "wirenet-okf-experiment-pack/v0.1",
    ]
    assert "okf_profile" not in metadata

    registry = json.loads(
        (manager / ".wirenet/workspace-bindings.json").read_text(encoding="utf-8")
    )
    assert registry["projects"] == [
        {"project_id": project["project_id"], "path": str(workspace.resolve())}
    ]
    assert registry["experiments"] == []
    assert registry["ignored"] == [{"path": str(ignored.resolve())}]
    assert not (manager / ".wirenet/project-bindings.json").exists()
    assert (
        manager / ".wirenet/migrations/wirenet-manager-v0.1/project-bindings.json"
    ).is_file()
    assert "Personal migration marker." in readme.read_text(encoding="utf-8")
    packet_readme = Path(str(project["packet"])) / "README.md"
    assert frontmatter_value(packet_readme, "name") == "Migration Fixture"
    assert frontmatter_value(packet_readme, "summary") == "Preserve this packet"
    assert "Only an explicitly invoked UltraGoal" in (
        Path(str(project["packet"])) / "AGENTS.md"
    ).read_text(encoding="utf-8")
    index = (manager / "projects/index.md").read_text(encoding="utf-8")
    for heading in (
        "## Active Project Packs",
        "## Waiting And Blocked",
        "## Completed Project Packs",
        "## Archived Project Packs",
    ):
        assert heading in index
    assert (
        json.loads(run_script(DOCTOR, "--manager-dir", str(manager)).stdout)["ok"]
        is True
    )
    assert subprocess.run(
        ["git", "status", "--porcelain=v1"],
        cwd=manager,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def test_upgrade_stops_before_ambiguous_legacy_experiment_route(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    experiment = tmp_path / "legacy-spike"
    experiment.mkdir()
    make_legacy_v01_manager(manager, experiment_route=experiment)
    metadata_path = manager / ".wirenet/manager.json"
    legacy_path = manager / ".wirenet/project-bindings.json"
    before = {
        metadata_path: metadata_path.read_bytes(),
        legacy_path: legacy_path.read_bytes(),
    }

    rejected = run_script(
        UPGRADE,
        "--manager-dir",
        str(manager),
        "--apply",
        check=False,
    )
    result = json.loads(rejected.stdout)

    assert rejected.returncode == 2
    assert result["state"] == "manual-review"
    assert result["manual_paths"] == [str(experiment.resolve())]
    assert {path: path.read_bytes() for path in before} == before
    assert not (manager / ".wirenet/workspace-bindings.json").exists()


def test_bootstrap_routes_legacy_manager_to_clean_checkpoint_gate(
    tmp_path: Path,
) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    make_legacy_v01_manager(manager)
    todo = manager / "TODO.md"
    todo.write_text(
        todo.read_text(encoding="utf-8") + "\n- [ ] Uncommitted personal task.\n",
        encoding="utf-8",
    )

    bootstrap_result = run_script(
        BOOTSTRAP,
        "--manager-dir",
        str(manager),
        check=False,
    )
    routed = json.loads(bootstrap_result.stdout)
    assert bootstrap_result.returncode == 2
    assert routed["state"] == "upgrade-available"
    assert routed["upgrade"]["git_clean"] is False

    rejected = run_script(
        UPGRADE,
        "--manager-dir",
        str(manager),
        "--apply",
        check=False,
    )
    result = json.loads(rejected.stdout)
    assert rejected.returncode == 2
    assert result["state"] == "checkpoint-required"
    assert "Uncommitted personal task." in todo.read_text(encoding="utf-8")
    assert not (manager / ".wirenet/workspace-bindings.json").exists()


def test_upgrade_requires_newer_plugin_for_newer_workspace_schema(
    tmp_path: Path,
) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    metadata_path = manager / ".wirenet/manager.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["schema_version"] = "wirenet-manager/v0.3"
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    rejected = run_script(UPGRADE, "--manager-dir", str(manager), check=False)
    result = json.loads(rejected.stdout)
    assert rejected.returncode == 2
    assert result["state"] == "plugin-too-old"
    assert "update wirenet Manager" in result["error"]


def test_repair_fills_an_empty_existing_manager_without_overwrite(
    tmp_path: Path,
) -> None:
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
        run_script(
            BOOTSTRAP, "--manager-dir", str(manager), "--repair", "--apply"
        ).stdout
    )
    assert repaired["state"] == "repaired"
    assert repaired["doctor"]["ok"] is True
    assert existing.read_text(encoding="utf-8") == "keep me"
    assert not (manager / ".git").exists()


def test_project_pack_is_open_and_supports_optional_concepts_and_local_routing(
    tmp_path: Path,
) -> None:
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
    assert frontmatter_value(child_packet / "AGENTS.md", "type") is None
    assert (
        frontmatter_value(child_packet / "AGENTS.md", "schema")
        == "wirenet-runtime/v0.1"
    )
    assert frontmatter_value(child_packet / "AGENTS.md", "audience") == "agent"
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
    assert not index.startswith("---")
    assert index.endswith("\n")
    assert "[Client](client/README.md) — Parent packet" in index
    assert "[Campaign](campaign/README.md) — Nested packet" in index
    assert not (manager / "projects/README.md").exists()
    registry = json.loads(
        (manager / ".wirenet/workspace-bindings.json").read_text(encoding="utf-8")
    )
    assert {row["path"] for row in registry["projects"]} == {
        str(parent.resolve()),
        str(child.resolve()),
    }

    result = json.loads(
        run_script(
            INSPECT, "--manager-dir", str(manager), "--workspace", str(child / "edit")
        ).stdout
    )
    assert result["classification"] == "tracked"
    assert result["project_id"] == child_result["project_id"]
    assert result["project_packet"].endswith("projects/campaign")

    ignored = child / "scratch"
    ignored.mkdir()
    run_script(
        IGNORE,
        str(ignored),
        "--manager-dir",
        str(manager),
        "--apply",
    )
    repeated_route = json.loads(
        run_script(
            IGNORE,
            str(ignored),
            "--manager-dir",
            str(manager),
            "--apply",
        ).stdout
    )
    assert repeated_route["changed"] is False
    routed = json.loads(
        run_script(
            INSPECT, "--manager-dir", str(manager), "--workspace", str(ignored)
        ).stdout
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
    assert any(
        "NOTE.md is missing a non-empty OKF type" in error
        for error in diagnosis["errors"]
    )


def test_manager_doctor_rejects_untyped_markdown_in_any_knowledge_shelf(
    tmp_path: Path,
) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    (manager / "notes/idea.md").write_text(
        "# Idea\n\nUntyped drift.\n", encoding="utf-8"
    )

    diagnosis = json.loads(
        run_script(DOCTOR, "--manager-dir", str(manager), check=False).stdout
    )
    assert diagnosis["ok"] is False
    assert "notes/idea.md is missing a non-empty OKF type" in diagnosis["errors"]


def test_fresh_manager_markdown_has_one_canonical_role(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)

    for path in manager.rglob("*.md"):
        if ".git" in path.parts or ".wirenet" in path.parts or "outputs" in path.parts:
            continue
        concept_type = frontmatter_value(path, "type")
        if path.name == "AGENTS.md":
            assert concept_type is None
            assert frontmatter_value(path, "schema") == "wirenet-runtime/v0.1"
        elif path.name in {"index.md", "log.md"}:
            assert concept_type is None
        else:
            assert concept_type, path


def test_manager_doctor_rejects_local_template_shelf(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    (manager / "templates").mkdir()

    diagnosis = json.loads(
        run_script(DOCTOR, "--manager-dir", str(manager), check=False).stdout
    )
    assert diagnosis["ok"] is False
    assert (
        "templates is not part of the canonical v0.2 workspace" in diagnosis["errors"]
    )


def test_manager_doctor_rejects_typed_runtime_instructions(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    agents = manager / "AGENTS.md"
    agents.write_text(
        agents.read_text(encoding="utf-8").replace(
            'schema: "wirenet-runtime/v0.1"',
            'schema: "wirenet-runtime/v0.1"\ntype: "Runtime Instruction"',
        ),
        encoding="utf-8",
    )

    diagnosis = json.loads(
        run_script(DOCTOR, "--manager-dir", str(manager), check=False).stdout
    )
    assert diagnosis["ok"] is False
    assert (
        "AGENTS.md must remain outside the OKF concept projection"
        in diagnosis["errors"]
    )


def test_person_generator_is_dry_run_first_and_creates_typed_context(
    tmp_path: Path,
) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)

    preview = json.loads(
        run_script(
            CREATE_PERSON,
            "Alex Example",
            "--context",
            "Alex owns the final review for the launch.",
            "--manager-dir",
            str(manager),
        ).stdout
    )
    path = Path(str(preview["path"]))
    assert preview["dry_run"] is True
    assert not path.exists()

    applied = json.loads(
        run_script(
            CREATE_PERSON,
            "Alex Example",
            "--context",
            "Alex owns the final review for the launch.",
            "--manager-dir",
            str(manager),
            "--apply",
        ).stdout
    )
    assert applied["ok"] is True
    assert path.is_file()
    content = path.read_text(encoding="utf-8")
    assert frontmatter_value(path, "type") == "Person"
    assert frontmatter_value(path, "schema") == "wirenet-manager/v0.2"
    assert frontmatter_value(path, "title") == "Alex Example"
    assert "Alex owns the final review for the launch." in content
    assert "## Context" in content

    duplicate = run_script(
        CREATE_PERSON,
        "Alex Example",
        "--context",
        "Must not overwrite the existing concept.",
        "--manager-dir",
        str(manager),
        "--apply",
        check=False,
    )
    assert duplicate.returncode == 2
    assert "already exists" in duplicate.stdout
    assert "Must not overwrite" not in path.read_text(encoding="utf-8")

    diagnosis = json.loads(run_script(DOCTOR, "--manager-dir", str(manager)).stdout)
    assert diagnosis["ok"] is True


def test_project_preview_and_rejected_overlap_are_side_effect_free(
    tmp_path: Path,
) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    tracked_paths = (
        manager / "projects/index.md",
        manager / ".wirenet/workspace-bindings.json",
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


def test_manager_native_project_needs_no_device_binding(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    created = json.loads(
        run_script(
            CREATE_PROJECT,
            "Native Project",
            "--summary",
            "Work performed directly in Manager",
            "--manager-dir",
            str(manager),
            "--apply",
        ).stdout
    )

    registry = json.loads(
        (manager / ".wirenet/workspace-bindings.json").read_text(encoding="utf-8")
    )
    assert registry["projects"] == []
    packet = Path(str(created["packet"]))
    inspection = json.loads(
        run_script(
            INSPECT,
            "--manager-dir",
            str(manager),
            "--workspace",
            str(packet / "working-note"),
        ).stdout
    )
    assert inspection["classification"] == "tracked"
    assert inspection["manager_native"] is True
    assert inspection["project_id"] == created["project_id"]


def test_experiment_can_be_bound_promoted_and_completed_as_project(
    tmp_path: Path,
) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    workspace = tmp_path / "spike"
    workspace.mkdir()

    experiment = json.loads(
        run_script(
            CREATE_EXPERIMENT,
            "Routing Spike",
            "--question",
            "Does the route work?",
            "--decision-criterion",
            "The Manager Doctor passes",
            "--workspace",
            str(workspace),
            "--manager-dir",
            str(manager),
            "--apply",
        ).stdout
    )
    experiment_packet = Path(str(experiment["packet"]))
    assert {path.name for path in experiment_packet.iterdir()} == {
        "README.md",
        "AGENTS.md",
    }
    assert frontmatter_value(experiment_packet / "README.md", "status") == "active"
    assert "Routing Spike" in (manager / "experiments/index.md").read_text(
        encoding="utf-8"
    )

    inspection = json.loads(
        run_script(
            INSPECT,
            "--manager-dir",
            str(manager),
            "--workspace",
            str(workspace / "trial"),
        ).stdout
    )
    assert inspection["classification"] == "experiment"
    assert inspection["experiment_id"] == experiment["experiment_id"]

    promoted = json.loads(
        run_script(
            PROMOTE_EXPERIMENT,
            "routing-spike",
            "--project-name",
            "Routing Product",
            "--summary",
            "Durable routing work",
            "--manager-dir",
            str(manager),
            "--apply",
        ).stdout
    )
    project_packet = Path(str(promoted["project_packet"]))
    assert frontmatter_value(experiment_packet / "README.md", "status") == "promoted"
    assert (
        frontmatter_value(project_packet / "README.md", "source_experiment_id")
        == experiment["experiment_id"]
    )
    assert "../../projects/routing-product/README.md" in experiment_packet.joinpath(
        "README.md"
    ).read_text(encoding="utf-8")
    assert "../../experiments/routing-spike/README.md" in project_packet.joinpath(
        "README.md"
    ).read_text(encoding="utf-8")

    registry = json.loads(
        (manager / ".wirenet/workspace-bindings.json").read_text(encoding="utf-8")
    )
    assert registry["experiments"] == []
    assert registry["projects"] == [
        {"project_id": promoted["project_id"], "path": str(workspace.resolve())}
    ]

    transitioned = json.loads(
        run_script(
            TRANSITION,
            "project",
            "routing-product",
            "--to",
            "completed",
            "--manager-dir",
            str(manager),
            "--apply",
        ).stdout
    )
    assert transitioned["changed"] is True
    assert frontmatter_value(project_packet / "README.md", "status") == "completed"
    assert "Routing Product" in (manager / "projects/index.md").read_text(
        encoding="utf-8"
    )
    assert (
        json.loads(run_script(DOCTOR, "--manager-dir", str(manager)).stdout)["ok"]
        is True
    )


def test_invalid_lifecycle_transition_is_side_effect_free(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    experiment = json.loads(
        run_script(
            CREATE_EXPERIMENT,
            "Archived Spike",
            "--question",
            "Can this be skipped?",
            "--decision-criterion",
            "No",
            "--manager-dir",
            str(manager),
            "--apply",
        ).stdout
    )
    packet = Path(str(experiment["packet"]))
    run_script(
        TRANSITION,
        "experiment",
        "archived-spike",
        "--to",
        "archived",
        "--manager-dir",
        str(manager),
        "--apply",
    )
    before = packet.joinpath("README.md").read_bytes()
    rejected = run_script(
        TRANSITION,
        "experiment",
        "archived-spike",
        "--to",
        "concluded",
        "--manager-dir",
        str(manager),
        "--apply",
        check=False,
    )
    assert rejected.returncode == 2
    assert "invalid experiment transition" in json.loads(rejected.stdout)["error"]
    assert packet.joinpath("README.md").read_bytes() == before


def test_worklog_is_reserved_for_explicit_ultragoal_state(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    project = json.loads(
        run_script(
            CREATE_PROJECT,
            "Persistent Goal",
            "--summary",
            "Requires durable attempts",
            "--manager-dir",
            str(manager),
            "--apply",
        ).stdout
    )
    packet = Path(str(project["packet"]))
    packet.joinpath("WORKLOG.md").write_text(
        "\n".join(
            [
                "---",
                'type: "Project Note"',
                'schema: "wirenet-project-pack/v0.1"',
                f'project_id: "{project["project_id"]}"',
                "---",
                "",
                "# Worklog",
                "",
            ]
        ),
        encoding="utf-8",
    )
    diagnosis = json.loads(
        run_script(DOCTOR, "--manager-dir", str(manager), check=False).stdout
    )
    assert any(
        "WORKLOG.md must use OKF type Goal Worklog" in error
        for error in diagnosis["errors"]
    )
    assert any(
        "WORKLOG.md must declare producer ultragoal" in error
        for error in diagnosis["errors"]
    )


def test_doctor_rejects_out_of_packet_worklog_and_malformed_binding(
    tmp_path: Path,
) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    manager.joinpath("notes/WORKLOG.md").write_text(
        "\n".join(
            [
                "---",
                'type: "Goal Worklog"',
                'producer: "ultragoal"',
                "---",
                "",
                "# Misrouted Worklog",
                "",
            ]
        ),
        encoding="utf-8",
    )
    registry_path = manager / ".wirenet/workspace-bindings.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["ignored"] = [{"path": "relative/path"}]
    registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")

    diagnosis = json.loads(
        run_script(DOCTOR, "--manager-dir", str(manager), check=False).stdout
    )
    assert (
        "notes/WORKLOG.md is reserved for UltraGoal state in a Project Pack"
        in diagnosis["errors"]
    )
    assert (
        "workspace-bindings.json ignored[0] path must be absolute"
        in diagnosis["errors"]
    )


def test_manager_doctor_detects_project_index_drift(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    result = json.loads(
        run_script(
            CREATE_PROJECT,
            "Index Drift",
            "--summary",
            "Must appear in the canonical index",
            "--manager-dir",
            str(manager),
            "--apply",
        ).stdout
    )
    index = manager / "projects/index.md"
    entry = (
        "- [Index Drift](index-drift/README.md) — Must appear in the canonical index\n"
    )
    index.write_text(
        index.read_text(encoding="utf-8").replace(entry, ""), encoding="utf-8"
    )

    diagnosis = json.loads(
        run_script(DOCTOR, "--manager-dir", str(manager), check=False).stdout
    )
    assert diagnosis["ok"] is False
    assert any(
        "projects/index-drift: packet is missing from projects/index.md" in error
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
        "all projects packet files must share one project_id" in error
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
    assert any(
        "log.md date headings must be newest first" in error
        for error in diagnosis["errors"]
    )


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


def test_workspace_inspection_uses_only_canonical_bindings(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    bootstrap(manager)
    workspace = tmp_path / "unbound-workspace"
    workspace.mkdir()
    created = json.loads(
        run_script(
            CREATE_PROJECT,
            "Binding Only",
            "--summary",
            "Only bindings may classify a workspace",
            "--manager-dir",
            str(manager),
            "--apply",
        ).stdout
    )
    readme = Path(str(created["packet"])) / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8").replace(
            "title:", f'workspace_paths:\n  - "{workspace}"\ntitle:', 1
        ),
        encoding="utf-8",
    )

    result = json.loads(
        run_script(
            INSPECT, "--manager-dir", str(manager), "--workspace", str(workspace)
        ).stdout
    )
    assert result["classification"] == "untracked"
