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

- `GOAL.md`: stable intent and completion contract.
- `README.md`: current operational handoff.
- `RESULT.md`: completed evidence.
- `AGENTS.md`: recurring routing and local rules.
- `log.md`: one concise dated entry for a meaningful state transition; never a
  command-by-command worklog or duplicate status page.

## Workspace Classification

- `project`: create a packet after approval and bind its `project_id` to the
  local path.
- `experiment`: store the local route without creating a full packet.
- `ignored`: store the local route and do not ask again.

Bindings and routes are device-local. They belong in
`.wirenet/project-bindings.json`, not portable Project Pack frontmatter.
