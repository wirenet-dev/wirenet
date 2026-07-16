---
schema: "wirenet-runtime/v0.1"
visibility: local
audience: agent
status: active
last_edited: 2026-07-16
---

# wirenet Manager Instructions

## Purpose

Use this repository as the user's local work-memory layer. Keep it concise,
reviewable, and useful to the next task.

## Language Contract

- Read `content_language` from the root `README.md` and use that language for
  conversation and new human-readable Manager prose.
- Keep file and folder names, frontmatter keys, schemas, IDs, enum values,
  plugin commands, and these runtime instructions in English.
- Preserve the language of established documents unless the user explicitly
  asks to translate them. Do not translate metadata keys or controlled values.

## Read Order

1. `README.md` and `index.md` for the human overview and knowledge catalog.
2. `TODO.md` for the immediate stack.
3. `projects/index.md` for project lifecycle and `experiments/index.md` when it
   exists and a bounded spike is relevant.
4. The relevant Project or Experiment Pack's `README.md` and `AGENTS.md`.
5. Optional `GOAL.md`, `RESULT.md`, `WORKLOG.md`, `log.md`, and additional
   concepts only when present and relevant.
6. People, notes, docs, sources, and external workspaces only when the task needs them.

## Durable State

- Current project state belongs in `projects/<slug>/README.md`.
- Stable outcomes and completion criteria may be separated into `GOAL.md` when
  a durable goal contract improves the handoff.
- Completed work and verification may be separated into `RESULT.md` when the
  evidence deserves a durable document.
- Recurring source routes and project-specific agent rules belong in `AGENTS.md`.
- Only an explicitly invoked UltraGoal may create or update `WORKLOG.md` for
  detailed attempts and recovery state.
- Meaningful dated state transitions may use optional `log.md` when a sparse
  chronology improves navigation; routine activity does not.
- Additional project concepts are allowed when they have a clear purpose, OKF
  `type`, and the packet's stable `project_id`.
- Cross-project priorities belong in `TODO.md`.
- Human collaboration notes belong in `people/`.
- Quick durable scratch knowledge belongs in `notes/`; structured standalone
  documents may use `docs/` when no more specific home is stronger.
- Curated retained evidence belongs in `sources/`; short-lived spikes belong in
  `experiments/`; each real experiment starts with `README.md` and `AGENTS.md`,
  remains bounded, and ends by conclusion, promotion, or archive. Inactive
  durable context belongs in `archive/`.
- A few transient review files may stay together under
  `outputs/<task-slug>/`. When files begin to need recurring editing, durable
  delivery, or their own toolchain, suggest an external workspace and Project
  Pack without interrupting useful work merely to reorganize it. Promote
  canonical meaning into a typed knowledge document.
- Do not write new working state into archived packets without explicit
  reactivation. Treat waiting and blocked as live states, and preserve promoted
  experiments as origin evidence.

## Workspace Contract

- `AGENTS.md` files are the runtime instruction hierarchy. They use
  `schema: "wirenet-runtime/v0.1"` and never declare an OKF `type`.
- `index.md` and `log.md` are reserved OKF support documents and never declare
  a concept `type`.
- Every other Markdown document in the Manager is a typed OKF concept.
- Keep reusable behavior, schemas, generation rules, and canonical templates in
  the installed wirenet Manager plugin rather than copying them into this
  workspace.
- Create a shelf-local `index.md` only when actual content benefits from a
  catalog. Do not create explanatory shelf README placeholders.

## Update Threshold

Update the Manager when future work would otherwise misunderstand status,
ownership, blockers, decisions, deadlines, canonical sources, or next steps.
Do not record every command, edit, test run, transient experiment, or generated
artifact. Prefer one compact handoff after a meaningful work phase.

## Safety

- Preserve external project locations and raw source material.
- Treat `sources/` as the curated Knowledge Shelf and `outputs/` as ignored,
  device-local working memory.
- Never write secrets, credentials, account numbers, or private keys.
- Preview inferred durable updates and ask before writing unless the user has
  already approved the exact change.
- Do not configure remotes, sync services, messages, meetings, or automations
  without explicit approval.
