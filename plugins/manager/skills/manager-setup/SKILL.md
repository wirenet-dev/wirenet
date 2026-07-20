---
name: manager-setup
description: Set up, onboard, upgrade, inspect, repair, or explain a local wirenet Manager workspace. Use after installing or updating manager@wirenet, when creating ~/Manager, continuing the first personal meeting, learning the user's work and writing voice, resolving a workspace-schema mismatch, checking Manager health, or configuring QMD retrieval.
---

# manager setup

Create or repair the technical Manager baseline conservatively. Bootstrap owns
filesystem, schema, Git, Doctor, QMD, and managed-global-instruction mechanics.
This skill also owns the personal first meeting after the technical baseline is
healthy.

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
7. Run plugin-root `scripts/manager_doctor.py --check-updates` when a public
   GitHub read is available. If the installed plugin is current, read the
   packaged `RELEASE_NOTES.md` and close an update task with a concise report:
   installed version, workspace-migration result (`none` is valid), up to three
   user-facing release-note bullets, and final Doctor status. An unavailable
   release check does not invalidate a healthy Manager.
8. Preview plugin-root `scripts/manager_qmd.py`.
   - If QMD is healthy, offer the `manager` collection registration.
   - If missing or unhealthy, explain the state and ask before using `--install`.
   - Add `--embed` only after separate approval for model-backed embeddings.
   - QMD failure does not invalidate the Manager; canonical file reads remain.
9. When the technical baseline is healthy, read `references/onboarding.md` and
   continue the first meeting in the same task. Do not present the technical
   recap as completed onboarding.

## Setup Operations Used During Onboarding

Run these only when the onboarding map makes them useful and the user approves
their exact scope:

- Discover explicitly named project roots with plugin-root
  `scripts/discover_projects.py`; never scan the whole home directory.
- Classify each relevant folder as project, bounded experiment, or ignored by
  following `../manager/references/project-lifecycle.md`.
- Preview then create Project Packs with plugin-root
  `scripts/create_project_pack.py`; create Experiment Packs with
  `scripts/create_experiment_pack.py`; record ignored workspaces with
  plugin-root `scripts/record_ignored_workspace.py`.
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
- `references/onboarding.md`: first-meeting workflow and approval gates.
- `references/first-meeting-flow.md`: detailed conversation sequence.
- `references/write-like-me.md`: optional personal voice-skill setup.
