---
name: wirenet-manager-bootstrap
description: Set up, upgrade, inspect, repair, or explain a canonical local WireNet Manager workspace. Use when someone installs or updates WireNet Manager, bootstraps ~/Manager, sees a workspace-schema mismatch, checks Manager health, connects existing project folders, or installs the global Project Pack trigger.
---

# WireNet Manager Bootstrap

Set up the Manager conservatively from the content-only template bundled with
the installed plugin. Do not clone the product repository into the user's
personal Manager.

For a new or incomplete installation, read
`references/first-run-experience.md` before starting. Classify the setup as
brand new, partial, or established and run only the missing first-run phases.

## Workflow

1. Explain the boundary: the plugin owns behavior; `~/Manager` owns content and
   local history; external projects stay where they are.
2. Recommend `~/Manager` unless the user chooses another location.
3. Run the plugin-root `scripts/upgrade_manager.py` without `--apply` when
   `.wirenet/manager.json` already exists.
   - `current`: continue with the normal health check.
   - `upgrade-available`: show the deterministic migration plan and require a
     clean local Git checkpoint before applying it.
   - `plugin-too-old`: stop and ask the user to update the plugin.
   - `manual-review`, `recovery-required`, or `unsupported`: stop and explain
     the exact unresolved state rather than guessing.
4. Ask for approval before applying a migration. Rerun the updater with
   `--apply`, require Doctor `ok: true`, inspect the resulting local Git diff,
   and create a migration commit after confirming it contains only the planned
   structural changes. Never overwrite personal prose or user routing rules.
5. Run `scripts/bootstrap_manager.py` without `--apply` and show the plan.
6. Ask for approval before creating or repairing the directory.
7. Rerun with `--apply`. For an existing Manager, use `--repair`; repair creates
   only missing scaffold and never overwrites personalized files.
8. Require the returned doctor result to have `ok: true`.
9. Run the plugin-root `scripts/manager_qmd.py` without `--apply`.
   - If QMD is healthy, preview registration of the Manager as the `manager`
     collection.
   - If QMD is missing or unhealthy, explain the detected state and ask before
     installing or repairing the pinned tested package with `--install`.
   - Apply collection setup only after approval. Add `--embed` only when the
     user also approves the model-backed semantic index; lexical indexing is
     already useful without it.
   - A QMD failure never invalidates the Manager workspace. Report retrieval as
     unavailable and continue with canonical file reads.
10. For a brand-new or incomplete setup, follow the work-map and communication
    setup in `references/first-run-experience.md`.
    - Ask what is currently on the user's plate and return a compact map before
      proposing durable content.
    - Inspect available communication and work-source capabilities and
      recommend only what the map makes useful.
    - Keep installation, connection, source reading, and inferred durable
      writes as separate explicit approval gates.
11. Ask which project roots may be inspected. Run the plugin-root
   `scripts/discover_projects.py` only on explicitly approved roots.
12. Present candidates and classify each relevant folder as project,
   experiment, or ignored.
13. For approved projects, preview then apply the plugin-root
   `scripts/create_project_pack.py`. It creates an open packet with `README.md`
   and `AGENTS.md`, updates the canonical `projects/index.md`, and stores one
   stable `project_id`. Add optional goal, result, log, worklog, index, or other
   concepts only when useful. Omit `--workspace` for a knowledge-first,
   Manager-native project.
14. For approved bounded experiments, preview then apply the plugin-root
   `scripts/create_experiment_pack.py`. It creates a lightweight packet and
   optional workspace binding rather than a full project.
15. Record approved ignored folders with
   `../wirenet-manager-sync/scripts/record_ignored_workspace.py`.
16. Preview `scripts/install_global_guidance.py`; ask before applying the core
    managed block to the user's global `AGENTS.md`.
17. Ask one optional routing question: does the user already have a stable
    workspace convention they want Codex to follow everywhere? If yes, propose
    the smallest useful one-line rules and preview them with repeated
    `--routing-rule` arguments. If no, install no routing block and do not
    invent or impose a folder structure. Existing project bindings are enough.
18. If an existing global section already describes workspace roots, offer to
    replace it with the optional managed routing block. Never keep manual and
    managed copies of the same rules.
19. Explain the four daily-use paths in the first-run reference: current stack,
    external workspace tracking, Inspector, and durable reconciliation.
20. Offer to keep the current task as the Manager home and create one quiet
    recurring Manager check-in there. Recommend an hourly cadence unless the
    user prefers another cadence or no automation. Use the automation tool with
    the current task as destination and the contract in the first-run
    reference. Create, rename, or pin tasks and create or change automations only
    with explicit approval for each action.
21. Close with the first-run recap and the smallest useful next action. Do not
    claim setup is complete while a required phase is unresolved.

## Safety

- Never move, copy, upload, or index raw project media or source trees.
- Never scan the whole home directory without an explicit root choice.
- Keep absolute workspace paths only in `.wirenet/workspace-bindings.json`.
- Preserve existing global instructions outside the managed blocks.
- Treat the optional global routing block as its own source of truth. Do not
  mirror it into Manager JSON or packets in v0.2.
- Change or remove routing only after explicit approval. Never reorganize a
  user's folders merely because their current system looks inconsistent.
- Never silently add a Git remote, cloud database, or sync service.
- Never install or connect a communication or work-source plugin, read a
  connected source for onboarding, or persist inferred context without its own
  explicit approval.
- Never install, repair, or embed QMD without explicit approval. QMD is a
  derived local retrieval index, not canonical Manager state.
- Never overwrite an existing QMD collection name that points elsewhere. Use a
  user-approved alternate collection name instead.
- Never treat a plugin update as permission to mutate personal Manager content.
  Workspace migration remains dry-run-first and explicitly approved.
- Bootstrap accepts only the canonical v0.2 contract. If an existing folder
  uses a supported older WireNet schema, use the deterministic updater. If it
  uses another layout or an unsupported schema, leave it untouched and
  bootstrap a fresh target for explicit review instead of improvising a
  translation.

## Resources

- `scripts/bootstrap_manager.py`: dry-run-first seed, local Git initialization,
  repair, and doctor wrapper.
- `scripts/install_global_guidance.py`: idempotent core and optional routing
  block installer.
- plugin-root `scripts/upgrade_manager.py`: dry-run-first version negotiation
  and supported workspace migrations.
- plugin-root `scripts/manager_qmd.py`: QMD health, approved installation,
  Manager collection registration, retrieval context, and optional embeddings.
- `references/manager-model.md`: canonical v0.2 structure and routing model.
- `references/first-run-experience.md`: work-map interview, source setup,
  day-to-day handoff, first Manager check-in, and completion contract.
