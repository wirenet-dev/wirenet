---
name: wirenet-manager-bootstrap
description: Set up, upgrade, inspect, repair, or explain the technical WireNet Manager workspace. Use when someone installs or updates WireNet Manager, creates ~/Manager, sees a workspace-schema mismatch, checks Manager health, configures QMD retrieval, or needs to continue into first-time personal onboarding after the local baseline is healthy.
---

# WireNet Manager Bootstrap

Create or repair the technical Manager baseline conservatively. Bootstrap owns
filesystem, schema, Git, Doctor, QMD, and managed-global-instruction mechanics.
`$wirenet-manager-onboarding` owns the personal first meeting.

Read `references/runtime-preflight.md` before running any Python, Git, upgrade,
or QMD helper. Resolve bundled Codex executables when available so the user does
not need a developer setup.

Do not clone the product repository into the user's personal Manager. The
installed plugin owns behavior; `~/Manager` owns personal content and local
history; external projects stay where they are.

## Technical Workflow

1. Complete the runtime preflight. Invoke helpers with the resolved Python
   executable and pass the resolved Git executable with `--git-bin`. Stop before
   writing if either runtime cannot be resolved.
2. Infer the human content language from the setup request. State it once and
   ask only when ambiguous. Recommend `~/Manager` unless the user chooses
   another location. Pass the BCP 47-style tag to
   `bootstrap_manager.py --content-language`; stable system structure remains
   English.
3. When `.wirenet/manager.json` exists, preview the plugin-root
   `scripts/upgrade_manager.py --git-bin <resolved-git>` result.
   - `current`: continue to Doctor.
   - `upgrade-available`: require a clean local Git checkpoint, show the plan,
     and ask before applying.
   - `plugin-too-old`: stop and ask the user to update the plugin.
   - `manual-review`, `recovery-required`, `unsupported`: stop rather than
     guessing.
4. Preview `scripts/bootstrap_manager.py --git-bin <resolved-git>` without
   `--apply`.
5. Ask before creating or repairing the directory, then rerun with `--apply`.
   Use `--repair` only for an existing Manager; repair creates missing scaffold
   and never overwrites personalized files.
6. Require Manager Doctor `ok: true`.
7. Preview plugin-root `scripts/manager_qmd.py`.
   - If QMD is healthy, offer the `manager` collection registration.
   - If missing or unhealthy, explain the state and ask before using `--install`.
   - Add `--embed` only after separate approval for model-backed embeddings.
   - QMD failure does not invalidate the Manager; canonical file reads remain.
8. When the technical baseline is healthy, continue in the same task with
   `$wirenet-manager-onboarding` for a brand-new or incomplete first meeting.
   Do not present the technical recap as completed onboarding.

## Setup Operations Used During Onboarding

Run these only when the onboarding map makes them useful and the user approves
their exact scope:

- Discover explicitly named project roots with plugin-root
  `scripts/discover_projects.py`; never scan the whole home directory.
- Classify each relevant folder as project, bounded experiment, or ignored.
- Preview then create Project Packs with plugin-root
  `scripts/create_project_pack.py`; create Experiment Packs with
  `scripts/create_experiment_pack.py`; record ignored workspaces with
  `../wirenet-manager-sync/scripts/record_ignored_workspace.py`.
- Preview `scripts/install_global_guidance.py` before adding the core managed
  block to global `AGENTS.md`.
- Offer the optional routing block only when the user already has a stable
  workspace convention. Do not invent a folder hierarchy or keep duplicate
  manual and managed routing rules.

## Upgrade Safety

Ask before applying a workspace migration. Require a clean local Git checkpoint,
run the updater with `--apply`, require Doctor `ok: true`, inspect the diff, and
commit only the planned structural migration. Never overwrite personal prose or
user routing rules. A plugin update is never permission to mutate personal
Manager content.

## Safety

- Never move, copy, upload, or index raw project media or source trees.
- Keep absolute workspace paths only in `.wirenet/workspace-bindings.json`.
- Preserve existing global instructions outside managed blocks.
- Never silently add a Git remote, cloud database, sync service, communication
  connection, source read, automation, or inferred personal knowledge.
- Never overwrite a QMD collection name that points elsewhere.
- Accept only the canonical workspace contract or a supported deterministic
  migration. Leave ambiguous layouts untouched for explicit review.

## Resources

- `scripts/bootstrap_manager.py`: dry-run-first seed, local Git initialization,
  repair, and Doctor wrapper.
- `scripts/install_global_guidance.py`: idempotent core and optional routing
  block installer.
- `references/runtime-preflight.md`: Codex-bundled and PATH executable
  resolution for non-developer computers.
- plugin-root `scripts/upgrade_manager.py`: version negotiation and migration.
- plugin-root `scripts/manager_qmd.py`: QMD health and collection setup.
- `references/manager-model.md`: canonical workspace model.
