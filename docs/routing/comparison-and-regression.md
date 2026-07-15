---
last_edited: 2026-07-15
---

# Routing Comparison And Regression Strategy

This comparison answers one question: where does WireNet preserve Jason Liu's
plain-file operating model, and where does it deliberately add or change a
contract?

Run the mechanical comparison with:

```sh
python3 scripts/compare_routing_contracts.py
python3 scripts/compare_routing_contracts.py --json
```

## Preserved

| Jason mechanism | WireNet v0.1 | Preservation rule |
| --- | --- | --- |
| Root and nearest `AGENTS.md` | Same | Markdown instructions remain the executable routing layer. |
| Root `README.md` | Same human role | It is not replaced by an index. |
| `projects/README.md` | Same collection-guide and active-packet role | WireNet keeps it and adds a separate OKF index. |
| Project `README.md` | Same canonical current-state role | It gains OKF metadata but remains full project prose. |
| Project `AGENTS.md` | Same local routing role | It is generated with the packet core. |
| `GOAL.md` | Same optional long-objective role | It remains optional and works with UltraGoal. |
| `RESULT.md` | Same optional completed-evidence role | It remains optional and works with UltraGoal. |
| Open project folders | Same extensibility | Agents may add useful documents instead of filling a fixed form. |
| `people/*.md` | Same durable collaborator role | WireNet keeps evidence and privacy boundaries. |
| `notes/` | Same durable-scratch role | WireNet adds a visible README and viewer projection. |
| `sources/` | Same retained-evidence role | WireNet adds a visible README and preserves read-only-by-default. |
| Repo-local skills as procedures | Same conceptual separation | WireNet packages generic Manager behavior globally instead of copying it into personal content. |
| Git-backed reviewable memory | Same | Manager Git remains local history in v0.1. |

## Changed

| Change | Why | Regression risk |
| --- | --- | --- |
| Plugin behavior is separate from personal Manager content | One updateable product can serve many users and external projects. | Bootstrap must never copy skills into Manager or overwrite personal content. |
| External workspaces are bound by stable project ID and local path | Media, code, and data stay in their proper working folders. | Portable packet files must never leak absolute paths. |
| Every Project Pack starts with `README.md` and `AGENTS.md` | A small stable core preserves Jason's open model while making local handoff reliable. | Generator, doctor, sync, and viewer must accept optional extensions without requiring empty documents. |
| Root and project collection `index.md` files are WireNet-required | Stable catalog entry points improve portability and agent navigation even though OKF makes them optional. | They must remain additive and never replace README or AGENTS routing. |
| Optional `log.md` adds a sparse time axis when useful | OKF history can improve portable handoff and later sync. | It must stay newest-first and semantic, never become mandatory activity logging. |
| Global managed core block triggers reconciliation outside Manager | Repo-local skill recall cannot update packets from arbitrary workspaces reliably. | The block must be idempotent, minimal, approval-gated, and independent from optional workspace routing. |
| `docs/`, `outputs/`, and `archive/` receive explicit policies | Jason's placeholders otherwise have no usable routing semantics. | Policies must stay open and must not turn working output into canonical knowledge. |
| Viewer adds an optional agent-instructions projection | Humans need inspectable content and developers need visible instruction inheritance without changing source files. | The viewer must render complete documents, derive nearest-parent AGENTS routing exactly, and exclude indexes, hidden bindings, and implementation files. |

## Added

- stable `manager_id` and `project_id` values;
- device-local `.wirenet/` metadata and path bindings;
- project and route classification;
- dry-run-first bootstrap, repair, doctor, and deterministic packet generator;
- a globally installable Manager, bootstrap, and sync skill set;
- OKF concept metadata, reserved index and log behavior, links, and graph view;
- a formal distinction between external implementation work and portable memory;
- machine-readable routing contracts and contract-delta tests.

## Removed From The Runtime

- Jason's repo-local `.codex/skills/` shelf is not copied into `~/Manager`.
  Generic Manager behavior lives in the installed plugin; domain skills remain
  separate plugins.
- The ambiguous option to treat `projects/<slug>` as both implementation folder
  and packet is removed. Manager holds the packet; the binding points to work.

The original `.codex/` and template trees remain in the product repository only
as inspectable downstream reference material while the migration is developed.

## Why OKF Indexes Do Not Destroy Jason's README Routing

Jason has two different README roles:

1. `projects/README.md` is created during onboarding as a collection router with
   a short explanation and active-packet links.
2. `projects/<slug>/README.md` is the canonical project document.

WireNet preserves both roles. It adds root `index.md` and
`projects/index.md` as reserved OKF navigation documents. The collection README
retains its explanation and active-packet links; the additive index provides a
minimal progressive-disclosure catalog. The packet README remains canonical
project state.

This is safe only while tests enforce all three facts:

- `projects/README.md` and `projects/index.md` both exist and receive relative
  packet links;
- every packet still contains its own complete `README.md`.

## OKF Scope Decision

The clean v0.1 interpretation is:

- `~/Manager` is the local content container and viewer root;
- each Project Pack is a self-contained portable synchronization unit;
- root `index.md` catalogs the Manager's content shelves;
- `projects/README.md` preserves collection guidance and `projects/index.md`
  additively catalogs those units;
- other typed Manager notes can participate in graph navigation;
- strict whole-tree OKF conformance is deferred until authoring and migration
  rules can guarantee metadata for every user-created Markdown file.

This avoids declaring the entire personal workspace a single indivisible bundle
while preserving the option to export a Project Pack, a shelf, or a curated
Manager subset to a future Knowledge Hub.

## Regression Suite

The routing tests must stay network-independent. The Jason contract is a frozen
snapshot; upstream review is a separate explicit fetch step.

The suite checks:

1. both contracts follow the same routing-contract schema and cite evidence;
2. Jason's snapshot and known ambiguities remain explicit;
3. WireNet's seed contains every declared runtime entry point;
4. Project Pack generation produces `README.md` and `AGENTS.md` with stable IDs
   and accepts optional typed concepts;
5. collection navigation updates both `projects/README.md` and
   `projects/index.md` without replacing packet READMEs;
6. root, collection, and project AGENTS files remain the routing hierarchy;
7. local bindings contain paths but no project prose or instructions;
8. the global core block supplies the cross-workspace trigger;
9. viewer link and derived AGENTS-routing behavior remain a projection, not a write path;
10. contract comparison makes added, removed, and changed entities visible.

When upstream changes, first run `scripts/compare_upstream.py --fetch`, inspect
the commits, and deliberately update the frozen Jason contract only when its
documented routing really changed.

## Open Design Questions

- Keep `docs/`, `outputs/`, and `archive/` policies narrow and revise them only
  with usage evidence; Jason's placeholders are not semantics by themselves.
- Revisit whether the WireNet-required root and projects indexes remain useful
  after real bootstrap and viewer use; OKF itself does not require them.
- Define the future Knowledge Hub merge model before claiming multi-device sync.
- Decide whether all new free-form notes must become typed OKF concepts or
  whether the consumer should continue tolerating untyped Markdown.
