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
- `$wirenet-manager-bootstrap` seeds the matching folders and installs the
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

The shelves are defaults rather than a closed taxonomy:

| Destination | Use it for | Do not use it for |
| --- | --- | --- |
| `TODO.md` | Cross-project commitments, waiting items, and ordered next moves | Project detail or routine task logs |
| `agent/USER_CONTEXT.md` | Confirmed working style, responsibilities, and operating boundaries | Temporary mood or weak inference |
| `projects/<slug>/` | Portable state and context for a durable workstream | Implementation code, raw media, or a fixed form |
| `people/` | Evidence-backed context about recurring collaborators | Sensitive or irrelevant personal detail |
| `notes/` | Quick durable scratch knowledge without a better home | A second copy of canonical project state |
| `docs/` | Optional structured documents without a stronger project, person, or source home | Documentation already canonical in an external repo |
| `sources/` | Curated Knowledge Shelf: retained evidence, source notes, and linkable context | Large, private, or operational source trees |
| `experiments/` | Context for short-lived spikes or their classification | Durable projects that deserve a packet |
| `outputs/` | Ignored device-local working memory for generated intermediates | Canonical knowledge or synchronized artifacts |
| `archive/` | Inactive durable context that should remain reviewable | A dumping ground for unresolved active work |

## Open Project Packs

Every Project Pack begins with:

- `README.md`: current state and human handoff;
- `AGENTS.md`: local read order, recurring sources, safety, and routing.

The agent may create these conventions only when useful:

- `GOAL.md`: stable outcome and completion contract;
- `RESULT.md`: completed outcomes and verification;
- `WORKLOG.md`: detailed active UltraGoal attempts and next experiment;
- `log.md`: sparse OKF chronology for meaningful transitions;
- `index.md`: optional packet-local progressive disclosure when the packet grows;
- any other concept whose purpose is clearer than forcing it into a standard file.

All non-reserved portable concepts use OKF frontmatter with a descriptive
`type` and the packet's stable `project_id`. Reserved `index.md` and `log.md`
remain path-scoped. Preserve unknown frontmatter keys.

## Index And README

README files retain Jason Liu's human and agent routing roles. Never rename or
remove them merely to introduce OKF.

- Manager `index.md` provides the bundle-level catalog and declares OKF 0.1.
- `projects/README.md` remains the human and Jason-compatible collection guide.
- `projects/index.md` is the additive OKF catalog generated from packet state.
- A packet-local `index.md` is optional; the viewer may synthesize navigation.

## UltraGoal And OKF History

`WORKLOG.md` and `log.md` serve different resolutions:

- `WORKLOG.md` may contain detailed attempts, failures, evidence, and the next
  action while an UltraGoal is active.
- `log.md` contains only sparse, durable state transitions useful for navigation
  or synchronization.

Do not maintain both with the same information. A log entry may link to a
meaningful WORKLOG conclusion or RESULT, but it must not reproduce the worklog.
Neither file is required merely because a packet exists.

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
