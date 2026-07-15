---
name: wirenet-manager-sync
description: Reconcile meaningful durable context from the current workspace into WireNet Manager. Use when the user asks to create, start, or track a new project or experiment; after durable project, person, source, deadline, result, decision, blocker, or next-step changes; when finishing a substantial work phase; when asked to update the Manager; or when an untracked workspace needs classification.
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
     lifecycle transitions.
   - `ignored`: stay quiet.
   - `untracked`: ask once whether the folder is a project, experiment, or
     ignored.
3. For a new project, preview the plugin-root `scripts/create_project_pack.py`.
   Apply it only after approval. It writes `README.md`, `AGENTS.md`, the
   `projects/index.md` entry, and an optional local binding when `--workspace`
   is supplied. Add optional concepts only when useful.
4. For a tracked project, propose only the smallest durable diff:
   - `README.md` for status, owner, decision, blocker, deadline, source, or next move;
   - `AGENTS.md` for read order, recurring sources, safety, or routing changes.
   - create or update `GOAL.md` only for a useful separate outcome contract;
   - create or update `RESULT.md` only for durable completed evidence;
   - only an explicitly invoked `$ultragoal` may create or update `WORKLOG.md`;
   - use another typed concept when its purpose is clearer than a standard file.
5. Use or create `log.md` only when sparse chronology materially improves
   navigation or synchronization. Never mirror a WORKLOG or routine activity.
6. Show the intended diff and ask before writing unless the user already
   approved that exact update.
7. Preserve `project_id`, unknown frontmatter fields, and the local/portable
   boundary.
8. For a new experiment, preview then apply the plugin-root
   `scripts/create_experiment_pack.py`. It creates `README.md`, `AGENTS.md`, a
   stable `experiment_id`, an experiments index, and optional local bindings.
9. Promote a spike with the plugin-root `scripts/promote_experiment.py` once it
   becomes a durable multi-session workstream. Preserve the Experiment Pack and
   transfer its local bindings to the new Project Pack.
10. Record ignored routes with `scripts/record_ignored_workspace.py` after
   approval so future tasks stay quiet.
11. Use `scripts/transition_packet.py` for deterministic project or experiment
   lifecycle changes; semantic readiness still belongs to the agent. Do not
   write new working state into an archived packet until the user reactivates
   it. Reactivate a completed project before beginning a new durable phase.
   Treat a promoted experiment as preserved origin evidence rather than an
   active work surface.
12. For durable context not owned by a packet, follow
   `../wirenet-manager/references/content-routing.md` and route it to the
   appropriate Manager shelf as a typed concept. Create a shelf `index.md` only
   when real content benefits from progressive disclosure.

## Update Threshold

Update when a future task would otherwise misunderstand the project. Do not
write routine command output, raw transcripts, generated files, temporary
implementation detail, secrets, or unconfirmed inference.

Archive only when no open next move or waiting handoff remains and durable
results have been retained. Waiting and blocked are active lifecycle states,
not archival reasons.

## Resources

- `scripts/inspect_workspace.py`: read-only lookup through local bindings.
- `scripts/record_ignored_workspace.py`: dry-run-first ignored-path recorder.
- plugin-root `scripts/create_experiment_pack.py`: Experiment Pack generator.
- plugin-root `scripts/promote_experiment.py`: experiment-to-project promotion.
- plugin-root `scripts/transition_packet.py`: validated lifecycle transitions.
- `references/update-contract.md`: durable update and routing rules.
- `../wirenet-manager/references/content-routing.md`: shared Manager shelf and
  open Project Pack rules.
