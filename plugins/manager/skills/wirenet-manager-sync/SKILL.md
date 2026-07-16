---
name: wirenet-manager-sync
description: Reconcile meaningful durable progress from the current external workspace into an existing WireNet Manager Project or Experiment Pack. Use after a substantial work phase or durable status, source, deadline, result, decision, blocker, or next-step change; when asked to update Manager with the current workspace; or when the global managed block requests a handoff. Use wirenet-manager-project for new workspace classification and lifecycle changes, and wirenet-manager-person for canonical person context.
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
   - `experiment`: read its lightweight `README.md` and `AGENTS.md`; preserve the
     bound and decision criterion, then record only meaningful observations or
     results.
   - `ignored`: stay quiet.
   - `untracked`: use `$wirenet-manager-project` to classify it once as a
     project, experiment, or ignored folder.
3. For a tracked project, propose only the smallest durable diff:
   - `README.md` for the current handoff, owner, decision, blocker, deadline,
     source, or next move;
   - `AGENTS.md` for read order, recurring sources, safety, or routing changes.
   - create or update `GOAL.md` only for a useful separate outcome contract;
   - create or update `RESULT.md` only for durable completed evidence;
   - only an explicitly invoked `$ultragoal` may create or update `WORKLOG.md`;
   - use another typed concept when its purpose is clearer than a standard file.
4. Use or create `log.md` only when sparse chronology materially improves
   navigation or synchronization. Never mirror a WORKLOG or routine activity.
5. Show the intended diff and ask before writing unless the user already
   approved that exact update.
6. Preserve `project_id`, unknown frontmatter fields, and the local/portable
   boundary.
7. For a tracked experiment, record only meaningful observations or results.
   Use `$wirenet-manager-project` for conclusion, promotion, archival, or
   reactivation.
8. Use `$wirenet-manager-person` for canonical person context. For other
   durable context not owned by a packet, follow
   `../wirenet-manager/references/content-routing.md`.

## Update Threshold

Update when a future task would otherwise misunderstand the project. Do not
write routine command output, raw transcripts, generated files, temporary
implementation detail, secrets, or unconfirmed inference.

Do not archive, reactivate, promote, conclude, or change lifecycle status here.
Route those transitions through `$wirenet-manager-project` after the durable
handoff has been reconciled.

## Resources

- `scripts/inspect_workspace.py`: read-only lookup through local bindings.
- `references/update-contract.md`: durable update and routing rules.
- `../wirenet-manager/references/content-routing.md`: shared Manager shelf and
  open Project Pack rules.
