# External Workspace Sync

Keep packs useful without turning them into activity logs. The managed global
block is the reliable cross-project trigger; this reference defines what to do
when it fires.

## Workflow

1. Look up the current workspace path in
   `~/Manager/.wirenet/workspace-bindings.json`.
   - **Bound project**: read the pack's `README.md` (and `AGENTS.md` if
     present) before working; continue below after meaningful progress.
   - **Bound experiment**: preserve its question and decision criterion;
     record only meaningful observations or results.
   - **Ignored**: stay quiet.
   - **Untracked but durable-looking**: ask once whether it is a project, an
     experiment, or an ignored folder, then follow `vault-model.md`. Do not
     re-ask per session.
2. After meaningful progress, propose the smallest durable diff:
   - pack `README.md` for the handoff — status, owner, decision, blocker,
     deadline, source, next move;
   - pack `AGENTS.md` only for changed recurring sources, safety rules, or
     read order;
   - `GOAL.md` / `RESULT.md` only when the outcome contract or completed
     evidence earns a separate document.
3. Show the intended diff and ask before writing, unless the user already
   approved that exact update.

## Threshold

Update when a future task would otherwise resume from the wrong state. Do not
mirror commands, test runs, transcripts, generated files, or implementation
detail that will not matter next session. One compact handoff after a
meaningful work phase beats many small writes.

Lifecycle changes (complete, archive, promote, reactivate) are not sync;
route them through `vault-model.md` after the handoff is reconciled.
