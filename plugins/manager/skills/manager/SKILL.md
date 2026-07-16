---
name: manager
description: Run and maintain the user's ongoing wirenet Manager workspace across Manager-native and external projects. Use when the user asks what is on their plate or what they should know, wants proactive work awareness, asks to keep an eye on work, needs follow-up or check-in help, starts or changes a project or experiment, asks to remember a collaborator, needs a durable project handoff, wants current priorities organized, or resumes a long-running Manager task. Use manager-setup instead for installation, onboarding, upgrades, repair, or QMD configuration.
---

# manager

Act as a quiet, judgment-driven work companion backed by the user's local
Manager. Keep the next move visible without turning the Manager into an activity
log.

## Orient

1. Resolve the Manager from `WIRENET_MANAGER_DIR`, then `~/Manager`.
2. If it is missing or unhealthy, use `$manager-setup`.
3. Read root `AGENTS.md`, `index.md`, `README.md`, and `TODO.md`. Read
   `content_language` from `README.md`; use it for conversation and new
   human-readable prose while keeping stable system fields in English.
4. Read `projects/index.md` for active packets.
5. Read `experiments/index.md` only when it exists and the task concerns a
   bounded spike.
6. Read only the Project Packs, Experiment Packs, and recurring sources relevant
   to the request.
7. Read the relevant playbook before changing project lifecycle, person
   context, or an external-workspace handoff.

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
   and direct file reads. Use `$manager-setup` when the user asks to
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
  archive work, read `references/project-lifecycle.md`.
- When the user asks to remember or update a recurring collaborator, read
  `references/person-context.md`.
- After meaningful progress in an externally bound workspace, read
  `references/workspace-sync.md`.
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

## Open wirenet Inspector

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

## References

Read `references/system-model.md` when explaining the architecture or changing
Manager structure. Read `references/content-routing.md` whenever deciding where
durable information belongs. Load only the task-relevant lifecycle, person, or
sync playbook.
