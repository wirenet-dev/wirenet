from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VIEWER = ROOT / "plugins/wirenet-manager/scripts/generate_manager_viewer.py"


def write_concept(
    path: Path,
    *,
    concept_type: str,
    title: str,
    body: str,
    project_id: str = "",
) -> None:
    project_line = f'project_id: "{project_id}"\n' if project_id else ""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        f'type: "{concept_type}"\n'
        'schema: "wirenet-manager/v0.1"\n'
        f'{project_line}'
        f'title: "{title}"\n'
        "status: active\n"
        "last_edited: 2026-07-15\n"
        "---\n\n"
        f"# {title}\n\n{body}\n",
        encoding="utf-8",
    )


def extract_bundle(html: str) -> dict[str, object]:
    match = re.search(r"window\.BUNDLE = (?P<bundle>\{.*?\});\n</script>", html, re.DOTALL)
    assert match is not None
    return json.loads(match.group("bundle"))


def test_viewer_contains_only_okf_content_and_reserved_navigation(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    write_concept(
        manager / "README.md",
        concept_type="Manager Overview",
        title="Manager",
        body="Private work memory.",
    )
    write_concept(
        manager / "projects/alpha/GOAL.md",
        concept_type="Project Brief",
        title="Alpha Goal",
        project_id="prj_alpha",
        body="Ship Alpha.",
    )
    write_concept(
        manager / "projects/alpha/README.md",
        concept_type="Project Status",
        title="Alpha Status",
        project_id="prj_alpha",
        body="Read the [goal](GOAL.md).",
    )
    (manager / "projects/index.md").write_text(
        "# Projects\n\n- [Alpha](alpha/README.md)\n", encoding="utf-8"
    )
    (manager / "projects/alpha/log.md").write_text(
        "# Update Log\n\n## 2026-07-15\n\n- **Creation**: Started.\n",
        encoding="utf-8",
    )
    (manager / "notes/private.md").parent.mkdir(parents=True)
    (manager / "notes/private.md").write_text(
        "# Not OKF\n\nDO_NOT_RENDER_UNTYPED\n", encoding="utf-8"
    )
    write_concept(
        manager / "skills/fake/SKILL.md",
        concept_type="Runtime Adapter",
        title="Fake Skill",
        body="DO_NOT_RENDER_SKILLS",
    )
    write_concept(
        manager / ".wirenet/private.md",
        concept_type="Secret",
        title="Hidden State",
        body="DO_NOT_RENDER_HIDDEN_STATE",
    )

    output = tmp_path / "viewer.html"
    result = subprocess.run(
        [sys.executable, str(VIEWER), "--manager-dir", str(manager), "--out", str(output)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "OKF concepts: 5" in result.stdout
    html = output.read_text(encoding="utf-8")
    bundle = extract_bundle(html)
    nodes = {node["data"]["path"] for node in bundle["nodes"]}
    assert nodes == {
        "README.md",
        "projects/index.md",
        "projects/alpha/GOAL.md",
        "projects/alpha/README.md",
        "projects/alpha/log.md",
    }
    assert "DO_NOT_RENDER_UNTYPED" not in html
    assert "DO_NOT_RENDER_SKILLS" not in html
    assert "DO_NOT_RENDER_HIDDEN_STATE" not in html
    assert str(manager) not in html

    edge_kinds = {edge["data"]["kind"] for edge in bundle["edges"]}
    assert edge_kinds == {"link", "packet"}


def test_viewer_rejects_links_that_escape_the_manager(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    write_concept(
        manager / "projects/alpha/README.md",
        concept_type="Project Status",
        title="Alpha Status",
        body="Do not follow [outside](../../../outside.md).",
    )
    write_concept(
        tmp_path / "outside.md",
        concept_type="Project Status",
        title="Outside",
        body="Outside the Manager.",
    )

    output = tmp_path / "viewer.html"
    subprocess.run(
        [sys.executable, str(VIEWER), "--manager-dir", str(manager), "--out", str(output)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    bundle = extract_bundle(output.read_text(encoding="utf-8"))

    assert bundle["edges"] == []
    assert "outside.md" in next(iter(bundle["bodies"].values()))
