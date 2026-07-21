---
schema: "wirenet-runtime/v0.1"
visibility: local
audience: agent
status: active
last_edited: 2026-07-16
---

# Project Pack Instructions

## Minimum Contract

Every active Project Pack starts with:

1. `README.md` — current project state; OKF `Project Status`.
2. `AGENTS.md` — local read order and routing; runtime sidecar outside OKF.

## Optional Conventions

- `GOAL.md` — stable outcome and completion contract; OKF `Project Brief`.
- `RESULT.md` — completed outcomes and verification; wirenet `Project Result`.
- `WORKLOG.md` — detailed active UltraGoal attempts, evidence, and next action;
  only an explicitly invoked UltraGoal may create or update it.
- `log.md` — sparse meaningful changes under ISO-date headings; reserved OKF history.
- Other Markdown concepts — allowed when their purpose is clearer than forcing
  the information into a standard filename.

## Rules

- Use one stable `project_id` across every Project Pack concept document.
  Reserved `index.md` and `log.md` are path-scoped and carry no concept
  frontmatter.
- Keep local filesystem paths out of portable Project Pack files.
- Update `projects/index.md` after every packet creation or lifecycle transition.
- Create `GOAL.md`, `RESULT.md`, `WORKLOG.md`, `log.md`, or another concept only
  when it earns a separate durable role.
- Never mirror UltraGoal `WORKLOG.md` detail into `log.md`; the latter is only a
  sparse portable chronology when useful.
- Keep packets useful as handoffs without restricting agents to a fixed file set.
- Every non-reserved Markdown document other than `AGENTS.md` must be a typed
  OKF concept. Do not add untyped explanatory README files.
- Preserve unknown frontmatter keys when editing.
