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
| `AGENTS.md` | Read order, sources, rules, safety | runtime sidecar outside OKF |
| optional `GOAL.md` | Outcome, constraints, completion criteria | `Project Brief` |
| optional `RESULT.md` | Completed outcomes and verification | `Project Result` |
| optional `WORKLOG.md` | Detailed active UltraGoal state | producer-defined concept |
| optional `log.md` | Sparse dated state transitions | reserved OKF history |
| other optional concepts | Purpose-driven project knowledge | producer-defined OKF type |

`README.md` and `AGENTS.md` are the minimum packet. Every concept and the runtime
sidecar share one stable `project_id`; reserved `index.md` and `log.md` are
scoped by the packet path and carry no concept frontmatter. Local filesystem paths stay in
`.wirenet/project-bindings.json` so portable Project Packs can later move
between devices.

## Update Boundary

Update a Project Pack after a meaningful handoff or state transition. Do not
mirror every edit, command, test, or temporary experiment. A recurring Manager
task reconciles missed updates; it is not a filesystem watcher. Use an optional
compact `log.md` only when sparse chronology improves navigation or future sync.

README files are preserved only where they carry instance knowledge: the typed
root `README.md` is the Manager Overview and each typed project `README.md` is
Project Status. Manager `index.md` catalogs the bundle and
`projects/index.md` provides progressive disclosure. Neither OKF metadata nor
indexes replace AGENTS instructions.

The Manager is one canonical OKF bundle with a transparent runtime overlay.
Future sync consumers use typed Markdown concepts plus reserved indexes and
logs. The WireNet Inspector emits only typed concepts; reserved indexes, logs,
runtime `AGENTS.md`, hidden local state, ignored outputs, and plugin
implementation do not enter its generated payload. No untyped guide exception
exists in v0.1.
