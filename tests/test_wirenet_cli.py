from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "bin/wirenet"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_init_base_is_dry_run_first(tmp_path: Path) -> None:
    config = tmp_path / "runtime/installation.json"
    target = tmp_path / "base"

    result = run_cli(
        "--config",
        str(config),
        "init",
        "base",
        "--path",
        str(target),
        "--owner",
        "acme",
        "--installation-id",
        "inst_acme",
    )

    assert result.returncode == 0
    assert "WireNet init preview" in result.stdout
    assert "result: no changes" in result.stdout
    assert not target.exists()
    assert not config.exists()


def test_init_base_materializes_seed_and_origin_manifest(tmp_path: Path) -> None:
    config = tmp_path / "runtime/installation.json"
    target = tmp_path / "base"

    result = run_cli(
        "init",
        "base",
        "--config",
        str(config),
        "--path",
        str(target),
        "--owner",
        "acme",
        "--installation-id",
        "inst_acme",
        "--apply",
    )

    assert result.returncode == 0, result.stderr
    assert (target / "index.md").is_file()
    installation = json.loads(config.read_text(encoding="utf-8"))
    assert installation["schema_version"] == "wirenet-installation/v0.1"
    assert installation["installation_id"] == "inst_acme"
    assert installation["owner"] == "acme"
    assert installation["elements"]["base"]["path"] == str(target)
    manifest = json.loads(
        (target / ".wirenet/instance.json").read_text(encoding="utf-8")
    )
    assert manifest == {
        "element": "base",
        "installation_id": "inst_acme",
        "origin": {
            "repository": "https://github.com/wirenet-dev/wirenet.git",
            "template_version": "0.1.0",
        },
        "owner": "acme",
        "schema_version": "wirenet-instance/v0.1",
    }


def test_init_refuses_a_nonempty_target(tmp_path: Path) -> None:
    config = tmp_path / "installation.json"
    target = tmp_path / "base"
    target.mkdir()
    (target / "customer.md").write_text("keep\n", encoding="utf-8")

    result = run_cli(
        "--config",
        str(config),
        "init",
        "base",
        "--path",
        str(target),
        "--apply",
    )

    assert result.returncode == 1
    assert "result: blocked" in result.stdout
    assert (target / "customer.md").read_text(encoding="utf-8") == "keep\n"
    assert not config.exists()


def test_status_uses_configured_paths_and_manager_bindings(tmp_path: Path) -> None:
    manager = tmp_path / "personal-manager"
    base = tmp_path / "company-base"
    shelf = tmp_path / "company-shelf"
    for path in (manager, base, shelf):
        path.mkdir()
    runtime = manager / ".wirenet"
    runtime.mkdir()
    (runtime / "workspace-bindings.json").write_text(
        json.dumps({"projects": [], "experiments": [], "ignored": []}) + "\n",
        encoding="utf-8",
    )
    config = tmp_path / "installation.json"
    config.write_text(
        json.dumps(
            {
                "schema_version": "wirenet-installation/v0.1",
                "installation_id": "inst_acme",
                "owner": "acme",
                "elements": {
                    "manager": {"path": str(manager)},
                    "base": {"path": str(base)},
                    "shelf": {"path": str(shelf)},
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )

    result = run_cli("status", "--config", str(config))

    assert result.returncode == 0, result.stderr
    assert "installation: inst_acme — owner acme" in result.stdout
    assert f"Manager: {manager}" in result.stdout
    assert f"Base: {base}" in result.stdout
    assert f"Shelf: {shelf}" in result.stdout
    assert "bindings: 0/0 resolve" in result.stdout
