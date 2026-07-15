from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VIEWER = ROOT / "plugins/wirenet-manager/scripts/generate_manager_viewer.py"
BOOTSTRAP = ROOT / "plugins/wirenet-manager/skills/wirenet-manager-bootstrap/scripts/bootstrap_manager.py"
CREATE_PROJECT = ROOT / "plugins/wirenet-manager/scripts/create_project_pack.py"


def write_concept(
    path: Path,
    *,
    concept_type: str,
    title: str,
    body: str,
    project_id: str = "",
    audience: str = "",
) -> None:
    project_line = f'project_id: "{project_id}"\n' if project_id else ""
    audience_line = f'audience: "{audience}"\n' if audience else ""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        f'type: "{concept_type}"\n'
        'schema: "wirenet-manager/v0.1"\n'
        f'{project_line}'
        f'{audience_line}'
        f'title: "{title}"\n'
        "status: active\n"
        "last_edited: 2026-07-15\n"
        "---\n\n"
        f"# {title}\n\n{body}\n",
        encoding="utf-8",
    )


def write_runtime(path: Path, *, title: str, body: str, project_id: str = "") -> None:
    project_line = f'project_id: "{project_id}"\n' if project_id else ""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        'schema: "wirenet-runtime/v0.1"\n'
        f"{project_line}"
        f'title: "{title}"\n'
        "audience: agent\n"
        "visibility: local\n"
        "last_edited: 2026-07-15\n"
        "---\n\n"
        f"# {title}\n\n{body}\n",
        encoding="utf-8",
    )


def extract_bundle(html: str) -> dict[str, object]:
    match = re.search(r"window\.BUNDLE = (?P<bundle>\{.*?\});\n</script>", html, re.DOTALL)
    assert match is not None
    return json.loads(match.group("bundle"))


