from __future__ import annotations

import datetime as dt
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ONBOARDING_SCRIPTS = ROOT / ".codex" / "skills" / "onboarding" / "scripts"
NEW_PROJECT = ROOT / ".codex" / "skills" / "new-project" / "scripts" / "new_project.py"
NEW_PERSON = ROOT / ".codex" / "skills" / "new-person" / "scripts" / "new_person.py"


def load_validator():
    path = ROOT / "scripts" / "validate_markdown.py"
    spec = importlib.util.spec_from_file_location("validate_markdown", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_script(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"missing frontmatter: {path}"
    _, raw, _ = text.split("---", 2)
    data: dict[str, object] = {}
    for line in raw.splitlines():
        if not line.strip() or line[0].isspace():
            continue
        key, separator, value = line.partition(":")
        assert separator, f"frontmatter line must be key/value: {path}: {line}"
        data[key.strip()] = value.strip().strip('"\'')
    return data


def assert_valid_generated_markdown(vault: Path) -> None:
    assert load_validator().validate_tree(vault) == []
    markdown = sorted(vault.rglob("*.md"))
    assert markdown
    for path in markdown:
        relative = path.relative_to(vault)
        if path.name == "SKILL.md" and "plugins" in relative.parts and "skills" in relative.parts:
            continue
        value = frontmatter(path).get("last_edited")
        try:
            dt.date.fromisoformat(str(value))
        except ValueError:
            raise AssertionError(f"invalid last_edited: {path}: {value!r}") from None


def test_fresh_setup_project_and_person_generate_valid_markdown(tmp_path: Path) -> None:
    run_script(
        ONBOARDING_SCRIPTS / "setup_shared_memory_vault.py",
        "--vault-dir",
        str(tmp_path),
    )
    run_script(
        ONBOARDING_SCRIPTS / "new_project_note.py",
        "--vault-dir",
        str(tmp_path),
        "--title",
        "Disposable Project",
    )
    run_script(
        ONBOARDING_SCRIPTS / "new_person_note.py",
        "--vault-dir",
        str(tmp_path),
        "--name",
        "Disposable Person",
    )

    assert_valid_generated_markdown(tmp_path)


def test_partial_setup_preserves_existing_files_and_repeat_is_idempotent(tmp_path: Path) -> None:
    personalized = "---\nlast_edited: 2026-07-01\n---\n\n# Personal rules\n"
    (tmp_path / "AGENTS.md").write_text(personalized, encoding="utf-8")

    setup = ONBOARDING_SCRIPTS / "setup_shared_memory_vault.py"
    run_script(setup, "--vault-dir", str(tmp_path))
    first_snapshot = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }
    second = run_script(setup, "--vault-dir", str(tmp_path))
    second_snapshot = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }

    assert (tmp_path / "AGENTS.md").read_text(encoding="utf-8") == personalized
    assert first_snapshot == second_snapshot
    assert json.loads(second.stdout)["created_files"] == []
    assert_valid_generated_markdown(tmp_path)


def test_standalone_generators_share_schemas_and_update_router(tmp_path: Path) -> None:
    template_root = tmp_path / "template"
    shutil.copytree(ROOT, template_root, ignore=shutil.ignore_patterns(".git", ".pytest_cache", "__pycache__"))

    run_script(
        template_root / ".codex" / "skills" / "new-project" / "scripts" / "new_project.py",
        "Canonical Project",
        "--summary",
        "A durable test project.",
        "--vault-dir",
        str(template_root),
    )
    run_script(
        template_root / ".codex" / "skills" / "new-person" / "scripts" / "new_person.py",
        "Canonical Person",
        "--role",
        "Test collaborator",
        "--vault-dir",
        str(template_root),
    )

    router = (template_root / "projects" / "README.md").read_text(encoding="utf-8")
    assert router.count("[[projects/canonical-project/README|Canonical Project]]") == 1
    project = template_root / "projects" / "canonical-project" / "README.md"
    person = template_root / "people" / "canonical-person.md"
    assert set(frontmatter(project)) >= {"title", "status", "created_at", "updated_at", "last_edited"}
    assert set(frontmatter(person)) >= {"title", "created_at", "updated_at", "last_edited"}
    assert "## Current Status" in project.read_text(encoding="utf-8")
    assert "## Snapshot" in person.read_text(encoding="utf-8")
    assert_valid_generated_markdown(template_root)


