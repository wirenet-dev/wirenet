---
last_edited: 2026-07-15
---

# Manager Content Routing

This is the shared content contract for `$wirenet-manager` and
`$wirenet-manager-sync`. It helps the agent maintain the Manager without
requiring the user to understand its folders.

## Skill Ownership

- `$wirenet-manager` uses this contract for orientation and writes made inside
  the Manager.
- `$wirenet-manager-sync` uses it for durable handoffs from external workspaces.
- `$wirenet-manager-bootstrap` materializes the matching shelves and installs the
  minimal managed global `AGENTS.md` trigger after approval.

Keep this shared reference instead of creating a separate routing skill. The
managed global block supplies reliable recall; the skills hold the procedure;
the local Manager documents remain inspectable content and inherited rules.

## Principle

Preserve durable meaning, not activity. Prefer the clearest existing canonical
home, link instead of duplicating, and let the structure grow when a new concept
earns a distinct purpose.

Apply **Metadata as Code**: keep durable identity, type, relationships, routing,
and lifecycle explicit beside the content, preserve unknown producer metadata,
and make inferred changes reviewable. Do not hide canonical meaning in chat,
bindings, or application state, and do not let metadata replace readable prose
or inherited `AGENTS.md` instructions.

The shelves are defaults rather than a closed taxonomy. Their reusable meaning
lives here and in the runtime `AGENTS.md`; do not copy generic explanatory
README files into an instance.

| Destination | Use it for | Do not use it for |
| --- | --- | --- |
| `TODO.md` | Cross-project commitments, waiting items, and ordered next moves | Project detail or routine task logs |
| `agent/USER_CONTEXT.md` | Confirmed working style, responsibilities, and operating boundaries | Temporary mood or weak inference |
| `projects/<slug>/` | Portable state for a durable Manager-native or externally bound workstream | Implementation code, raw media, or a fixed form |
| `people/` | Evidence-backed context about recurring collaborators | Sensitive or irrelevant personal detail |
| `notes/` | Quick durable scratch knowledge without a better home | A second copy of canonical project state |
| `docs/` | Optional structured documents without a stronger project, person, or source home | Documentation already canonical in an external repo |
| `sources/` | Curated Knowledge Shelf: retained evidence, source notes, and linkable context | Large, private, or operational source trees |
| `experiments/<slug>/` | Lightweight context for a bounded spike with a question and decision criterion | Durable multi-session work that should be promoted |
| `outputs/` | Ignored device-local working memory for generated intermediates | Canonical knowledge or synchronized artifacts |
| `archive/` | Inactive durable context that should remain reviewable | A dumping ground for unresolved active work |

## File-World Heuristic

Treat this as a gentle judgment call, not a rigid classifier:

- A few transient review files may stay together under `outputs/<task-slug>/`.
- When files begin to need recurring editing, durable delivery, their own
  toolchain, or a reusable body of work, suggest a separate external workspace
  and connect it to a Project Pack.
- Short-lived work is not automatically an experiment. Use an Experiment Pack
  when a bounded question and decision criterion matter.
- Do not interrupt useful work merely to reorganize it. Suggest a move when the
  files have started to earn their own home.

## Open Project Packs

Every Project Pack begins with:

- `README.md`: current state and human handoff;
- `AGENTS.md`: local read order, recurring sources, safety, and routing.

The agent may create these conventions only when useful:

- `GOAL.md`: stable outcome and completion contract;
- `RESULT.md`: completed outcomes and verification;
- `WORKLOG.md`: detailed active UltraGoal attempts and next experiment; only an
  explicitly invoked UltraGoal may create or update it;
- `log.md`: sparse OKF chronology for meaningful transitions;
- `index.md`: optional packet-local progressive disclosure when the packet grows;
- any other concept whose purpose is clearer than forcing it into a standard file.

All non-reserved portable concepts use OKF frontmatter with a descriptive
`type` and the packet's stable `project_id`. Reserved `index.md` and `log.md`
remain path-scoped. Preserve unknown frontmatter keys.

## Index And README

WireNet keeps only README files that carry instance knowledge:

- Root `README.md` is a typed `Manager Overview` and the human landing page for
  this Manager instance.
- A Project Pack `README.md` is typed `Project Status` and remains its compact
  operational handoff.
- Generic shelf explanations and product manuals belong to the plugin and
  runtime instructions, not untyped README placeholders.

Manager `index.md` declares OKF 0.1 and catalogs the bundle.
`projects/index.md` is the canonical lifecycle-aware Project Pack catalog.
`experiments/index.md` is created with the first real Experiment Pack. Other
shelf or packet indexes are created only when real content benefits from
progressive disclosure. Reserved indexes and logs support agents and future
sync, but do not enter the WireNet Inspector payload.

## Canonical Markdown Boundary

- `AGENTS.md` is runtime, uses `wirenet-runtime/v0.1`, and never declares a
  concept `type`.
- `index.md` and `log.md` are reserved OKF support documents and never declare
  a concept `type`.
- Every other Markdown document in an in-scope Manager shelf is a typed OKF
  concept. The Doctor treats an untyped document as invalid rather than silently
  maintaining a compatibility exception.
- `outputs/`, hidden local state, and plugin implementation are outside the
  portable projection.

## UltraGoal And OKF History

`WORKLOG.md` and `log.md` serve different resolutions and have different owners:

- `WORKLOG.md` may contain detailed attempts, failures, evidence, and the next
  action only while an explicitly activated UltraGoal owns the loop. It uses
  `type: "Goal Worklog"` and `producer: "ultragoal"`.
- `log.md` contains only sparse, durable state transitions useful for navigation
  or synchronization.

Do not maintain both with the same information. A log entry may link to a
meaningful WORKLOG conclusion or RESULT, but it must not reproduce the worklog.
Neither file is required merely because a packet exists. A normal Manager or
Sync update must never create a WORKLOG.

## Project And Experiment Lifecycle

- Project: `active`, `waiting`, `blocked`, `completed`, or `archived`.
- Experiment: `active`, `concluded`, `promoted`, or `archived`.
- Archive a project only when no open next move or waiting handoff remains and
  durable results have been retained.
- Promote an experiment when it becomes a durable multi-session workstream.
  Preserve the experiment as origin evidence and transfer its local bindings.
- Use the plugin lifecycle contract and transition helpers for mechanics;
  semantic readiness remains an agent judgment.

## Decision Heuristic

Before writing, ask internally:

1. Would a future task otherwise misunderstand durable meaning?
2. Does an existing canonical document already own it?
3. Is this project state, a person, a source, a general note, a structured doc,
   local working output, or inactive history?
4. Should the content be portable? If yes, use an OKF concept and stable links.
5. Is the evidence raw, private, large, generated, or transient? If yes, keep it
   external or in ignored `outputs/` and store only a link or synthesis.

Preview inferred durable writes and obtain approval unless the user already
approved that exact update.
