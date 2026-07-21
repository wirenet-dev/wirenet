#!/usr/bin/env python3
"""Build the portable OKF knowledge projection of a Manager workspace."""

from __future__ import annotations

import json
import os
import posixpath
import re
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote, urlsplit


MAX_MARKDOWN_BYTES = 2_000_000
RESERVED_DOCUMENTS = {"index.md": "index", "log.md": "log"}
RUNTIME_DOCUMENTS = {"agents.md"}
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

TYPE_PALETTE = {
    "Manager Overview": "#262626",
    "Task Stack": "#ff5c1a",
    "Project Brief": "#ff5c1a",
    "Project Status": "#2f8fce",
    "Project Result": "#23855c",
    "Person": "#7c5cc4",
    "Decision": "#b1507c",
    "Document": "#8a8a8a",
}
DEFAULT_NODE_COLOR = "#8a8a8a"


@dataclass
class KnowledgeDocument:
    path: str
    document_id: str
    kind: str
    concept_type: str
    title: str
    description: str
    resource: str
    tags: list[str]
    metadata: dict[str, Any]
    body: str
    outgoing: list[str] = field(default_factory=list)

    @property
    def is_concept(self) -> bool:
        return self.kind == "concept"

    def to_node(self) -> dict[str, Any]:
        return {
            "data": {
                "id": self.document_id,
                "label": self.title or self.document_id,
                "type": self.concept_type,
                "description": self.description,
                "resource": self.resource,
                "tags": self.tags,
                "color": TYPE_PALETTE.get(self.concept_type, DEFAULT_NODE_COLOR),
                "size": 30 + min(60, len(self.body) // 200),
            }
        }


@dataclass
class OKFProjection:
    documents: list[KnowledgeDocument]

    @property
    def concepts(self) -> list[KnowledgeDocument]:
        return [document for document in self.documents if document.is_concept]

    @property
    def indexes(self) -> list[KnowledgeDocument]:
        return [document for document in self.documents if document.kind == "index"]

    @property
    def logs(self) -> list[KnowledgeDocument]:
        return [document for document in self.documents if document.kind == "log"]


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
            if path.suffix.lower() not in MARKDOWN_EXTENSIONS:
                continue
            try:
                if path.stat().st_size <= MAX_MARKDOWN_BYTES:
                    paths.append(path)
            except OSError:
                continue
    return paths


def collect_okf_projection(manager_dir: Path) -> OKFProjection:
    """Select the canonical Manager OKF bundle without its runtime overlay."""
    documents: list[KnowledgeDocument] = []
    for path in iter_markdown(manager_dir):
        try:
            raw = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        metadata, body = parse_frontmatter(raw)
        relative_path = path.relative_to(manager_dir).as_posix()
        relative = PurePosixPath(relative_path)
        name = relative.name.lower()
        if name in RUNTIME_DOCUMENTS:
            continue
        if name in RESERVED_DOCUMENTS:
            kind = RESERVED_DOCUMENTS[name]
            concept_type = "Catalog" if kind == "index" else "History"
        else:
            concept_type = str(metadata.get("type") or "").strip()
            if not concept_type:
                continue
            kind = "concept"
        documents.append(
            KnowledgeDocument(
                path=relative_path,
                document_id=str(relative.with_suffix("")),
                kind=kind,
                concept_type=concept_type,
                title=title_from(relative_path, body, metadata),
                description=description_from(body, metadata),
                resource=str(metadata.get("resource") or ""),
                tags=tags_from(metadata),
                metadata=metadata,
                body=body,
            )
        )
    resolve_links(documents)
    return OKFProjection(documents=documents)


def build_path_lookup(documents: list[KnowledgeDocument]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    aliases: dict[str, set[str]] = {}
    for document in documents:
        path = PurePosixPath(document.path)
        without_suffix = str(path.with_suffix(""))
        lookup[document.path.lower()] = document.document_id
        lookup[without_suffix.lower()] = document.document_id
        aliases.setdefault(path.name.lower(), set()).add(document.document_id)
        aliases.setdefault(path.stem.lower(), set()).add(document.document_id)
    for alias, document_ids in aliases.items():
        if len(document_ids) == 1:
            lookup[alias] = next(iter(document_ids))
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
        variants.extend(
            [
                f"{normalized}.md",
                posixpath.join(normalized, "index.md"),
                posixpath.join(normalized, "index"),
            ]
        )
    for variant in variants:
        match = lookup.get(variant.lower())
        if match:
            return match
    return None


def resolve_links(documents: list[KnowledgeDocument]) -> None:
    lookup = build_path_lookup(documents)
    for document in documents:
        outgoing: list[str] = []
        for match in MARKDOWN_LINK_RE.finditer(document.body):
            target = resolve_target(document.path, match.group(2), lookup)
            if target and target != document.document_id and target not in outgoing:
                outgoing.append(target)
        document.outgoing = outgoing
        document.body = normalize_internal_links(document, lookup)


def normalize_internal_links(document: KnowledgeDocument, lookup: dict[str, str]) -> str:
    def replace_markdown(match: re.Match[str]) -> str:
        target = resolve_target(document.path, match.group(2), lookup)
        if not target:
            return match.group(0)
        parsed = urlsplit(match.group(2))
        anchor = f"#{parsed.fragment}" if parsed.fragment else ""
        return f"[{match.group(1)}](/{target}.md{anchor})"

    return MARKDOWN_LINK_RE.sub(replace_markdown, document.body)


def build_graph(projection: OKFProjection) -> dict[str, Any]:
    concepts = projection.concepts
    concept_ids = {concept.document_id for concept in concepts}
    edges: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for concept in concepts:
        for target in concept.outgoing:
            key = (concept.document_id, target)
            if target not in concept_ids or key in seen:
                continue
            seen.add(key)
            edges.append(
                {
                    "data": {
                        "id": f"{concept.document_id}__{target}",
                        "source": concept.document_id,
                        "target": target,
                    }
                }
            )
    return {
        "nodes": [concept.to_node() for concept in concepts],
        "edges": edges,
        "bodies": {concept.document_id: concept.body for concept in concepts},
        "types": sorted({concept.concept_type for concept in concepts}),
        "palette": TYPE_PALETTE,
    }
