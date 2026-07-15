---
name: wirenet-manager-bootstrap
description: Set up, upgrade, inspect, repair, or explain a canonical local WireNet Manager workspace. Use when someone installs or updates WireNet Manager, bootstraps ~/Manager, sees a workspace-schema mismatch, checks Manager health, connects existing project folders, or installs the global Project Pack trigger.
---

# WireNet Manager Bootstrap

Set up the Manager conservatively from the content-only template bundled with
the installed plugin. Do not clone the product repository into the user's
personal Manager.

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
9. Ask which project roots may be inspected. Run the plugin-root
   `scripts/discover_projects.py` only on explicitly approved roots.
10. Present candidates and classify each relevant folder as project,
   experiment, or ignored.
11. For approved projects, preview then apply the plugin-root
   `scripts/create_project_pack.py`. It creates an open packet with `README.md`
   and `AGENTS.md`, updates the canonical `projects/index.md`, and stores one
   stable `project_id`. Add optional goal, result, log, worklog, index, or other
   concepts only when useful. Omit `--workspace` for a knowledge-first,
   Manager-native project.
12. For approved bounded experiments, preview then apply the plugin-root
   `scripts/create_experiment_pack.py`. It creates a lightweight packet and
   optional workspace binding rather than a full project.
13. Record approved ignored folders with
   `../wirenet-manager-sync/scripts/record_ignored_workspace.py`.
14. Preview `scripts/install_global_guidance.py`; ask before applying the core
    managed block to the user's global `AGENTS.md`.
15. Ask one optional routing question: does the user already have a stable
    workspace convention they want Codex to follow everywhere? If yes, propose
    the smallest useful one-line rules and preview them with repeated
    `--routing-rule` arguments. If no, install no routing block and do not
    invent or impose a folder structure. Existing project bindings are enough.
16. If an existing global section already describes workspace roots, offer to
    replace it with the optional managed routing block. Never keep manual and
    managed copies of the same rules.
17. Offer a pinned Manager task and optional recurring check-in. Create or
    change tasks and automations only with explicit approval.

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
- `references/manager-model.md`: canonical v0.2 structure and routing model.
