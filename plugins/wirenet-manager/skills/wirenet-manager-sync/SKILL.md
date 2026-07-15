---
name: wirenet-manager-sync
description: Reconcile meaningful durable context from the current workspace into WireNet Manager. Use after durable project, person, source, deadline, result, decision, blocker, or next-step changes; when finishing a substantial work phase; when asked to update the Manager; or when an untracked workspace needs classification.
---

# WireNet Manager Sync

Keep Project Packs useful without turning them into activity logs. Skill
description matching is convenient; the managed global `AGENTS.md` block is the
reliable cross-project trigger.

## Workflow

1. Run `scripts/inspect_workspace.py` for the current workspace and Manager.
2. Follow its classification:
   - `manager`: use the shared shelf contract and update only the canonical file
     relevant to the task.
   - `tracked`: read `README.md` and `AGENTS.md` first; read optional concepts
     only when present and relevant, then inspect the smallest useful external evidence.
   - `experiment` or `ignored`: stay quiet and do not create a packet.
   - `untracked`: ask once whether the folder is a project, experiment, or
     ignored.
3. For a new project, preview the plugin-root `scripts/create_project_pack.py`.
   Apply it only after approval. It writes `README.md`, `AGENTS.md`, the
   `projects/index.md` entry, and a local binding. Add optional concepts only
   when useful.
4. For a tracked project, propose only the smallest durable diff:
   - `README.md` for status, owner, decision, blocker, deadline, source, or next move;
   - `AGENTS.md` for read order, recurring sources, safety, or routing changes.
   - create or update `GOAL.md` only for a useful separate outcome contract;
   - create or update `RESULT.md` only for durable completed evidence;
   - let UltraGoal use `WORKLOG.md` for detailed iteration;
   - use another typed concept when its purpose is clearer than a standard file.
5. Use or create `log.md` only when sparse chronology materially improves
   navigation or synchronization. Never mirror a WORKLOG or routine activity.
6. Show the intended diff and ask before writing unless the user already
   approved that exact update.
7. Preserve `project_id`, unknown frontmatter fields, and the local/portable
   boundary.
8. Record experiment or ignored routes with `scripts/record_routing.py` after
   approval so future tasks stay quiet.
9. For durable context not owned by a Project Pack, follow
   `../wirenet-manager/references/content-routing.md` and route it to the
   appropriate Manager shelf as a typed concept. Create a shelf `index.md` only
   when real content benefits from progressive disclosure.

## Update Threshold

Update when a future task would otherwise misunderstand the project. Do not
write routine command output, raw transcripts, generated files, temporary
implementation detail, secrets, or unconfirmed inference.

## Resources

- `scripts/inspect_workspace.py`: read-only lookup through local bindings.
- `scripts/record_routing.py`: dry-run-first experiment/ignore recorder.
- `references/update-contract.md`: durable update and routing rules.
- `../wirenet-manager/references/content-routing.md`: shared Manager shelf and
  open Project Pack rules.
