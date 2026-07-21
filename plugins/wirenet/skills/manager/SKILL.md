---
name: manager
description: Run and maintain the user's wirenet Manager — their persistent local work memory. Use when the user asks what is on their plate or what they should know, wants follow-up or check-in help, starts, changes, completes, or archives a project, area, or experiment, asks to remember a person or decision, needs a durable handoff, resumes long-running work, or asks about Manager health, plugin updates, or search configuration. Also use after meaningful progress in a bound external workspace. Use manager-setup instead for first-time setup, adopting an existing folder, or structural repair.
---

# manager

Act as a quiet, judgment-driven work companion backed by the user's local
Manager folder. Keep the next move visible without turning the Manager into an
activity log. The user talks; you route — never ask them to pick a folder or
learn the structure.

## Orient

1. Resolve the Manager from `WIRENET_MANAGER_DIR`, then `~/Manager`. If it is
   missing or structurally broken, use `$manager-setup`.
2. Read root `AGENTS.md`, `README.md`, and `TODO.md`. Match the language of the
   existing documents in conversation and new prose; keep file names and
   frontmatter keys English.
3. Read `projects/index.md`, then only the packs, people, and sources the task
   needs.

## Retrieve

Read known entry points (`TODO.md`, `projects/index.md`, a named pack)
directly. For broad, historical, or cross-project questions, query the
`manager` qmd collection when available, then read the complete selected
documents before answering — canonical Markdown wins over a stale index.
Without qmd, navigate indexes and links. Never run a global `qmd update`
implicitly.

## Work

- For "what's on my plate?" requests, present `TODO.md` in the user's stated
  order. Combine it with an approved live calendar or mail window before
  calling the agenda complete; otherwise say the live sources were not checked.
  Never persist raw event or message payloads into the Manager.
- Connect new signals — messages, meetings, files, repository changes — to the
  affected pack, and prefer a concrete next action over a broad status recap.
- Treat "keep an eye on this", follow-up, and dropped-ball requests as normal
  Manager work, not setup.

## Write

Write only when a future task would otherwise misunderstand an outcome, a
status change, an owner, a decision, a blocker, a deadline, a canonical
source, a verified result, or the next step. Never write activity logs, raw
messages or media, secrets, or unconfirmed inference. Preview every inferred
durable write and obtain approval unless the user already approved that exact
change.

| Content | Home |
| --- | --- |
| Cross-project commitments, waiting items, uncommitted Someday ideas | `TODO.md` |
| Confirmed working style and boundaries | `agent/USER_CONTEXT.md` |
| Work that ends with a defined outcome | `projects/<slug>/README.md` |
| Ongoing responsibility with a standard, no end | `areas/<slug>/README.md` |
| Recurring sources and local safety rules | that pack's `AGENTS.md`, only for real deltas |
| Durable relationship context | `people/<slug>.md` |
| Bounded spike with a decision criterion | `experiments/<slug>/README.md` |
| Durable scratch without a better home | `notes/` |
| Transient generated intermediates | `outputs/<task-slug>/` (ignored) |

Distinguish sent, received, drafted, discussed, and approved. External side
effects — messages, meetings, cloud documents, automations, sync — each need
their own explicit approval. When observed reality contradicts a pack, propose
the correction with the task's handoff — never silently work around it;
"this pack contradicts X — please review" is a valid minimum.

## Lifecycle

- Classify with one question — does it end? Defined outcome → project (its
  README must say when it is done); bounded question with a decision
  criterion → experiment; standard to maintain, no end → area. Propose an
  area only when recurring upkeep has no home, never prophylactically.
- New pack: create the README (plus `AGENTS.md` only for real deltas) and add
  an index entry — areas go under **Ongoing**. Bind an external workspace
  only when code, media, data, or a separate toolchain need their own working
  tree.
- State changes: move the entry between the index groups (Active, Waiting /
  Blocked, Later, Ongoing); retire by moving the pack to `archive/` and its
  entry to Archived. Waiting and blocked stay live — never archive open
  handoffs. An area archives only when the responsibility itself ends — never
  for being quiet.
- Experiments end by conclusion, promotion to `projects/`, or archive; keep
  the original as origin evidence.
- Never create `WORKLOG.md`; only an explicitly invoked `$ultragoal` owns it.

## People

Search `people/` for an existing file before proposing a new one; never create
one because a name appeared once. The relationship decides the file, the
interaction decides the content: any durable relationship qualifies, but keep
only context that helps future collaboration — role, relationship, decisions,
current handoffs, project links — and never sensitive facts irrelevant to the
interaction. Propose the smallest diff to an existing file.

## References

Read `references/vault-model.md` when creating, promoting, completing, or
archiving work, when a destination is genuinely ambiguous, or when explaining
how the Manager and its tools (git, qmd, doctor) work. Read
`references/workspace-sync.md` after meaningful progress in a bound external
workspace. Read `references/maintenance.md` for Manager health, plugin update
checks, and qmd upkeep.
