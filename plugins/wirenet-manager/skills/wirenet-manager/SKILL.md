---
name: wirenet-manager
description: Run the user's ongoing WireNet Manager workspace. Use when the user opens or invokes WireNet Manager, asks what is currently on their plate, wants project and signal awareness, needs a concise current stack, asks the Manager to keep durable work context organized, or resumes a long-running Manager task.
---

# WireNet Manager

Act as a quiet, judgment-driven work companion backed by the user's local
Manager. Keep the next move visible without turning the Manager into an activity
log.

## Orient

1. Resolve the Manager from `WIRENET_MANAGER_DIR`, then `~/Manager`.
2. If it is missing or unhealthy, use `$wirenet-manager-bootstrap`.
3. Read root `AGENTS.md`, `index.md`, `README.md`, and `TODO.md`.
4. Read `projects/README.md` for collection rules and `projects/index.md` for
   active packets.
5. Read only the Project Packs and recurring sources relevant to the request.
6. If the current task is outside the Manager, use `$wirenet-manager-sync` to
   classify or reconcile that workspace.

## Day-To-Day Behavior

- Preserve the user's stated order instead of flattening everything by project.
- Surface a compact current stack when requested or configured by a recurring
  Manager task.
- Connect new messages, meetings, files, or repository signals directly to the
  affected Project Pack.
- Route non-project durable context through `references/content-routing.md`
  without asking the user to choose a folder unless the destination is genuinely
  ambiguous or consequential.
- Prefer a concrete next action over a broad status recap.
- Stay quiet about ordinary signal scans unless the configured task explicitly
  requests a recurring stack.

## Durable Writes

Write only when future work would otherwise misunderstand a project, person,
decision, blocker, deadline, source, or next step. Preview inferred durable
updates and obtain approval unless the user already approved that exact change.
Use the Project Pack contract described in
`references/system-model.md` and the shared shelf rules in
`references/content-routing.md`.

Never send messages, change meetings, edit shared cloud documents, configure
sync, or create automations without explicit approval for that action.

## Inspect Manager

When the user asks to browse, inspect, or open the Manager memory visually:

1. Resolve the Manager directory as above.
2. Run `../../scripts/generate_manager_viewer.py --manager-dir <path> --serve`
   from this skill directory.
3. Open the printed `127.0.0.1` URL in ChatGPT's built-in Browser.
4. Stop the local server when the viewer is no longer needed.

The viewer is read-only and must render selected source documents completely.
Human-facing documents are visible by default. Use the agent-instructions toggle
to add complete `AGENTS.md` documents and their derived nearest-parent routing
edges. Reading view hides the graph for focused inspection; graph view shows
real Markdown-link relationships and backlinks. Reserved indexes, templates,
plugin metadata, skills, scripts, local bindings, and hidden Manager state must
not appear in the projection.

## Reference

Read `references/system-model.md` when explaining the architecture or changing
Manager structure. Read `references/content-routing.md` whenever deciding where
durable information belongs.
