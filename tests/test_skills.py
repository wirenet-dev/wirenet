from __future__ import annotations

import importlib.util
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
