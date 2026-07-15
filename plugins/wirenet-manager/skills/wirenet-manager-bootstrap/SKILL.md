---
name: wirenet-manager-bootstrap
description: Set up, inspect, repair, or explain a local WireNet Manager workspace. Use when someone installs WireNet Manager, bootstraps ~/Manager, checks Manager health, migrates from an earlier Artbeats Seed or vault, connects existing project folders, or installs the global Project Pack trigger.
---

# WireNet Manager Bootstrap

Set up the Manager conservatively from the content-only template bundled with
the installed plugin. Do not clone the product repository into the user's
personal Manager.

## Workflow

1. Explain the boundary: the plugin owns behavior; `~/Manager` owns content and
   local history; external projects stay where they are.
2. Recommend `~/Manager` unless the user chooses another location.
3. Run `scripts/bootstrap_manager.py` without `--apply` and show the plan.
4. Ask for approval before creating or repairing the directory.
5. Rerun with `--apply`. For an existing Manager, use `--repair`; repair creates
   only missing scaffold and never overwrites personalized files.
6. Require the returned doctor result to have `ok: true`.
7. Ask which project roots may be inspected. Run the plugin-root
   `scripts/discover_projects.py` only on explicitly approved roots.
8. Present candidates and classify each relevant folder as project,
   experiment, or ignored.
9. For approved projects, preview then apply the plugin-root
   `scripts/create_project_pack.py`. It creates an open packet with `README.md`
   and `AGENTS.md`, updates both the Jason-compatible README router and additive
   OKF index, and stores one stable `project_id`. Add optional goal, result, log,
   worklog, index, or other concepts only when useful.
10. Preview `scripts/install_global_guidance.py`; ask before applying the core
    managed block to the user's global `AGENTS.md`.
11. Ask one optional routing question: does the user already have a stable
    workspace convention they want Codex to follow everywhere? If yes, propose
    the smallest useful one-line rules and preview them with repeated
    `--routing-rule` arguments. If no, install no routing block and do not
    invent or impose a folder structure. Existing project bindings are enough.
12. If an existing global section already describes workspace roots, offer to
    replace it with the optional managed routing block. Never keep manual and
    managed copies of the same rules.
13. Offer a pinned Manager task and optional recurring check-in. Create or
    change tasks and automations only with explicit approval.

## Safety

- Never move, copy, upload, or index raw project media or source trees.
- Never scan the whole home directory without an explicit root choice.
- Keep absolute workspace paths only in `.wirenet/project-bindings.json`.
- Preserve existing global instructions outside the managed blocks.
- Treat the optional global routing block as its own source of truth. Do not
  mirror it into Manager JSON or Project Packs in v0.1.
- Change or remove routing only after explicit approval. Never reorganize a
  user's folders merely because their current system looks inconsistent.
- Never silently add a Git remote, cloud database, or sync service.
- For older vaults, propose a disposable reviewed migration before changing the
  live folder.

## Resources

- `scripts/bootstrap_manager.py`: dry-run-first seed, local Git initialization,
  repair, and doctor wrapper.
- `scripts/install_global_guidance.py`: idempotent core and optional routing
  block installer, including migration from the earlier single block.
- `references/manager-model.md`: canonical v0.1 structure and routing model.
