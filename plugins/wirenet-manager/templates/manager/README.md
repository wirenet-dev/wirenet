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
2. Read `projects/index.md` for active Project Packs.
3. Open the relevant `projects/<slug>/` packet only when needed.
4. Use recurring sources listed in the packet's `AGENTS.md` selectively.

## Main Areas

- `agent/`: durable user and working-context notes.
- `people/`: evidence-backed collaborator notes.
- `projects/`: Project Packs with four state documents and an OKF log.
- `notes/`: durable scratch notes without a better canonical home.
- `sources/`: retained evidence; read-only by default.
- `experiments/`: short-lived spikes that may later become projects.
- `outputs/`: reviewable generated artifacts worth retaining.
- `archive/`: inactive material preserved for history.
- `.wirenet/`: local machine bindings and Manager metadata.

## Project Pack Contract

Each Project Pack uses four stable state documents and one time axis:

- `GOAL.md`: stable outcome, constraints, and completion criteria.
- `README.md`: current status, next move, owners, decisions, and blockers.
- `RESULT.md`: completed outcomes and verification evidence.
- `AGENTS.md`: read order, recurring sources, safety gates, and update rules.
- `log.md`: concise meaningful changes under ISO-date headings, newest first.

The four state filenames preserve Jason Liu's practical monorepo model. Their
frontmatter maps them to a small WireNet OKF profile; the additional `log.md`
provides portable chronology without changing the local reading experience.

## Boundaries

- Absolute external project paths live only in `.wirenet/project-bindings.json`.
- Portable Project Packs use stable `project_id` values.
- Do not copy credentials, private source dumps, raw media, build output, or
  generated caches into the Manager.
- Git is local history by default. No remote or cloud sync is configured by v0.1.
