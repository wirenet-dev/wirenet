---
name: wirenet-manager-sync
description: Reconcile the current external workspace with its WireNet Manager Project Pack. Use after meaningful durable status, ownership, blocker, decision, source, deadline, result, or next-step changes; when finishing a substantial project work phase; when asked to update or check the Manager; or when an untracked workspace needs classification.
---

# WireNet Manager Sync

Keep Project Packs useful without turning them into activity logs. Skill
description matching is convenient; the managed global `AGENTS.md` block is the
reliable cross-project trigger.

## Workflow

1. Run `scripts/inspect_workspace.py` for the current workspace and Manager.
2. Follow its classification:
   - `manager`: update only the canonical Manager file relevant to the task.
   - `tracked`: read `GOAL.md`, `README.md`, `RESULT.md`, and `AGENTS.md`, then
     inspect the smallest useful external evidence.
   - `experiment` or `ignored`: stay quiet and do not create a packet.
   - `untracked`: ask once whether the folder is a project, experiment, or
     ignored.
3. For a new project, preview the plugin-root `scripts/create_project_pack.py`.
   Apply it only after approval. It writes the four-file packet and a local
   binding in `.wirenet/project-bindings.json`.
4. For a tracked project, propose only the smallest durable diff:
   - `GOAL.md` for outcome or completion-contract changes;
   - `README.md` for status, owner, decision, blocker, deadline, source, or next move;
   - `RESULT.md` for completed outcomes with verification;
   - `AGENTS.md` for read order, recurring sources, safety, or routing changes.
5. Show the intended diff and ask before writing unless the user already
   approved that exact update.
6. Preserve `project_id`, unknown frontmatter fields, and the local/portable
   boundary.
7. Record experiment or ignored routes with `scripts/record_routing.py` after
   approval so future tasks stay quiet.

## Update Threshold

Update when a future task would otherwise misunderstand the project. Do not
write routine command output, raw transcripts, generated files, temporary
implementation detail, secrets, or unconfirmed inference.

## Resources

- `scripts/inspect_workspace.py`: read-only lookup through local bindings.
- `scripts/record_routing.py`: dry-run-first experiment/ignore recorder.
- `references/update-contract.md`: durable update and routing rules.
