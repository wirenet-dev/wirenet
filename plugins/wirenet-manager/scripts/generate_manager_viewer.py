#!/usr/bin/env python3
"""Generate or serve the read-only WireNet Manager OKF viewer."""

from __future__ import annotations

import argparse
import json
import os
import posixpath
import re
import tempfile
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote, urlsplit


DEFAULT_PORT = 4318
MAX_MARKDOWN_BYTES = 2_000_000
INDEX_NAME = "index.md"
IGNORED_DIRECTORIES = {
    ".git",
    ".obsidian",
    ".wirenet",
    ".codex",
    ".agents",
    "node_modules",
    "dist",
    ".next",
    ".turbo",
    "assets",
    "plugins",
    "scripts",
    "skills",
    "tests",
    "templates",
    "outputs",
    "viewer",
}
MARKDOWN_EXTENSIONS = {".md", ".markdown"}
FRONTMATTER_RE = re.compile(r"\A---\s*\n(?P<meta>.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
HEADING_RE = re.compile(r"(?m)^#\s+(.+?)\s*$")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\)")
WIKI_LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]")

TYPE_PALETTE = {
    "Manager Overview": "#262626",
    "Task Stack": "#ff5c1a",
    "Project Brief": "#ff5c1a",
    "Project Status": "#2f8fce",
    "Project Result": "#23855c",
    "Runtime Adapter": "#737373",
    "Person": "#7c5cc4",
    "Decision": "#b1507c",
    "OKF Log": "#c2841a",
    "Document": "#8a8a8a",
}
DEFAULT_NODE_COLOR = "#8a8a8a"
AGENT_AUDIENCES = {"agent", "machine", "system"}
AGENT_CONCEPT_TYPES = {"Runtime Adapter"}


