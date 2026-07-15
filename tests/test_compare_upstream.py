from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/compare_upstream.py"


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )


def commit(repo: Path, message: str) -> None:
    git(repo, "add", ".")
    git(
        repo,
        "-c",
        "user.name=WireNet Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "-qm",
        message,
    )


def test_compare_upstream_reports_both_sides_and_worktree(tmp_path: Path) -> None:
    source = tmp_path / "source"
    downstream = tmp_path / "downstream"
    source.mkdir()
    git(source, "init", "-q", "-b", "main")
    (source / "base.txt").write_text("base\n", encoding="utf-8")
    commit(source, "base")

    subprocess.run(["git", "clone", "-q", str(source), str(downstream)], check=True)
    git(downstream, "remote", "rename", "origin", "upstream")

    (downstream / "wire.txt").write_text("wire\n", encoding="utf-8")
    commit(downstream, "wire change")
    (source / "upstream.txt").write_text("upstream\n", encoding="utf-8")
    commit(source, "upstream change")
    (downstream / "local.txt").write_text("local\n", encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--repo",
            str(downstream),
            "--fetch",
            "--json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)

    assert result["ahead"] == 1
    assert result["behind"] == 1
    assert result["upstream_commits"][0].endswith("upstream change")
    assert result["wirenet_commits"][0].endswith("wire change")
    assert "A\twire.txt" in result["committed_delta"]
    assert "?? local.txt" in result["worktree_delta"]
