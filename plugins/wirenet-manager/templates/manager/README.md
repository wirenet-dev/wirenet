---
type: "Manager Overview"
schema: "wirenet-manager/v0.2"
title: "WireNet Manager"
visibility: private
status: active
content_language: "en"
last_edited: 2026-07-15
---

# WireNet Manager

This is the human landing page for the user's local, durable work memory.
Knowledge-first projects may live entirely in this Manager. Code, media, large
data, and deliverable-heavy work stay in external workspaces; both variants use
the same portable Project Pack contract.

## Start Here

1. Open the [current stack](TODO.md).
2. Browse the [Project Pack catalog](projects/index.md).
3. Open only the relevant packet and follow its links selectively.
4. Read [user context](agent/USER_CONTEXT.md) only when the task needs it.

## Main Areas

- `agent/`: durable user and working-context notes.
- `people/`: evidence-backed collaborator notes.
- `projects/`: portable Project Packs with typed status and local agent routing.
- `notes/`: durable scratch notes without a better canonical home.
- `docs/`: optional structured documents without a stronger project, person,
  or source home; agents may organize it as useful.
- `sources/`: the Knowledge Shelf for curated evidence and source context.
- `experiments/`: bounded Experiment Packs that conclude, archive, or promote
  into linked Project Packs.
- `outputs/`: ignored, device-local working memory for generated intermediates;
  not canonical knowledge and not part of future sync by default.
- `archive/`: inactive material preserved for history.
- `.wirenet/`: device-local bindings and Manager metadata; never portable
  knowledge.

The shelves are routing defaults, not a fixed taxonomy. An index is created for
a shelf only once its real content benefits from a catalog.

## Project Pack Contract

Each Project Pack starts with two stable documents:

- `README.md`: current status, next move, owners, decisions, and blockers.
- `AGENTS.md`: read order, recurring sources, safety gates, and update rules.

The agent may add `GOAL.md`, `RESULT.md`, `log.md`, `index.md`, or other useful
concepts when the project needs them. Only an explicitly invoked UltraGoal may
create or update `WORKLOG.md`. Every non-reserved Markdown
document other than `AGENTS.md` is typed OKF knowledge. Project concepts share
the packet's stable `project_id`.

`WORKLOG.md` is detailed UltraGoal working state. Reserved `log.md` is a sparse
OKF chronology and should exist only when that time axis materially helps. They
must not duplicate one another.

Experiment Packs use the same two-file core with a stable `experiment_id`, but
stay lighter: `README.md` holds the question, bound, decision criterion, and
observation. Promotion preserves the experiment as origin evidence and creates
a linked Project Pack.

## Boundaries

- Absolute external project paths live only in `.wirenet/workspace-bindings.json`.
- Portable Project and Experiment Packs use stable packet IDs.
- Do not copy credentials, private source dumps, raw media, build output, or
  generated caches into the Manager.
- Keep actual `outputs/` content local and ignored. Link or distill anything
  durable into a Project Pack, `sources/`, or `notes/`.
- Product instructions, generation rules, and canonical templates live in the
  installed WireNet Manager plugin rather than being copied into this folder.
- Git is local history by default. No remote or cloud sync is configured by v0.2.
