from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANAGER_QMD = ROOT / "plugins/wirenet-manager/scripts/manager_qmd.py"


def write_state(path: Path, **overrides: object) -> None:
    state: dict[str, object] = {
        "healthy": True,
        "collections": {},
        "contexts": {},
        "embed_calls": [],
    }
    state.update(overrides)
    path.write_text(json.dumps(state), encoding="utf-8")


def fake_qmd_source() -> str:
    return f"""#!{sys.executable}
import json
import os
import sys

state_path = os.environ["FAKE_QMD_STATE"]

def load():
    with open(state_path, encoding="utf-8") as handle:
        return json.load(handle)

def save(state):
    with open(state_path, "w", encoding="utf-8") as handle:
        json.dump(state, handle)

args = sys.argv[1:]
state = load()

if args == ["--version"]:
    print("qmd 2.5.3 (test)")
elif args == ["doctor"]:
    if state.get("healthy"):
        print("QMD Doctor: ready")
    else:
        print("QMD Doctor: unhealthy", file=sys.stderr)
        raise SystemExit(1)
elif args[:2] == ["collection", "show"]:
    name = args[2]
    collection = state["collections"].get(name)
    if not collection:
        print(f"Collection not found: {{name}}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Collection: {{name}}")
    print(f"  Path:     {{collection['path']}}")
    print(f"  Pattern:  {{collection['pattern']}}")
elif args[:2] == ["collection", "list"]:
    print(f"Collections ({{len(state['collections'])}}):\\n")
    for name, collection in state["collections"].items():
        print(f"{{name}} (qmd://{{name}}/)")
        print(f"  Pattern:  {{collection['pattern']}}")
        if collection.get("ignore"):
            print(f"  Ignore:   {{', '.join(collection['ignore'])}}")
        print()
elif args[:2] == ["collection", "add"]:
    path = args[2]
    name = args[args.index("--name") + 1]
    pattern = args[args.index("--mask") + 1]
    state["collections"][name] = {{"path": path, "pattern": pattern}}
    save(state)
    print(f"Collection '{{name}}' created successfully")
elif args[:2] == ["context", "add"]:
    name = args[2].removeprefix("qmd://").rstrip("/")
    state["contexts"][name] = args[3]
    save(state)
    print("Context added")
elif args and args[0] == "embed":
    name = args[args.index("-c") + 1]
    state["embed_calls"].append(name)
    save(state)
    print("Embedded")
else:
    print(f"Unexpected fake qmd command: {{args}}", file=sys.stderr)
    raise SystemExit(2)
"""


def make_fake_qmd(path: Path) -> Path:
    path.write_text(fake_qmd_source(), encoding="utf-8")
    path.chmod(0o755)
    return path


def run_manager_qmd(
    manager: Path,
    *args: str,
    env: dict[str, str],
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(MANAGER_QMD),
            "--manager-dir",
            str(manager),
            *args,
        ],
        cwd=ROOT,
        env=env,
        check=check,
        capture_output=True,
        text=True,
    )


def test_qmd_preview_detects_missing_installation_without_mutation(
    tmp_path: Path,
) -> None:
    manager = tmp_path / "Manager"
    manager.mkdir()
    missing = tmp_path / "missing-qmd"

    result = json.loads(
        run_manager_qmd(
            manager,
            "--qmd-bin",
            str(missing),
            env=os.environ.copy(),
        ).stdout
    )

    assert result["ok"] is True
    assert result["dry_run"] is True
    assert result["state"] == "qmd-missing"
    assert result["install_required"] is True
    assert "--install --apply" in result["next_action"]


def test_qmd_setup_registers_only_manager_knowledge_and_is_idempotent(
    tmp_path: Path,
) -> None:
    manager = tmp_path / "Manager"
    manager.mkdir()
    state_path = tmp_path / "qmd-state.json"
    write_state(state_path)
    qmd = make_fake_qmd(tmp_path / "qmd")
    env = {**os.environ, "FAKE_QMD_STATE": str(state_path)}

    applied = json.loads(
        run_manager_qmd(
            manager,
            "--qmd-bin",
            str(qmd),
            "--embed",
            "--apply",
            env=env,
        ).stdout
    )
    state = json.loads(state_path.read_text(encoding="utf-8"))

    assert applied["ok"] is True
    assert applied["state"] == "ready"
    assert state["collections"]["manager"]["path"] == str(manager.resolve())
    pattern = state["collections"]["manager"]["pattern"]
    assert "!(*AGENTS).md" in pattern
    assert "outputs" not in pattern
    assert "Runtime AGENTS" in state["contexts"]["manager"]
    assert state["embed_calls"] == ["manager"]

    repeated = json.loads(
        run_manager_qmd(
            manager,
            "--qmd-bin",
            str(qmd),
            env=env,
        ).stdout
    )
    assert repeated["ok"] is True
    assert repeated["state"] == "ready"
    assert repeated["dry_run"] is True


