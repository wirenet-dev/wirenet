---
type: "Manager Overview"
schema: "wirenet-manager/v0.1"
title: "WireNet Manager"
visibility: private
status: active
last_edited: 2026-07-15
---

# WireNet Manager

This is the human landing page for the user's local, durable work memory.
Implementation code, media, and large data stay in their existing external
workspaces; this Manager keeps the portable meaning needed to resume work.

## Start Here

1. Open the [current stack](TODO.md).
2. Browse the [Project Pack catalog](projects/index.md).
3. Open only the relevant packet and follow its links selectively.
4. Read [user context](agent/USER_CONTEXT.md) only when the task needs it.

## Main Areas

- `agent/`: durable user and working-context notes.
- `people/`: evidence-backed collaborator notes.
- `projects/`: portable Project Packs with typed status and local agent routing.
- `notes/`: durable scratch notes without a better canonical home.
- `docs/`: optional structured documents without a stronger project, person,
  or source home; agents may organize it as useful.
- `sources/`: the Knowledge Shelf for curated evidence and source context.
- `experiments/`: short-lived spikes that may later become projects.
- `outputs/`: ignored, device-local working memory for generated intermediates;
  not canonical knowledge and not part of future sync by default.
- `archive/`: inactive material preserved for history.
- `.wirenet/`: device-local bindings and Manager metadata; never portable
  knowledge.

The shelves are routing defaults, not a fixed taxonomy. An index is created for
a shelf only once its real content benefits from a catalog.

## Project Pack Contract

Each Project Pack starts with two stable documents:

- `README.md`: current status, next move, owners, decisions, and blockers.
- `AGENTS.md`: read order, recurring sources, safety gates, and update rules.

The agent may add `GOAL.md`, `RESULT.md`, `WORKLOG.md`, `log.md`, `index.md`, or
other useful concepts when the project needs them. Every non-reserved Markdown
document other than `AGENTS.md` is typed OKF knowledge. Project concepts share
the packet's stable `project_id`.

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
- Product instructions, generation rules, and canonical templates live in the
  installed WireNet Manager plugin rather than being copied into this folder.
- Git is local history by default. No remote or cloud sync is configured by v0.1.
