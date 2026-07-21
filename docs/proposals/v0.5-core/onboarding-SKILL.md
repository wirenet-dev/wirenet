---
name: manager-onboarding
description: Create or repair the user's wirenet Manager. Use when the user wants to set up their Manager for the first time, says "onboard me", asks to install or initialize the Manager, wants to adopt an existing folder as their Manager, or when $manager found the Manager missing or structurally broken. Runs once per machine; ongoing work and maintenance belong to $manager.
---

# manager-onboarding

Build the user's Manager through a conversation, not a configuration. The user
should end onboarding with a working Manager and no learned structure words.

## Preflight

1. Resolve the target from `WIRENET_MANAGER_DIR`, then `~/Manager`.
2. If a healthy Manager already exists, say so and hand off to `$manager` — do
   not re-onboard. If a folder exists with prior content, propose adopting it
   in place; never overwrite existing files without an approved plan.
3. In repair mode (sent here by `$manager`), fix only what the doctor found,
   as previewed diffs, then hand back.

## Interview

Ask small, concrete questions and draft as you go — propose, don't quiz:

1. Who are you and what do you do? → draft root `README.md` and
   `agent/USER_CONTEXT.md` (role, working style, boundaries).
2. What is on your plate right now? → draft `TODO.md` as an ordered stack
   (Now / Next / Waiting / Later), each item with an owner and next step.
3. Which two or three workstreams matter most? → draft one pack each:
   `projects/<slug>/README.md` with status, decisions, next move; a pack
   `AGENTS.md` only when real recurring sources or safety rules exist.
4. Who do you work with repeatedly? → draft one `people/<slug>.md` per named
   recurring collaborator; skip one-off names.
5. With approval, scan connected sources (mail, calendar, repositories) for
   evidence — recent recurring threads, deadlines, active repos — and refine
   the drafts. Store synthesis only, never raw messages.

Follow the Manager shape in the `$manager` reference `vault-model.md`. Create
only the core files; optional folders appear later on first real content.

## Voice And Instructions

- Personalize the Manager's root `AGENTS.md` from the interview: confirmed
  collaboration tone, decision latitude, and attention boundaries. The managed
  template stays one page; personalization edits it, never grows it.
- Offer the write-like-me bootstrap (see `references/write-like-me.md`): with
  separately approved source scopes — user-authored sent mail and messages,
  usually the last 90–180 days — infer voice and postures and generate a
  personal write-like-me skill at the global skill root, outside the Manager.
  Synthetic examples only, never raw excerpts; reading sources and writing the
  generated skill are separate approvals. Skip without friction when the user
  declines; offer again only on request.

Each with its own explicit approval:

1. Initialize git in the Manager and make the first commit. Offer a private
   remote and push windows; configure nothing unasked.
2. Install the managed global block (~5 lines) into the global
   `AGENTS.md`/`CLAUDE.md`: the Manager's location, read-the-pack-first in
   bound workspaces, propose-an-update after meaningful progress.
3. Register the Manager as a qmd collection when qmd is available; skip quietly
   when it is not.
4. Bind external project folders the user names now (slug → path in
   `.wirenet/workspace-bindings.json`, plus the one-line pointer in each
   workspace's own `AGENTS.md`, per `vault-model.md`).

## Done

Run the doctor, then show the user what exists in their words: "You have a
stack, three projects, two people. Ask me 'what's on my plate?' anytime — I'll
keep this current and always ask before writing." Hand off to `$manager`.

Success criterion: after ~30 minutes the user has `TODO.md`, two or three
packs, and at least one person file — and has not learned a single structure
word.
