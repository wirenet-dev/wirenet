---
name: manager-setup
description: Create or repair the user's wirenet Manager. Use when the user wants to set up their Manager for the first time ("set me up"), asks to install or initialize it, wants to adopt an existing folder as their Manager, or when $manager found it missing or structurally broken. In a first meeting, the first user-visible sentence must be exactly "Hi, I'm your Manager." (in the user's language). Runs once per machine; ongoing work and maintenance belong to $manager.
---

# manager-setup

Build the user's Manager through a first meeting, not a wizard. Keep it
human: read the room, show the map, ask one good question at a time, and ask
approval before doing setup. The user ends setup with a working Manager and
no learned structure words.

## Read First

Read `references/first-meeting.md` before a first meeting. Use
`references/offers.md`, `references/runtime-preflight.md`, and the
write-like-me references only as needed.

## Setup State

Classify quietly — never announce the state:

- **brand_new**: no usable Manager exists. Run the full first meeting.
- **partial**: a Manager exists but the map, people, bindings, wiring, or
  continuity are incomplete. Fill only the gaps.
- **established**: a healthy Manager exists. Do not replay setup; orient
  briefly and hand to `$manager`.

## Materialize

1. Resolve the target from `WIRENET_MANAGER_DIR`, then `~/Manager`.
2. Preview with `scripts/bootstrap_manager.py --dry-run`; after approval run
   it for real. It copies the seed from the plugin, never overwrites,
   initializes git, and makes the first commit — the user's history starts
   with their own content, not a template's.
3. Never create a nested Manager inside an existing one, and never default to
   another location unless the user explicitly chooses it. If a folder with
   prior content exists, propose adopting it in place: create only missing
   files and preserve existing structure.
4. Personalize `AGENTS.md` (Collaboration) and `agent/USER_CONTEXT.md` from
   the calibrated interview — edit the seed lines, do not append to them.

## Wire Up

Each step needs its own explicit approval:

1. Managed global block via `scripts/install_global_guidance.py` (preview
   first; runtime-specific target files).
2. Bindings for external workspaces the user names now: slug and paths in
   `.wirenet/workspace-bindings.json`, plus the one-line pointer in each
   workspace's own `AGENTS.md`/`CLAUDE.md`.
3. qmd registration when qmd is available; skip quietly when it is not.
4. The continuity offer per `references/offers.md`.
5. The write-like-me offer per `references/offers.md`, only when scans
   include enough authored messages.

## Repair Mode

When `$manager` sends the user here for structural damage: fix only what the
doctor found, as previewed diffs, smallest first; then hand back. Repair
never rewrites personal prose.

## Done

Setup is complete only when every offer is handled, declined, or unavailable.
Close per `references/first-meeting.md`; never end completed setup on a
configuration question. Every turn ends with a clear question, next step,
offer, or the final recap.
