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
| Root `README.md` | Same human role | It remains the landing page and becomes typed `Manager Overview`. |
| `projects/README.md` | Role preserved, file replaced | Collection navigation moves to `projects/index.md`; reusable rules move to runtime and plugin contracts. |
| Project `README.md` | Same canonical current-state role | It gains OKF metadata but remains full project prose. |
| Project `AGENTS.md` | Same local routing role | It is generated with the packet core. |
| `GOAL.md` | Same optional long-objective role | It remains optional and works with UltraGoal. |
| `RESULT.md` | Same optional completed-evidence role | It remains optional and works with UltraGoal. |
| Open project folders | Same extensibility | Agents may add useful documents instead of filling a fixed form. |
| `people/*.md` | Same durable collaborator role | WireNet keeps evidence and privacy boundaries. |
| `notes/` | Same durable-scratch role | WireNet types real content and avoids placeholder guides. |
| `sources/` | Same retained-evidence role | WireNet types real content and preserves read-only-by-default. |
| Repo-local skills as procedures | Same conceptual separation | WireNet packages generic Manager behavior globally instead of copying it into personal content. |
| Git-backed reviewable memory | Same | Manager Git remains local history in v0.1. |

## Changed

| Change | Why | Regression risk |
| --- | --- | --- |
| Plugin behavior is separate from personal Manager content | One updateable product can serve many users and external projects. | Bootstrap must never copy skills into Manager or overwrite personal content. |
| External workspaces are bound by stable project ID and local path | Media, code, and data stay in their proper working folders. | Portable packet files must never leak absolute paths. |
| Every Project Pack starts with `README.md` and `AGENTS.md` | A small stable core preserves Jason's open model while making local handoff reliable. | Generator, doctor, sync, and viewer must accept optional extensions without requiring empty documents. |
| Root and project collection `index.md` files are WireNet-required | Stable catalog entry points improve portability and agent navigation even though OKF makes them optional. | They must remain canonical navigation and never replace project README state or AGENTS routing. |
| Optional `log.md` adds a sparse time axis when useful | OKF history can improve portable handoff and later sync. | It must stay newest-first and semantic, never become mandatory activity logging. |
| Global managed core block triggers reconciliation outside Manager | Repo-local skill recall cannot update packets from arbitrary workspaces reliably. | The block must be idempotent, minimal, approval-gated, and independent from optional workspace routing. |
| `docs/`, `outputs/`, and `archive/` receive explicit policies | Jason's placeholders otherwise have no usable routing semantics. | Policies must stay open and must not turn working output into canonical knowledge. |
| Inspector exposes OKF concepts without support or runtime files | Humans need a faithful view of portable knowledge without inventing semantic or routing edges. | It must render complete concepts, use only Markdown-link edges, and exclude `index.md`, `log.md`, `AGENTS.md`, and hidden state from its payload. |
| Generic shelf README files are removed | Reusable rules belong to plugin/runtime; instance Markdown should be actual typed knowledge. | The Doctor must reject every untyped non-reserved in-scope Markdown file. |

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

The original scaffold is represented only by the fetch-only upstream remote and
the frozen Jason routing contract. It is not duplicated in the product tree.

## Why Replacing Shelf README Routing Is Safe

Jason has two useful README roles:

1. `projects/README.md` is created during onboarding as a collection router with
   a short explanation and active-packet links.
2. `projects/<slug>/README.md` is the canonical project document.

WireNet preserves the meaning but separates the concerns. The typed root
`README.md` remains the human Manager overview. Each typed packet `README.md`
remains canonical project state. `projects/index.md` becomes the single
collection catalog, while its creation and routing rules live in the installed
plugin and inherited `projects/AGENTS.md`.

This is safe only while tests enforce these facts:

- `projects/index.md` exists and receives every relative packet link;
- every packet still contains its own complete `README.md`.
- generic shelf README placeholders remain absent and the Doctor rejects any
  other untyped Markdown drift.

## OKF Scope Decision

The clean v0.1 interpretation is:

- `~/Manager` is one canonical OKF bundle plus a transparent runtime overlay;
- each Project Pack is a self-contained portable synchronization unit;
- root `index.md` catalogs the Manager's content shelves;
- `projects/index.md` catalogs those units while plugin and runtime rules govern
  creation;
- other typed Manager notes can participate in graph navigation;
- every other in-scope Markdown file is a typed concept by contract.

The full bundle remains portable while Project Packs, shelves, or curated
subgraphs can still be selected as future synchronization units.

## Regression Suite

The routing tests must stay network-independent. The Jason contract is frozen;
upstream review is a separate explicit fetch step.

The suite checks:

1. both contracts follow the same routing-contract schema and cite evidence;
2. Jason's provenance and known ambiguities remain explicit;
3. WireNet's seed contains every declared runtime entry point;
4. Project Pack generation produces `README.md` and `AGENTS.md` with stable IDs
   and accepts optional typed concepts;
5. collection navigation updates `projects/index.md` without replacing packet
   READMEs;
6. root, collection, and project AGENTS files remain the routing hierarchy;
7. local bindings contain paths but no project prose or instructions;
8. the global core block supplies the cross-workspace trigger;
9. the Inspector uses only typed OKF concepts and real Markdown-link edges;
   `index.md`, `log.md`, and `AGENTS.md` remain outside its generated payload;
10. the Doctor rejects untyped non-reserved Markdown anywhere in the in-scope
    knowledge tree;
11. contract comparison makes added, removed, and changed entities visible.

When upstream changes, first run `scripts/compare_upstream.py --fetch`, inspect
the commits, and deliberately update the frozen Jason contract only when its
documented routing really changed.

## Open Design Questions

- Keep `docs/`, `outputs/`, and `archive/` policies narrow and revise them only
  with usage evidence; Jason's placeholders are not semantics by themselves.
- Revisit whether the WireNet-required root and projects indexes remain useful
  after real bootstrap and viewer use; OKF itself does not require them.
- Define the future Knowledge Hub merge model before claiming multi-device sync.
