---
last_edited: 2026-07-15
---

# Project Pack Contract v0.1

## Four State Documents

### `GOAL.md`

The stable outcome contract: baseline, completion criteria, constraints,
non-goals, and approval gates. Change it rarely.

### `README.md`

The operational handoff: purpose, current status, next move, owners, decisions,
blockers, and canonical sources.

### `RESULT.md`

Completed outcomes and evidence. It does not duplicate the active status or
serve as a running changelog.

### `AGENTS.md`

Read order, recurring source routes, safety gates, and rules for updating the
other three files.

These four concept documents are the stable dimensions of a project: intent,
current state, completed evidence, and agent behavior.

## One Time Axis

### `log.md`

The reserved OKF history file records meaningful project changes under ISO-date
headings, newest first. It contains concise state transitions and handoffs, not
commands, raw transcripts, or a second copy of current status.

`log.md` is scoped by its Project Pack path. It is not an OKF concept document,
so it has no Project Pack frontmatter and does not duplicate `project_id`.

## Frontmatter

All four state documents share:

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

Jason Liu's four concept filenames remain convenient for people and agents.
WireNet maps them semantically and adds the reserved OKF log:

| Local file | Profile type |
| --- | --- |
| `GOAL.md` | `Project Brief` |
| `README.md` | `Project Status` |
| `RESULT.md` | `Project Result` |
| `AGENTS.md` | `Runtime Adapter` |
| `log.md` | reserved OKF update history |

This is an adapter profile. A full WireNet OKF mirror uses `brief.md`,
`status.md`, events, decisions, outputs, context packs, and run receipts. The
Manager does not need that full structure in v0.1. A future Knowledge Hub can
transform the packet through the shared types and stable `project_id`.

## Collection Index

`projects/index.md` lists active Project Packs using normal relative Markdown
links and short descriptions. Individual packets do not need another index:
their fixed small structure and `AGENTS.md` already provide local routing.

The index contains no Project Pack frontmatter. It is an OKF navigation file,
not a project concept.

## UltraGoal Worklogs

An active UltraGoal may optionally use `WORKLOG.md` for detailed attempts,
evidence, current loop state, and the next experiment. It is not part of every
Project Pack. Meaningful conclusions are distilled into `README.md`,
`RESULT.md`, and `log.md`; routine iteration stays out of durable retrieval.

## Retrieval Boundary

QMD indexes these files as normal Markdown; reserved filenames do not receive
special ranking. The concise collection index improves orientation and search
vocabulary. The update log helps chronological retrieval only while entries
remain sparse and semantic. Verbose activity logging would create redundant
chunks and reduce result precision.

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
When canonical state changes, add one linked `log.md` entry describing that
transition without repeating the full state.
