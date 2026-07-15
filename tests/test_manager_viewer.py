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


def extract_bundle(html: str) -> dict[str, object]:
    match = re.search(r"window\.BUNDLE = (?P<bundle>\{.*?\});\n</script>", html, re.DOTALL)
    assert match is not None
    return json.loads(match.group("bundle"))


def test_viewer_contains_manager_documents_with_audience_and_routing(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    write_concept(
        manager / "AGENTS.md",
        concept_type="Runtime Adapter",
        title="Manager Instructions",
        body="Read the nested instructions.",
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
    write_concept(
        manager / "projects/alpha/AGENTS.md",
        concept_type="Runtime Adapter",
        title="Alpha Agent Instructions",
        body="RENDER_AGENT_INSTRUCTIONS_IN_AGENT_OR_ALL_MODE",
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

    assert "Viewer documents: 8" in result.stdout
    html = output.read_text(encoding="utf-8")
    bundle = extract_bundle(html)
    nodes = {node["data"]["path"] for node in bundle["nodes"]}
    assert nodes == {
        "AGENTS.md",
        "README.md",
        "notes/decision.md",
        "notes/private.md",
        "projects/alpha/AGENTS.md",
        "projects/alpha/GOAL.md",
        "projects/alpha/README.md",
        "projects/alpha/log.md",
    }
    assert "DO_NOT_RENDER_UNTYPED" in html
    assert "DO_NOT_RENDER_SKILLS" not in html
    assert "DO_NOT_RENDER_HIDDEN_STATE" not in html
    assert "RENDER_AGENT_INSTRUCTIONS_IN_AGENT_OR_ALL_MODE" in html
    assert "DO_NOT_RENDER_TEMPLATES" not in html
    assert "RENDER_TYPED_DOCUMENTS" in html
    assert str(manager) not in html
    assert "projects/index.md" not in html
    assert 'id="graph"' in html
    assert 'id="detail"' in html
    assert 'id="show-agent"' in html
    assert 'id="reading-mode"' in html
    assert 'id="document-select"' not in html
    assert 'id="view-mode"' not in html
    assert 'id="audience-filter"' not in html

    edge_kinds = {edge["data"]["kind"] for edge in bundle["edges"]}
    assert edge_kinds == {"link", "routing"}
    assert len(bundle["edges"]) == 2

    node_data = {node["data"]["path"]: node["data"] for node in bundle["nodes"]}
    assert node_data["AGENTS.md"]["audience"] == "agent"
    assert node_data["projects/alpha/AGENTS.md"]["audience"] == "agent"
    routing = next(edge["data"] for edge in bundle["edges"] if edge["data"]["kind"] == "routing")
    assert (routing["source"], routing["target"]) == (
        "AGENTS",
        "projects/alpha/AGENTS",
    )


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

    nodes = {node["data"]["path"]: node["data"] for node in bundle["nodes"]}
    assert f"Viewer documents: {len(nodes)}" in result.stdout
    assert nodes["projects/empty-project/AGENTS.md"]["audience"] == "agent"
    assert nodes["projects/empty-project/README.md"]["audience"] == "human"
    assert "projects/empty-project/GOAL.md" not in nodes
    assert "projects/empty-project/RESULT.md" not in nodes
    assert "projects/empty-project/log.md" not in nodes
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

    assert {node["data"]["path"] for node in bundle["nodes"]} == {
        "projects/alpha/README.md",
        "projects/alpha/RESULT.md",
        "projects/alpha/log.md",
    }


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
        node["data"]["path"]
        for node in bundle["nodes"]
        if node["data"]["path"].startswith("projects/useful-project/")
    }
    assert project_paths == {
        "projects/useful-project/AGENTS.md",
        "projects/useful-project/README.md",
    }
    assert "Ship the prototype." in bodies
    assert "Describe the latest durable state" in bodies
    assert "Add the smallest useful next action" in bodies
    assert "## Current Status" in bodies
    assert "## Next Move" in bodies


def test_explicit_audience_marks_an_instruction_document(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
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

    assert [node["data"]["path"] for node in bundle["nodes"]] == ["people/alex.md"]
    assert bundle["nodes"][0]["data"]["audience"] == "agent"


def test_agent_routing_uses_the_nearest_parent_instructions(tmp_path: Path) -> None:
    manager = tmp_path / "Manager"
    for path, title in (
        ("AGENTS.md", "Manager Instructions"),
        ("projects/AGENTS.md", "Project Instructions"),
        ("projects/alpha/AGENTS.md", "Alpha Instructions"),
    ):
        write_concept(
            manager / path,
            concept_type="Runtime Adapter",
            title=title,
            body="Routing instructions.",
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
    routes = {
        (edge["data"]["source"], edge["data"]["target"])
        for edge in bundle["edges"]
        if edge["data"]["kind"] == "routing"
    }

    assert routes == {
        ("AGENTS", "projects/AGENTS"),
        ("projects/AGENTS", "projects/alpha/AGENTS"),
    }


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