def test_doctor_repairs_missing_scaffold_without_rewriting_custom_content(tmp_path: Path) -> None:
    custom = "---\nlast_edited: 2026-07-01\n---\n\n# Keep me\n"
    (tmp_path / "TODO.md").write_text(custom, encoding="utf-8")
    doctor = ONBOARDING_SCRIPTS / "vault_doctor.py"

    before = json.loads(run_script(doctor, "--vault-dir", str(tmp_path)).stdout)
    assert before["ok"] is False
    assert not (tmp_path / "AGENTS.md").exists()

    repaired = json.loads(
        run_script(doctor, "--vault-dir", str(tmp_path), "--repair").stdout
    )
    assert repaired["ok"] is True
    assert (tmp_path / "TODO.md").read_text(encoding="utf-8") == custom
    assert (tmp_path / "notes" / ".gitkeep").exists()
    assert (tmp_path / "sources" / ".gitkeep").exists()


def test_canonical_shelves_survive_a_git_clone(tmp_path: Path) -> None:
    source = tmp_path / "source"
    clone = tmp_path / "clone"
    (source / "notes").mkdir(parents=True)
    (source / "sources").mkdir()
    shutil.copy2(ROOT / "notes" / ".gitkeep", source / "notes" / ".gitkeep")
    shutil.copy2(ROOT / "sources" / ".gitkeep", source / "sources" / ".gitkeep")
    subprocess.run(["git", "init", "-q"], cwd=source, check=True)
    subprocess.run(["git", "add", "."], cwd=source, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=Vault Test",
            "-c",
            "user.email=vault-test@example.invalid",
            "commit",
            "-qm",
            "fixture",
        ],
        cwd=source,
        check=True,
    )
    subprocess.run(["git", "clone", "-q", str(source), str(clone)], check=True)

    assert (clone / "notes").is_dir()
    assert (clone / "sources").is_dir()


def test_migration_copy_excludes_transient_files_and_reconciles_scaffold(tmp_path: Path) -> None:
    source = tmp_path / "old-vault"
    destination = tmp_path / "new-vault"
    (source / "people").mkdir(parents=True)
    (source / "people" / "custom.md").write_text(
        "---\nlast_edited: 2026-07-01\n---\n\n# Custom\n",
        encoding="utf-8",
    )
    (source / "__pycache__").mkdir()
    (source / "__pycache__" / "stale.cpython-313.pyc").write_bytes(b"old absolute path")
    (source / "MIGRATION_HANDOFF.md").write_text("temporary", encoding="utf-8")
    migration = ONBOARDING_SCRIPTS / "migrate_vault.py"

    planned = json.loads(
        run_script(
            migration,
            "--source",
            str(source),
            "--destination",
            str(destination),
        ).stdout
    )
    assert planned["dry_run"] is True
    assert not destination.exists()

    applied = json.loads(
        run_script(
            migration,
            "--source",
            str(source),
            "--destination",
            str(destination),
            "--apply",
        ).stdout
    )
    assert applied["ok"] is True
    assert (destination / "people" / "custom.md").exists()
    assert not (destination / "__pycache__").exists()
    assert not (destination / "MIGRATION_HANDOFF.md").exists()
    assert applied["automation_handoffs"] == "manual verification required"
    assert json.loads(run_script(ONBOARDING_SCRIPTS / "vault_doctor.py", "--vault-dir", str(destination)).stdout)["ok"] is True
