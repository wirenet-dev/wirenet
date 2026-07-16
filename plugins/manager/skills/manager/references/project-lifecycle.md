---
last_edited: 2026-07-16
---

# Project And Experiment Lifecycle

Own Project and Experiment Pack lifecycle. Keep creation and lifecycle decisions
explicit while reusing the plugin's deterministic dry-run-first helpers.

## Route The Work

1. Resolve Manager from `WIRENET_MANAGER_DIR`, then `~/Manager`. Use
   `$manager-setup` if it is missing or unhealthy.
2. Read root `AGENTS.md`, `README.md`, the relevant collection index, and the
   shared rules in `content-routing.md`.
3. Classify by durable shape:
   - **project**: multi-session work with durable state, handoffs, or its own
     file world;
   - **experiment**: a bounded spike with a question and decision criterion;
   - **ignored**: a folder that should not produce Manager reminders.
4. Keep a knowledge-first project Manager-native. Bind an external workspace
   only when code, media, data, deliverables, or a separate toolchain need their
   own working tree.
5. Use `workspace-sync.md` instead when an already tracked workspace only needs
   a meaningful status, decision, blocker, result, or next-step handoff.

## Create Or Classify

- Preview a Project Pack with plugin-root `scripts/create_project_pack.py`.
  Create only `README.md` and `AGENTS.md` by default; add optional concepts only
  when they already have a purpose.
- Preview an Experiment Pack with plugin-root
  `scripts/create_experiment_pack.py`. Require a real question and decision
  criterion rather than treating every short task as an experiment.
- Inspect an external workspace with plugin-root `scripts/inspect_workspace.py`.
  For an ignored folder, preview then use plugin-root
  `scripts/record_ignored_workspace.py`.
- Never scan the whole home directory or copy a source tree into Manager.
- Show the classification and dry-run output, then ask before applying it.

## Manage Lifecycle

- Preview every state change with plugin-root `scripts/transition_packet.py`.
- Keep waiting and blocked projects live. Complete only when the current outcome
  is done; archive only when no open next move or waiting handoff remains and
  durable results are retained.
- Reactivate a completed or archived project before beginning a new durable
  phase.
- Promote an experiment with plugin-root `scripts/promote_experiment.py` when
  it becomes durable multi-session work. Preserve the experiment as origin
  evidence and transfer its local binding.
- Never write new active state into an archived packet or a promoted experiment.

## Safety

Preserve stable IDs, unknown metadata, personal prose, and the portable/local
boundary. Preview inferred durable changes and obtain approval unless the user
already approved that exact change. Never create `WORKLOG.md`; only an
explicitly invoked `$ultragoal` owns it.
