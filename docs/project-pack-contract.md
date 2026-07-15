---
last_edited: 2026-07-15
---

# Project Pack Contract v0.1

## Open Core

Every Project Pack starts with two documents:

- `README.md`: the human and agent operational handoff;
- `AGENTS.md`: local read order, recurring sources, safety, and routing.

The packet is deliberately open. Agents may add purpose-driven concepts instead
of forcing every project into one fixed form.

## Optional Conventions

### `GOAL.md`

A stable outcome contract with baseline, completion criteria, constraints,
non-goals, and approval gates. Create it only when a separate durable goal
improves the handoff.

### `RESULT.md`

Completed outcomes and evidence. It does not duplicate active status or serve
as a running changelog.

### `WORKLOG.md`

Detailed attempts, evidence, active loop state, and the next experiment while
an UltraGoal is running. It is working state, not a portable summary.

### Other Concepts

Decisions, briefs, research, plans, or other documents are allowed when their
purpose is clearer than placing the information in a conventional filename.

## Optional Time Axis

### `log.md`

The reserved OKF history file may record meaningful project changes under
ISO-date headings, newest first. It contains concise state transitions and
handoffs, not commands, raw transcripts, or a second copy of current status.

`log.md` is scoped by its Project Pack path. It is not an OKF concept document,
so it has no Project Pack frontmatter and does not duplicate `project_id`. Do
not create it merely because a packet exists, and do not mirror UltraGoal's
more detailed `WORKLOG.md`.

## Frontmatter

Every non-reserved Project Pack concept shares:

```yaml
schema: "wirenet-project-pack/v0.1"
okf_profile: "wirenet-okf-project-pack/v0.1"
project_id: "prj_<uuid>"
scope: projects
context_scope: project
assembly_scope: project_context
```

Each concept adds its semantic `type`, title, status, visibility, timestamp,
and edited dates. Producer-defined fields are preserved. Reserved `index.md`
and `log.md` follow OKF's path-scoped formats and carry no concept metadata.

YAML frontmatter does not interfere with `AGENTS.md`. Codex reads the whole file
as Markdown instructions; the metadata is not Codex configuration.

## OKF Mapping

Jason Liu's conventional filenames remain convenient for people and agents.
WireNet maps them semantically without making the optional files mandatory:

| Local file | Profile type |
| --- | --- |
| `README.md` | `Project Status` |
| `AGENTS.md` | `Runtime Adapter` |
| optional `GOAL.md` | `Project Brief` |
| optional `RESULT.md` | `Project Result` |
| optional `WORKLOG.md` | producer-defined worklog concept |
| optional `log.md` | reserved OKF update history |
| another concept | descriptive producer-defined type |

This is an adapter profile. A future Knowledge Hub can transform or synchronize
the packet through stable types, links, and `project_id` without dictating its
complete file vocabulary.

## Additive Indexes

Manager `index.md` declares OKF 0.1 and catalogs the content shelves.
`projects/README.md` remains the human and Jason-compatible collection guide.
`projects/index.md` additively lists active Project Packs using normal relative
Markdown links and short descriptions.

Individual packets do not need another index while their structure is small;
an agent may add a packet-local index as the packet grows. The Google-derived
viewer deliberately omits reserved indexes and visualizes concept documents
instead. OKF indexes still route agents and future synchronization consumers;
they never replace README or AGENTS documents.

## Viewer Projection

The Project Pack remains inspectable when it contains only the minimum two
documents. Empty optional files are not created merely to make the structure
look complete.

The viewer shows complete human-facing documents by default and has one toggle
for complete `AGENTS.md` and explicit agent-facing runtime adapters. It filters
whole documents, never sections. Normal Markdown links become graph edges. The
nearest-parent relationship between `AGENTS.md` files becomes a derived dashed
routing edge only while agent instructions are enabled; no routing relationship
is persisted separately from the filesystem hierarchy.

Templates, ignored outputs, plugin implementation, and device-local bindings
remain outside the content projection. Reserved indexes remain navigation input
for agents and future OKF consumers rather than viewer nodes.

## UltraGoal Worklogs

An active UltraGoal may use `WORKLOG.md` for detailed attempts, evidence,
current loop state, and the next experiment. Meaningful conclusions are
distilled into `README.md`, optional `RESULT.md`, or another suitable concept.
Add a sparse `log.md` entry only when chronology is independently useful.

## Retrieval Boundary

QMD indexes these files as normal Markdown; reserved filenames do not receive
special ranking. Indexes improve orientation and search vocabulary. Logs help
chronological retrieval only while entries remain sparse and semantic.

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
Update the owning concept; add a `log.md` entry only when a durable sparse
chronology adds independent value.
