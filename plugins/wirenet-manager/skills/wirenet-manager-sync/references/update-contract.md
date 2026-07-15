---
last_edited: 2026-07-15
---

# Project Pack Update Contract

## Write When

- the desired outcome or completion criteria changed;
- durable status or a milestone changed;
- an owner, decision maker, or responsibility changed;
- a blocker, deadline, canonical source, or next step changed;
- a completed result gained meaningful verification;
- a future task would otherwise resume from the wrong state.

## Do Not Write

- command-by-command logs or every passing test;
- raw media, transcripts, email bodies, or private source dumps;
- speculative conclusions presented as fact;
- secrets, credentials, build output, generated files, or caches;
- implementation detail that will not matter in the next work session.

## Project Pack Routing

- `README.md`: current operational handoff.
- `AGENTS.md`: recurring routing and local rules.
- optional `GOAL.md`: stable intent and completion contract when a separate
  document improves the handoff.
- optional `RESULT.md`: completed evidence when it deserves a durable document.
- optional `WORKLOG.md`: detailed active UltraGoal attempts and next action.
- optional `log.md`: sparse dated transitions useful for navigation or sync;
  never a command-by-command worklog or duplicate status page.
- other optional concepts: allowed when they use a clear OKF type and stable
  packet `project_id`.

Do not force information into a conventional filename merely to fill a template.
Do not create empty optional documents.

## Workspace Classification

- `project`: create a packet after approval and bind its `project_id` to the
  local path.
- `experiment`: store the local route without creating a full packet.
- `ignored`: store the local route and do not ask again.

Bindings and routes are device-local. They belong in
`.wirenet/project-bindings.json`, not portable Project Pack frontmatter.

For non-project durable context, follow the shared content-routing contract in
`../wirenet-manager/references/content-routing.md`.