@dataclass
class Concept:
    path: str
    concept_id: str
    concept_type: str
    title: str
    description: str
    resource: str
    tags: list[str]
    body: str
    audience: str
    outgoing: list[str] = field(default_factory=list)

    def to_node(self) -> dict[str, Any]:
        return {
            "data": {
                "id": self.concept_id,
                "label": self.title,
                "type": self.concept_type,
                "description": self.description,
                "resource": self.resource,
                "tags": self.tags,
                "path": self.path,
                "audience": self.audience,
                "color": TYPE_PALETTE.get(self.concept_type, DEFAULT_NODE_COLOR),
                "size": 30 + min(54, len(self.body) // 220),
            }
        }


def parse_frontmatter(raw: str) -> tuple[dict[str, Any], str]:
    match = FRONTMATTER_RE.match(raw)
    if not match:
        return {}, raw
    metadata: dict[str, Any] = {}
    for line in match.group("meta").splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        if re.fullmatch(r"[A-Za-z0-9_-]+", key):
            metadata[key] = parse_scalar(raw_value.strip())
    return metadata, raw[match.end() :]


def parse_scalar(value: str) -> Any:
    if not value:
        return ""
    if value.startswith(("\"", "'")) and value.endswith(value[0]):
        if value[0] == "\"":
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [] if not inner else [str(parse_scalar(item.strip())) for item in inner.split(",")]
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if lowered in {"null", "none", "~"}:
        return None
    return value


def title_from(path: str, body: str, metadata: dict[str, Any]) -> str:
    if metadata.get("title"):
        return str(metadata["title"])
    heading = HEADING_RE.search(body)
    if heading:
        return heading.group(1).strip()
    return Path(path).stem.replace("-", " ").replace("_", " ").title()


def description_from(body: str, metadata: dict[str, Any]) -> str:
    if metadata.get("description"):
        return str(metadata["description"])
    paragraphs: list[str] = []
    in_fence = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if (
            in_fence
            or not stripped
            or stripped.startswith(("#", "-", "*", ">", "|"))
            or (line[:1].isspace() and not paragraphs)
        ):
            if paragraphs:
                break
            continue
        paragraphs.append(stripped)
        if len(" ".join(paragraphs)) >= 180:
            break
    return " ".join(paragraphs)[:220]


def tags_from(metadata: dict[str, Any]) -> list[str]:
    value = metadata.get("tags", metadata.get("tag", []))
    if isinstance(value, list):
        values = value
    elif isinstance(value, str):
        values = re.split(r"[,\s]+", value)
    else:
        values = []
    return sorted({str(item).lstrip("#").strip() for item in values if str(item).strip()})


def document_audience(path: PurePosixPath, concept_type: str, metadata: dict[str, Any]) -> str:
    explicit = str(metadata.get("audience") or "").strip().lower()
    if explicit in AGENT_AUDIENCES:
        return "agent"
    if explicit in {"human", "people", "user"}:
        return "human"
    if path.name.lower() == "agents.md" or concept_type in AGENT_CONCEPT_TYPES:
        return "agent"
    return "human"


def iter_markdown(manager_dir: Path) -> list[Path]:
    paths: list[Path] = []
    for root, directories, files in os.walk(manager_dir):
        directories[:] = sorted(
            name
            for name in directories
            if name not in IGNORED_DIRECTORIES and not name.startswith(".")
        )
        root_path = Path(root)
        for name in sorted(files):
            path = root_path / name
            if path.suffix.lower() not in MARKDOWN_EXTENSIONS or path.name.lower() == INDEX_NAME:
                continue
            try:
                if path.stat().st_size <= MAX_MARKDOWN_BYTES:
                    paths.append(path)
            except OSError:
                continue
    return paths


def read_manager_documents(manager_dir: Path) -> list[Concept]:
    concepts: list[Concept] = []
    for path in iter_markdown(manager_dir):
        try:
            raw = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        metadata, body = parse_frontmatter(raw)
        relative_path = path.relative_to(manager_dir).as_posix()
        relative = PurePosixPath(relative_path)
        concept_type = str(metadata.get("type") or "").strip()
        if relative.name.lower() == "log.md":
            concept_type = concept_type or "OKF Log"
        elif relative.name.lower() == "agents.md":
            concept_type = concept_type or "Runtime Adapter"
        else:
            concept_type = concept_type or "Document"
        concepts.append(
            Concept(
                path=relative_path,
                concept_id=str(relative.with_suffix("")),
                concept_type=concept_type,
                title=title_from(relative_path, body, metadata),
                description=description_from(body, metadata),
                resource=str(metadata.get("resource") or ""),
                tags=tags_from(metadata),
                body=body,
                audience=document_audience(relative, concept_type, metadata),
            )
        )
    resolve_links(concepts)
    return concepts


def build_path_lookup(concepts: list[Concept]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    aliases: dict[str, set[str]] = {}
    for concept in concepts:
        path = PurePosixPath(concept.path)
        without_suffix = str(path.with_suffix(""))
        lookup[concept.path.lower()] = concept.concept_id
        lookup[without_suffix.lower()] = concept.concept_id
        aliases.setdefault(path.name.lower(), set()).add(concept.concept_id)
        aliases.setdefault(path.stem.lower(), set()).add(concept.concept_id)
    for alias, concept_ids in aliases.items():
        if len(concept_ids) == 1:
            lookup[alias] = next(iter(concept_ids))
    return lookup


def resolve_target(source_path: str, target: str, lookup: dict[str, str]) -> str | None:
    parsed = urlsplit(unquote(target))
    if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith("#"):
        return None
    source_dir = posixpath.dirname(source_path)
    candidate = (
        parsed.path.removeprefix("/")
        if parsed.path.startswith("/")
        else posixpath.join(source_dir, parsed.path)
    )
    normalized = posixpath.normpath(candidate)
    if normalized in {".", ".."} or normalized.startswith(("../", "/")):
        return None
    variants = [normalized, normalized.removesuffix(".md"), normalized.removesuffix(".markdown")]
    if not PurePosixPath(normalized).suffix:
        variants.append(f"{normalized}.md")
    for variant in variants:
        match = lookup.get(variant.lower())
        if match:
            return match
    return None


def resolve_links(concepts: list[Concept]) -> None:
    lookup = build_path_lookup(concepts)
    for concept in concepts:
        outgoing: list[str] = []
        for match in MARKDOWN_LINK_RE.finditer(concept.body):
            target = resolve_target(concept.path, match.group(2), lookup)
            if target and target != concept.concept_id and target not in outgoing:
                outgoing.append(target)
        for match in WIKI_LINK_RE.finditer(concept.body):
            target = resolve_target(concept.path, match.group(1), lookup)
            if not target:
                target = lookup.get(match.group(1).strip().lower())
            if target and target != concept.concept_id and target not in outgoing:
                outgoing.append(target)
        concept.outgoing = outgoing
        concept.body = normalize_internal_links(concept, lookup)


def normalize_internal_links(concept: Concept, lookup: dict[str, str]) -> str:
    def replace_markdown(match: re.Match[str]) -> str:
        target = resolve_target(concept.path, match.group(2), lookup)
        if not target:
            return match.group(0)
        parsed = urlsplit(match.group(2))
        anchor = f"#{parsed.fragment}" if parsed.fragment else ""
        return f"[{match.group(1)}](/{target}.md{anchor})"

    def replace_wiki(match: re.Match[str]) -> str:
        target = resolve_target(concept.path, match.group(1), lookup) or lookup.get(
            match.group(1).strip().lower()
        )
        if not target:
            return match.group(0)
        return f"[{match.group(2) or match.group(1)}](/{target}.md)"

    return WIKI_LINK_RE.sub(replace_wiki, MARKDOWN_LINK_RE.sub(replace_markdown, concept.body))


def build_graph(concepts: list[Concept]) -> dict[str, Any]:
    concept_ids = {concept.concept_id for concept in concepts}
    edges: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for concept in concepts:
        for target in concept.outgoing:
            key = ("link", concept.concept_id, target)
            if target not in concept_ids or key in seen:
                continue
            seen.add(key)
            edges.append(
                {
                    "data": {
                        "id": f"{concept.concept_id}__{target}",
                        "source": concept.concept_id,
                        "target": target,
                        "kind": "link",
                    }
                }
            )

    agent_documents = {
        PurePosixPath(concept.path).parent: concept
        for concept in concepts
        if PurePosixPath(concept.path).name.lower() == "agents.md"
    }
    for child_directory, child in agent_documents.items():
        candidates = [
            (directory, concept)
            for directory, concept in agent_documents.items()
            if directory != child_directory and directory in child_directory.parents
        ]
        if not candidates:
            continue
        _, parent = max(candidates, key=lambda item: len(item[0].parts))
        key = ("routing", parent.concept_id, child.concept_id)
        if key in seen:
            continue
        seen.add(key)
        edges.append(
            {
                "data": {
                    "id": f"routing__{parent.concept_id}__{child.concept_id}",
                    "source": parent.concept_id,
                    "target": child.concept_id,
                    "kind": "routing",
                }
            }
        )
    return {
        "nodes": [concept.to_node() for concept in concepts],
        "edges": edges,
        "bodies": {concept.concept_id: concept.body for concept in concepts},
        "types": sorted({concept.concept_type for concept in concepts}),
    }


def load_template() -> str:
    plugin_root = Path(__file__).resolve().parents[1]
    return (plugin_root / "viewer/manager-viewer.html").read_text(encoding="utf-8")


def generate_html(manager_dir: Path, *, bundle_name: str | None = None) -> tuple[str, dict[str, int]]:
    manager_dir = manager_dir.expanduser().resolve()
    if not manager_dir.is_dir():
        raise FileNotFoundError(f"Manager directory not found: {manager_dir}")
    graph = build_graph(read_manager_documents(manager_dir))
    graph_json = json.dumps(graph, ensure_ascii=False).replace("</", "<\\/")
    name_json = json.dumps(bundle_name or manager_dir.name, ensure_ascii=False).replace("</", "<\\/")
    html = load_template().replace("__BUNDLE_NAME__", name_json).replace("__BUNDLE_DATA__", graph_json)
    return html, {
        "concepts": len(graph["nodes"]),
        "edges": len(graph["edges"]),
        "bytes": len(html.encode("utf-8")),
    }


def default_output_path() -> Path:
    output_dir = Path(tempfile.gettempdir()) / "wirenet-manager"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / "manager-viewer.html"


def serve_html(html: str, port: int) -> None:
    html_bytes = html.encode("utf-8")

    class ViewerHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            host = self.headers.get("Host", "").split(":", 1)[0].strip("[]")
            if host not in {"127.0.0.1", "localhost", "::1"}:
                self.send_error(403)
                return
            if self.path not in {"/", "/index.html"}:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html_bytes)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(html_bytes)

        def log_message(self, format_string: str, *args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", port), ViewerHandler)
    print("WireNet Manager Viewer", flush=True)
    print(f"URL: http://127.0.0.1:{server.server_port}", flush=True)
    print("Press Ctrl+C to stop.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render Manager Markdown as a read-only Google-derived OKF viewer."
    )
    parser.add_argument(
        "--manager-dir",
        type=Path,
        default=Path(os.environ.get("WIRENET_MANAGER_DIR", "~/Manager")),
        help="Manager content root (default: WIRENET_MANAGER_DIR or ~/Manager)",
    )
    parser.add_argument("--out", type=Path, help="Write the generated HTML to this path")
    parser.add_argument("--name", help="Viewer title (default: Manager directory name)")
    parser.add_argument("--serve", action="store_true", help="Serve the page on 127.0.0.1")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Local port (default: {DEFAULT_PORT})")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not 1 <= args.port <= 65535:
        raise SystemExit("--port must be between 1 and 65535")
    html, counts = generate_html(args.manager_dir, bundle_name=args.name)
    print(f"Viewer documents: {counts['concepts']}", flush=True)
    print(f"Graph edges: {counts['edges']}", flush=True)
    if args.serve:
        serve_html(html, args.port)
        return 0
    output_path = (args.out or default_output_path()).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"Viewer: {output_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