def test_qmd_setup_preserves_conflicting_collection(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    manager.mkdir()
    other = tmp_path / "Other"
    other.mkdir()
    state_path = tmp_path / "qmd-state.json"
    write_state(
        state_path,
        collections={
            "manager": {"path": str(other.resolve()), "pattern": "**/*.md"}
        },
    )
    qmd = make_fake_qmd(tmp_path / "qmd")
    env = {**os.environ, "FAKE_QMD_STATE": str(state_path)}

    process = run_manager_qmd(
        manager,
        "--qmd-bin",
        str(qmd),
        "--apply",
        env=env,
        check=False,
    )
    result = json.loads(process.stdout)

    assert process.returncode == 2
    assert result["state"] == "collection-name-conflict"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["collections"]["manager"]["path"] == str(other.resolve())


def test_qmd_setup_preserves_same_path_custom_pattern_with_warning(
    tmp_path: Path,
) -> None:
    manager = tmp_path / "Manager"
    manager.mkdir()
    state_path = tmp_path / "qmd-state.json"
    write_state(
        state_path,
        collections={
            "manager": {"path": str(manager.resolve()), "pattern": "**/*.md"}
        },
    )
    qmd = make_fake_qmd(tmp_path / "qmd")
    env = {**os.environ, "FAKE_QMD_STATE": str(state_path)}

    result = json.loads(
        run_manager_qmd(
            manager,
            "--qmd-bin",
            str(qmd),
            env=env,
        ).stdout
    )

    assert result["ok"] is True
    assert result["state"] == "ready-custom"
    assert "custom pattern" in result["warning"]


def test_qmd_setup_accepts_equivalent_ignore_boundary(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    manager.mkdir()
    state_path = tmp_path / "qmd-state.json"
    write_state(
        state_path,
        collections={
            "manager": {
                "path": str(manager.resolve()),
                "pattern": "**/*.md",
                "ignore": ["**/AGENTS.md", "outputs/**", "templates/**"],
            }
        },
    )
    qmd = make_fake_qmd(tmp_path / "qmd")
    env = {**os.environ, "FAKE_QMD_STATE": str(state_path)}

    result = json.loads(
        run_manager_qmd(
            manager,
            "--qmd-bin",
            str(qmd),
            env=env,
        ).stdout
    )

    assert result["state"] == "ready"
    assert "warning" not in result


def test_qmd_setup_can_install_pinned_package_after_approval(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    manager.mkdir()
    state_path = tmp_path / "qmd-state.json"
    write_state(state_path)
    qmd_template = make_fake_qmd(tmp_path / "qmd-template")
    prefix = tmp_path / "npm-prefix"
    npm = tmp_path / "npm"
    npm.write_text(
        f"""#!{sys.executable}
import os
import shutil
import sys
from pathlib import Path

prefix = Path(os.environ["FAKE_NPM_PREFIX"])
if sys.argv[1:] == ["prefix", "-g"]:
    print(prefix)
elif sys.argv[1:3] == ["install", "-g"]:
    target = prefix / "bin/qmd"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(os.environ["FAKE_QMD_TEMPLATE"], target)
    target.chmod(0o755)
else:
    raise SystemExit(2)
""",
        encoding="utf-8",
    )
    npm.chmod(0o755)
    env = {
        **os.environ,
        "PATH": str(tmp_path / "empty-bin"),
        "FAKE_NPM_PREFIX": str(prefix),
        "FAKE_QMD_TEMPLATE": str(qmd_template),
        "FAKE_QMD_STATE": str(state_path),
    }

    applied = json.loads(
        run_manager_qmd(
            manager,
            "--npm-bin",
            str(npm),
            "--install",
            "--apply",
            env=env,
        ).stdout
    )

    assert applied["ok"] is True
    assert applied["qmd"]["version"] == "qmd 2.5.3 (test)"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["collections"]["manager"]["path"] == str(manager.resolve())


def test_qmd_setup_can_use_bundled_pnpm_without_shell_configuration(
    tmp_path: Path,
) -> None:
    manager = tmp_path / "Manager"
    manager.mkdir()
    state_path = tmp_path / "qmd-state.json"
    write_state(state_path)
    qmd_template = make_fake_qmd(tmp_path / "qmd-template")
    npm_template = tmp_path / "npm-template"
    npm_template.write_text(
        f"""#!{sys.executable}
import os
import shutil
import sys
from pathlib import Path

prefix = Path(sys.argv[sys.argv.index("--prefix") + 1])
target = prefix / "bin/qmd"
target.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(os.environ["FAKE_QMD_TEMPLATE"], target)
target.chmod(0o755)
""",
        encoding="utf-8",
    )
    npm_template.chmod(0o755)
    pnpm_home = tmp_path / "pnpm-home"
    qmd_prefix = tmp_path / "qmd-prefix"
    pnpm = tmp_path / "pnpm"
    pnpm.write_text(
        f"""#!{sys.executable}
import os
import shutil
import sys
from pathlib import Path

home = Path(os.environ["PNPM_HOME"])
bin_dir = home / "bin"
if sys.argv[1:3] == ["add", "-g"]:
    target = bin_dir / "npm"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(os.environ["FAKE_NPM_TEMPLATE"], target)
    target.chmod(0o755)
else:
    raise SystemExit(2)
""",
        encoding="utf-8",
    )
    pnpm.chmod(0o755)
    env = {
        **os.environ,
        "PATH": str(tmp_path / "empty-bin"),
        "PNPM_HOME": str(pnpm_home),
        "WIRENET_QMD_PREFIX": str(qmd_prefix),
        "FAKE_NPM_TEMPLATE": str(npm_template),
        "FAKE_QMD_TEMPLATE": str(qmd_template),
        "FAKE_QMD_STATE": str(state_path),
    }

    applied = json.loads(
        run_manager_qmd(
            manager,
            "--pnpm-bin",
            str(pnpm),
            "--install",
            "--apply",
            env=env,
        ).stdout
    )

    assert applied["ok"] is True
    assert applied["package_manager"]["kind"] == "pnpm"
    assert applied["package_manager"]["bootstraps"] == "npm@11.18.0"
    assert applied["qmd"]["version"] == "qmd 2.5.3 (test)"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["collections"]["manager"]["path"] == str(manager.resolve())
