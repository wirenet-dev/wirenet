---
type: "Runtime Adapter"
schema: "wirenet-manager/v0.1"
visibility: local
status: active
last_edited: 2026-07-15
---

# WireNet Manager Instructions

## Purpose

Use this repository as the user's local work-memory layer. Keep it concise,
reviewable, and useful to the next task.

## Read Order

1. `TODO.md` for the immediate stack.
2. `projects/index.md` for active workstreams.
3. The relevant Project Pack's `GOAL.md`, `README.md`, `RESULT.md`, and
   `AGENTS.md`; read `log.md` only when chronology matters.
4. People, notes, sources, and external workspaces only when the task needs them.

## Durable State

- Current project state belongs in `projects/<slug>/README.md`.
- Stable outcomes and completion criteria belong in `GOAL.md`.
- Completed work and verification belong in `RESULT.md`.
- Recurring source routes and project-specific agent rules belong in `AGENTS.md`.
- Meaningful dated state transitions belong in `log.md`; routine activity does not.
- Cross-project priorities belong in `TODO.md`.
- Human collaboration notes belong in `people/`.

## Update Threshold

Update the Manager when future work would otherwise misunderstand status,
ownership, blockers, decisions, deadlines, canonical sources, or next steps.
Do not record every command, edit, test run, transient experiment, or generated
artifact. Prefer one compact handoff after a meaningful work phase.

## Safety

- Preserve external project locations and raw source material.
- Never write secrets, credentials, account numbers, or private keys.
- Preview inferred durable updates and ask before writing unless the user has
  already approved the exact change.
- Do not configure remotes, sync services, messages, meetings, or automations
  without explicit approval.
