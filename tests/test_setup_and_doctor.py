"""End-to-end: materialize a Manager, wire it, and let the doctor judge it."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SETUP_SCRIPTS = ROOT / "plugins" / "wirenet" / "skills" / "manager-setup" / "scripts"
BOOTSTRAP = SETUP_SCRIPTS / "bootstrap_manager.py"
GUIDANCE = SETUP_SCRIPTS / "install_global_guidance.py"
DOCTOR = ROOT / "plugins" / "wirenet" / "scripts" / "doctor.py"


def run(script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(script), *args], capture_output=True, text=True
    )


def bootstrap(target: Path, *extra: str) -> dict:
    result = run(BOOTSTRAP, "--manager-dir", str(target), *extra)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_bootstrap_is_dry_run_first_and_never_overwrites(tmp_path: Path) -> None:
    target = tmp_path / "Manager"
    data = bootstrap(target, "--dry-run")
    assert data["ok"] and data["dry_run"]
    assert not target.exists()

    data = bootstrap(target)
    assert data["ok"] and (target / "AGENTS.md").is_file()
    assert data["git_initialized"] and data["committed"]

    (target / "README.md").write_text("# Mine\n", encoding="utf-8")
    data = bootstrap(target)
    assert "README.md" in data["skipped_existing"]
    assert (target / "README.md").read_text(encoding="utf-8") == "# Mine\n"


def test_bootstrap_refuses_a_nested_manager(tmp_path: Path) -> None:
    outer = tmp_path / "Manager"
    bootstrap(outer)
    result = run(BOOTSTRAP, "--manager-dir", str(outer / "inner"))
    data = json.loads(result.stdout)
    assert not data["ok"]
    assert "refusing to nest" in data["error"]


def test_doctor_calls_a_fresh_manager_healthy(tmp_path: Path) -> None:
    target = tmp_path / "Manager"
    bootstrap(target)
    result = run(DOCTOR, "--manager-dir", str(target), "--json")
    data = json.loads(result.stdout)
    assert result.returncode == 0, result.stdout
    assert data["ok"] and not data["errors"]
    info = [f for f in data["findings"] if f["check"] == "orientation-budget-info"]
    assert info, "doctor must report the orientation read"
    lines = int(info[0]["detail"].split(":")[1].split()[0])
    assert lines <= 250, f"fresh seed busts the orientation budget: {lines}"


def test_doctor_flags_unlisted_and_oversized_packs(tmp_path: Path) -> None:
    target = tmp_path / "Manager"
    bootstrap(target)
    pack = target / "projects" / "big"
    pack.mkdir(parents=True)
    (pack / "README.md").write_text(
        "# Big\n" + "line\n" * 130, encoding="utf-8"
    )
    result = run(DOCTOR, "--manager-dir", str(target), "--json")
    data = json.loads(result.stdout)
    assert result.returncode == 0
    checks = {f["check"] for f in data["findings"]}
    assert "index" in checks, "unlisted pack must be a finding"
    assert "pack-size" in checks, "oversized pack must be a finding"


def test_global_guidance_is_idempotent_and_removable(tmp_path: Path) -> None:
    target = tmp_path / "CLAUDE.md"
    target.write_text("# Mine\n", encoding="utf-8")

    run(GUIDANCE, "--file", str(target))
    text = target.read_text(encoding="utf-8")
    assert text.count("wirenet-manager:start") == 1
    assert text.startswith("# Mine")

    run(GUIDANCE, "--file", str(target))
    assert target.read_text(encoding="utf-8").count("wirenet-manager:start") == 1

    run(GUIDANCE, "--file", str(target), "--remove")
    assert "wirenet-manager" not in target.read_text(encoding="utf-8")