def test_inspector_matches_google_graph_model_and_excludes_reserved_runtime(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    write_runtime(
        manager / "AGENTS.md",
        title="Manager Instructions",
        body="DO_NOT_RENDER_RUNTIME",
    )
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
        "# Projects\n\nDO_NOT_RENDER_INDEX\n\n- [Alpha](alpha/README.md)\n", encoding="utf-8"
    )
    (manager / "projects/alpha/log.md").write_text(
        "# Update Log\n\nDO_NOT_RENDER_LOG\n\n## 2026-07-15\n\n- **Creation**: Started.\n",
        encoding="utf-8",
    )
    (manager / "notes/private.md").parent.mkdir(parents=True)
    (manager / "notes/private.md").write_text(
        "# Not OKF\n\nDO_NOT_RENDER_UNTYPED\n", encoding="utf-8"
    )
    write_concept(
        manager / "skills/fake/SKILL.md",
        concept_type="Procedure",
        title="Fake Skill",
        body="DO_NOT_RENDER_SKILLS",
    )
    write_concept(
        manager / ".wirenet/private.md",
        concept_type="Secret",
        title="Hidden State",
        body="DO_NOT_RENDER_HIDDEN_STATE",
    )
    write_runtime(
        manager / "projects/alpha/AGENTS.md",
        title="Alpha Agent Instructions",
        body="DO_NOT_RENDER_PROJECT_RUNTIME",
        project_id="prj_alpha",
    )
    write_concept(
        manager / "templates/README.md",
        concept_type="Project Status",
        title="Template",
        body="DO_NOT_RENDER_TEMPLATES",
    )
    write_concept(
        manager / "notes/decision.md",
        concept_type="Decision",
        title="Internal Decision",
        body="RENDER_TYPED_DOCUMENTS",
    )

    output = tmp_path / "viewer.html"
    result = subprocess.run(
        [sys.executable, str(VIEWER), "--manager-dir", str(manager), "--out", str(output)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Inspector concepts: 4" in result.stdout
    html = output.read_text(encoding="utf-8")
    bundle = extract_bundle(html)
    nodes = {node["data"]["id"] for node in bundle["nodes"]}
    assert nodes == {
        "README",
        "notes/decision",
        "projects/alpha/GOAL",
        "projects/alpha/README",
    }
    assert "DO_NOT_RENDER_RUNTIME" not in html
    assert "DO_NOT_RENDER_PROJECT_RUNTIME" not in html
    assert "DO_NOT_RENDER_UNTYPED" not in html
    assert "DO_NOT_RENDER_SKILLS" not in html
    assert "DO_NOT_RENDER_HIDDEN_STATE" not in html
    assert "DO_NOT_RENDER_TEMPLATES" not in html
    assert "DO_NOT_RENDER_INDEX" not in html
    assert "DO_NOT_RENDER_LOG" not in html
    assert "RENDER_TYPED_DOCUMENTS" in html
    assert str(manager) not in html
    assert set(bundle) == {"nodes", "edges", "bodies", "types", "palette"}
    assert set(bundle["bodies"]) == {
        "README",
        "notes/decision",
        "projects/alpha/GOAL",
        "projects/alpha/README",
    }
    assert "WireNet Inspector" in html
    assert 'id="graph"' in html
    assert 'id="detail"' in html
    assert 'id="search"' in html
    assert 'id="filter-type"' in html
    assert 'id="layout"' in html
    assert 'id="reset"' in html
    assert 'id="browse"' not in html
    assert 'id="reading-mode"' not in html

    assert bundle["edges"] == [
        {
            "data": {
                "id": "projects/alpha/README__projects/alpha/GOAL",
                "source": "projects/alpha/README",
                "target": "projects/alpha/GOAL",
            }
        }
    ]


def test_fresh_project_keeps_complete_source_documents(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    subprocess.run(
        [sys.executable, str(BOOTSTRAP), "--manager-dir", str(manager), "--apply"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    subprocess.run(
        [
            sys.executable,
            str(CREATE_PROJECT),
            "Empty Project",
            "--summary",
            "",
            "--workspace",
            str(workspace),
            "--manager-dir",
            str(manager),
            "--apply",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    output = tmp_path / "viewer.html"
    result = subprocess.run(
        [sys.executable, str(VIEWER), "--manager-dir", str(manager), "--out", str(output)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    bundle = extract_bundle(output.read_text(encoding="utf-8"))

    nodes = {node["data"]["id"]: node["data"] for node in bundle["nodes"]}
    assert f"Inspector concepts: {len(nodes)}" in result.stdout
    assert "projects/empty-project/AGENTS" not in nodes
    assert nodes["README"]["type"] == "Manager Overview"
    assert nodes["projects/empty-project/README"]["type"] == "Project Status"
    assert "projects/empty-project/GOAL" not in nodes
    assert "projects/empty-project/RESULT" not in nodes
    assert "projects/empty-project/log" not in nodes
    assert "index" not in bundle["bodies"]
    assert "projects/index" not in bundle["bodies"]
    bodies = "\n".join(bundle["bodies"].values())
    assert "Describe the latest durable state" in bodies
    assert "Add the smallest useful next action" in bodies


def test_substantive_project_content_appears_without_metadata_toggle(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    write_concept(
        manager / "projects/alpha/README.md",
        concept_type="Project Status",
        title="Alpha Status",
        project_id="prj_alpha",
        body="The prototype is ready for review.",
    )
    write_concept(
        manager / "projects/alpha/RESULT.md",
        concept_type="Project Result",
        title="Alpha Results",
        project_id="prj_alpha",
        body="The prototype passed the mobile review.",
    )
    (manager / "projects/alpha/log.md").write_text(
        "# Update Log\n\n## 2026-07-15\n\n- **Delivery**: Prototype approved.\n",
        encoding="utf-8",
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

    assert {node["data"]["id"] for node in bundle["nodes"]} == {
        "projects/alpha/README",
        "projects/alpha/RESULT",
    }
    assert "projects/alpha/log" not in bundle["bodies"]
    assert "Prototype approved" not in "\n".join(bundle["bodies"].values())
    assert "prototype passed the mobile review" in bundle["bodies"]["projects/alpha/RESULT"]


def test_viewer_does_not_filter_sections_from_generated_documents(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    subprocess.run(
        [sys.executable, str(BOOTSTRAP), "--manager-dir", str(manager), "--apply"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    subprocess.run(
        [
            sys.executable,
            str(CREATE_PROJECT),
            "Useful Project",
            "--summary",
            "Ship the prototype.",
            "--workspace",
            str(workspace),
            "--manager-dir",
            str(manager),
            "--apply",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
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
    bodies = "\n".join(bundle["bodies"].values())

    project_paths = {
        node["data"]["id"]
        for node in bundle["nodes"]
        if node["data"]["id"].startswith("projects/useful-project/")
    }
    assert project_paths == {
        "projects/useful-project/README",
    }
    assert "Ship the prototype." in bodies
    assert "Describe the latest durable state" in bodies
    assert "Add the smallest useful next action" in bodies
    assert "## Current Status" in bodies
    assert "## Next Move" in bodies


def test_type_frontmatter_is_the_explicit_concept_boundary(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    (manager / "README.md").parent.mkdir(parents=True)
    (manager / "README.md").write_text(
        "---\nlast_edited: 2026-07-15\n---\n\n# Workspace Guide\n",
        encoding="utf-8",
    )
    write_concept(
        manager / "people/alex.md",
        concept_type="Person",
        title="Alex",
        body="Alex owns the final review.",
        audience="agent",
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

    assert [node["data"]["id"] for node in bundle["nodes"]] == ["people/alex"]
    assert bundle["nodes"][0]["data"]["type"] == "Person"
    assert bundle["nodes"][0]["data"]["label"] == "Alex"
    assert "README" not in bundle["bodies"]


def test_graph_uses_only_standard_markdown_links_between_concepts(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    write_concept(
        manager / "projects/alpha/README.md",
        concept_type="Project Status",
        title="Alpha",
        body="See the [goal](GOAL.md). A wiki link [[RESULT]] is not OKF graph syntax.",
    )
    write_concept(
        manager / "projects/alpha/GOAL.md",
        concept_type="Project Brief",
        title="Goal",
        body="Ship Alpha.",
    )
    write_concept(
        manager / "projects/alpha/RESULT.md",
        concept_type="Project Result",
        title="Result",
        body="Not linked with standard Markdown.",
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
    assert bundle["edges"] == [
        {
            "data": {
                "id": "projects/alpha/README__projects/alpha/GOAL",
                "source": "projects/alpha/README",
                "target": "projects/alpha/GOAL",
            }
        }
    ]


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
