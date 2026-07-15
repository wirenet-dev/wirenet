---
type: "Manager Overview"
schema: "wirenet-manager/v0.1"
visibility: private
status: active
last_edited: 2026-07-15
---

# WireNet Manager

This folder is the user's local, durable work memory. It stores reviewable
Project Packs and personal operating context. Implementation code, media, and
large data stay in their existing external workspaces.

## Start Here

1. Read `TODO.md` for the current stack.
2. Read `projects/README.md` for the collection rules and `projects/index.md`
   for active Project Packs.
3. Open the relevant `projects/<slug>/` packet only when needed.
4. Use recurring sources listed in the packet's `AGENTS.md` selectively.

## Main Areas

- `agent/`: durable user and working-context notes.
- `people/`: evidence-backed collaborator notes.
- `projects/`: open Project Packs with a stable README and agent routing.
- `notes/`: durable scratch notes without a better canonical home.
- `docs/`: optional structured documents without a stronger project, person,
  or source home; agents may organize it as useful.
- `sources/`: the Knowledge Shelf for curated evidence and source context;
  read-only by default and link-first.
- `experiments/`: short-lived spikes that may later become projects.
- `outputs/`: ignored, device-local working memory for generated intermediates;
  not canonical knowledge and not part of future sync by default.
- `archive/`: inactive material preserved for history.
- `.wirenet/`: local machine bindings and Manager metadata.

The shelves are routing defaults, not a fixed taxonomy. Agents may add useful
subfolders and typed concepts while preferring the clearest existing canonical
home over duplication.

## Project Pack Contract

Each Project Pack starts with only two stable documents:

- `README.md`: current status, next move, owners, decisions, and blockers.
- `AGENTS.md`: read order, recurring sources, safety gates, and update rules.

The agent may add `GOAL.md`, `RESULT.md`, `WORKLOG.md`, `log.md`, or other useful
concepts when the project needs them. Additional concept documents use OKF
frontmatter and share the packet's stable `project_id`. This preserves Jason
Liu's open project model while making the packet portable.

`WORKLOG.md` is detailed UltraGoal working state. Reserved `log.md` is a sparse
OKF chronology and should exist only when that time axis materially helps. They
must not duplicate one another.

## Boundaries

- Absolute external project paths live only in `.wirenet/project-bindings.json`.
- Portable Project Packs use stable `project_id` values.
- Do not copy credentials, private source dumps, raw media, build output, or
  generated caches into the Manager.
- Keep actual `outputs/` content local and ignored. Link or distill anything
  durable into a Project Pack, `sources/`, or `notes/`.
- Git is local history by default. No remote or cloud sync is configured by v0.1.
