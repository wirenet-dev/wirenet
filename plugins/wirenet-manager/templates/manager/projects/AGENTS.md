---
type: "Runtime Adapter"
schema: "wirenet-manager/v0.1"
visibility: local
status: active
last_edited: 2026-07-15
---

# Project Pack Instructions

## Required Files

Every active Project Pack contains:

1. `GOAL.md` — stable outcome and completion contract; OKF `Project Brief`.
2. `README.md` — current project state; OKF `Project Status`.
3. `RESULT.md` — completed outcomes and verification; WireNet `Project Result`.
4. `AGENTS.md` — local read order and routing; OKF `Runtime Adapter`.
5. `log.md` — meaningful changes under ISO-date headings; reserved OKF history.

## Rules

- Use one stable `project_id` across the four concept documents. `log.md` is
  scoped by its packet path and carries no concept frontmatter.
- Keep local filesystem paths out of portable Project Pack files.
- Update the project index when creating or archiving a packet.
- Add one compact `log.md` entry when canonical project state meaningfully changes.
- Keep packets useful as handoffs; never turn `log.md` into a raw worklog.
- Preserve unknown frontmatter keys when editing.
