---
last_edited: 2026-07-15
---

# Project Pack Contract v0.1

## Four Files

### `GOAL.md`

The stable outcome contract: baseline, completion criteria, constraints,
non-goals, and approval gates. Change it rarely.

### `README.md`

The operational handoff: purpose, current status, next move, owners, decisions,
blockers, sources, and compact update history.

### `RESULT.md`

Completed outcomes and evidence. It does not duplicate the active status or
serve as a running changelog.

### `AGENTS.md`

Read order, recurring source routes, safety gates, and rules for updating the
other three files.

## Frontmatter

All four files share:

```yaml
schema: "wirenet-project-pack/v0.1"
okf_profile: "wirenet-okf-project-pack/v0.1"
project_id: "prj_<uuid>"
scope: projects
context_scope: project
assembly_scope: project_context
```

Each file adds its semantic `type`, title, status, visibility, timestamp, and
edited dates. Producer-defined fields are preserved.

YAML frontmatter does not interfere with `AGENTS.md`. Codex reads the whole file
as Markdown instructions; it does not currently define the Project Pack
metadata as Codex configuration. The metadata remains deliberately small so it
cannot be confused with behavioral instructions.

## OKF Mapping

Jason Liu's filenames remain convenient for people and agents. WireNet maps
them semantically:

| Local file | Profile type |
| --- | --- |
| `GOAL.md` | `Project Brief` |
| `README.md` | `Project Status` |
| `RESULT.md` | `Project Result` |
| `AGENTS.md` | `Runtime Adapter` |

This is an adapter profile. A full WireNet OKF mirror uses `brief.md`,
`status.md`, events, decisions, outputs, context packs, and run receipts. The
Manager does not need that full structure in v0.1. A future Knowledge Hub can
transform the four-file packet through the shared types and stable `project_id`.

## Local Binding

Absolute paths are not portable knowledge. The local registry keeps them
separate:

```json
{
  "project_id": "prj_<uuid>",
  "path": "/local/path/to/project"
}
```

Another device can bind the same `project_id` to a different path without
editing or conflicting with the Project Pack itself.

## Update Threshold

Write only when future work would otherwise resume incorrectly. Prefer one
compact handoff after a meaningful phase over incremental activity logging.
