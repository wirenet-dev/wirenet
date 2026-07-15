---
last_edited: 2026-07-15
---

# WireNet Manager v0.1 System Model

## Boundaries

- The installed plugin owns reusable behavior, schemas, deterministic scripts,
  and the seed template.
- `~/Manager` owns personal durable content and local Git history.
- External project workspaces keep code, media, data, and operational files.
- Client and domain capabilities belong in separately versioned plugins.
- The future Knowledge Hub will synchronize portable Project Pack concepts, not
  machine-local paths.

## Project Pack

| File | Responsibility | WireNet OKF mapping |
| --- | --- | --- |
| `GOAL.md` | Outcome, constraints, completion criteria | `Project Brief` |
| `README.md` | Status, next move, owners, decisions, blockers | `Project Status` |
| `RESULT.md` | Completed outcomes and verification | `Project Result` |
| `AGENTS.md` | Read order, sources, rules, safety | `Runtime Adapter` |

All four files share one stable `project_id`. Local filesystem paths stay in
`.wirenet/project-bindings.json` so portable Project Packs can later move
between devices.

## Update Boundary

Update a Project Pack after a meaningful handoff or state transition. Do not
mirror every edit, command, test, or temporary experiment. A recurring Manager
task reconciles missed updates; it is not a filesystem watcher.
