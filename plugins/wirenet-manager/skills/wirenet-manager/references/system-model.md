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
| `README.md` | Status, next move, owners, decisions, blockers | `Project Status` |
| `AGENTS.md` | Read order, sources, rules, safety | `Runtime Adapter` |
| optional `GOAL.md` | Outcome, constraints, completion criteria | `Project Brief` |
| optional `RESULT.md` | Completed outcomes and verification | `Project Result` |
| optional `WORKLOG.md` | Detailed active UltraGoal state | producer-defined concept |
| optional `log.md` | Sparse dated state transitions | reserved OKF history |
| other optional concepts | Purpose-driven project knowledge | producer-defined OKF type |

`README.md` and `AGENTS.md` are the minimum packet. Every non-reserved concept
shares one stable `project_id`; reserved `index.md` and `log.md` are scoped by
the packet path and carry no concept frontmatter. Local filesystem paths stay in
`.wirenet/project-bindings.json` so portable Project Packs can later move
between devices.

## Update Boundary

Update a Project Pack after a meaningful handoff or state transition. Do not
mirror every edit, command, test, or temporary experiment. A recurring Manager
task reconciles missed updates; it is not a filesystem watcher. Use an optional
compact `log.md` only when sparse chronology improves navigation or future sync.

README files retain Jason Liu's human and agent routing roles. OKF indexes are
additive: Manager `index.md` catalogs the bundle, `projects/README.md` retains
the collection guide, and `projects/index.md` provides progressive disclosure.
Neither OKF metadata nor indexes replace AGENTS instructions.
