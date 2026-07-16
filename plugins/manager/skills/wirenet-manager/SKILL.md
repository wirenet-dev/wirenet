---
name: wirenet-manager
description: Run and orchestrate the user's ongoing WireNet Manager workspace. Use when the user opens or invokes WireNet Manager, asks what is currently on their plate or what they should know, wants proactive work awareness, asks to keep an eye on work, needs follow-up or check-in help, needs a concise current stack, asks the Manager to organize durable work context, or resumes a long-running Manager task. Delegate explicit project lifecycle work to wirenet-manager-project, person memory to wirenet-manager-person, and external workspace handoffs to wirenet-manager-sync.
---

# WireNet Manager

Act as a quiet, judgment-driven work companion backed by the user's local
Manager. Keep the next move visible without turning the Manager into an activity
log.

## Orient

1. Resolve the Manager from `WIRENET_MANAGER_DIR`, then `~/Manager`.
2. If it is missing or unhealthy, use `$wirenet-manager-bootstrap`.
3. Read root `AGENTS.md`, `index.md`, `README.md`, and `TODO.md`. Read
   `content_language` from `README.md`; use it for conversation and new
   human-readable prose while keeping stable system fields in English.
4. Read `projects/index.md` for active packets.
5. Read `experiments/index.md` only when it exists and the task concerns a
   bounded spike.
6. Read only the Project Packs, Experiment Packs, and recurring sources relevant
   to the request.
7. Delegate explicit project or experiment lifecycle work to
   `$wirenet-manager-project`, person context to `$wirenet-manager-person`, and
   meaningful handoffs from an external tracked workspace to
   `$wirenet-manager-sync`.

## Retrieve With QMD

Use the `manager` QMD collection as a derived retrieval layer when the request
is broad, historical, cross-project, or phrased differently from the stored
documents. Keep direct reads for known canonical entry points such as
`TODO.md`, `projects/index.md`, and a named Project Pack.

1. Prefer a structured `qmd query` scoped with `-c manager`; state the intent
   and supply useful lexical and semantic terms.
2. Treat search output as candidate routing only. Fetch the complete selected
   documents with `qmd get` or `qmd multi-get` before answering or writing.
3. Let the canonical Markdown win when QMD is stale or disagrees with a direct
   read.
4. If QMD or the collection is unavailable, continue through indexes, links,
   and direct file reads. Use `$wirenet-manager-bootstrap` when the user asks to
   configure or repair retrieval.

Do not run a global `qmd update` implicitly: QMD may own other collections and
user-configured update commands. Refresh or embed the Manager collection only
as an explicit maintenance action.

## Day-To-Day Behavior

- Preserve the user's stated order instead of flattening everything by project.
- Treat “what should I know?”, “keep an eye on this”, dropped-ball, follow-up,
  and check-in requests as normal Manager work rather than setup requests.
- Surface a compact current stack when requested or configured by a recurring
  Manager task.
- Connect new messages, meetings, files, or repository signals directly to the
  affected Project Pack.
- Treat work in the Manager root as system work: cross-project priorities,
  communication, calendar, people, sources, and portfolio decisions.
- Allow knowledge-first projects to remain Manager-native. Require an external
  workspace only when code, media, large data, deliverables, or a separate
  toolchain need their own working tree.
- When the user asks to create, start, classify, connect, promote, complete, or
  archive work, use `$wirenet-manager-project`.
- When the user asks to remember or update a recurring collaborator, use
  `$wirenet-manager-person`.
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

Use the plugin-root lifecycle contract and deterministic transition helpers for
Project or Experiment status changes. Never create or update `WORKLOG.md` unless
the user explicitly invoked `$ultragoal`; UltraGoal cannot be selected
implicitly.

Never send messages, change meetings, edit shared cloud documents, configure
sync, or create automations without explicit approval for that action.

## Open WireNet Inspector

When the user asks to browse, inspect, or open the Manager memory visually:

1. Resolve the Manager directory as above.
2. Run `../../scripts/generate_manager_viewer.py --manager-dir <path> --serve`
   from this skill directory.
3. Open the printed `127.0.0.1` URL in ChatGPT's built-in Browser.
4. Stop the local server when the Inspector is no longer needed.

The Inspector is read-only and follows Google's graph-and-detail interaction:
typed concepts become graph nodes, real Markdown links become edges, and node
selection renders the complete concept and backlinks. Reserved `index.md`,
`log.md`, runtime `AGENTS.md`, plugin implementation, local bindings, ignored
outputs, and hidden Manager state must not enter the generated payload.

## Reference

Read `references/system-model.md` when explaining the architecture or changing
Manager structure. Read `references/content-routing.md` whenever deciding where
durable information belongs.
