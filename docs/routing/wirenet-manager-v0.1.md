---
last_edited: 2026-07-15
---

# WireNet Manager v0.1 Routing Contract

This document presents WireNet Manager in the same form as the frozen Jason Liu
reference. The matching machine-readable contract is
[`contracts/routing/wirenet-manager-v0.1.json`](../../contracts/routing/wirenet-manager-v0.1.json).

## System Boundary

WireNet separates behavior, personal memory, and implementation work:

```text
installed WireNet Manager plugin
├── skills/                    global behavior and triggers
├── scripts/                   deterministic producers and validators
└── templates/manager/         content-only bootstrap seed
               │
               ▼
~/Manager/
├── AGENTS.md                  Manager-local routing
├── index.md                   required WireNet bundle catalog
├── README.md                  typed Manager Overview
├── TODO.md                    ordered cross-project stack
├── agent/USER_CONTEXT.md      durable working context
├── projects/index.md          canonical OKF collection catalog
├── projects/<slug>/           portable Project Pack
├── people/, notes/, docs/, sources/
│                               supporting personal knowledge
├── experiments/, outputs/, archive/
└── .wirenet/                  device-local identity and paths
               │ project_id + local path
               ▼
external project workspace     code, media, data, operational files
```

The plugin is versioned and globally callable. The Manager contains content and
local Git history, not copied plugin skills. External project work remains
where the user already keeps it.

The product repository's `docs/`, `tests/`, contracts, marketplace metadata,
and development scripts verify or distribute the product. They are not copied
into the personal-memory routing graph unless they are part of the explicit
content seed.

## Entity Roles

| Entity | Canonical role | Created how | Routing authority |
| --- | --- | --- | --- |
| Root `AGENTS.md` | Manager read order, destinations, thresholds, safety; runtime sidecar outside OKF | Seed; repair only if missing | Yes, inside Manager |
| Root `index.md` | Required WireNet bundle catalog and OKF version declaration | Seed | Navigation |
| Root `README.md` | Typed Manager Overview and human landing page | Seed | Canonical instance overview |
| `TODO.md` | Ordered current stack | Seed and approved updates | State, not instructions |
| `agent/USER_CONTEXT.md` | Confirmed user and operating context | Seed and approved updates | Context, not instructions |
| `projects/index.md` | Canonical OKF active-packet catalog | Seed and packet generator | Navigation |
| `projects/AGENTS.md` | Runtime rules for the open packet core, identity, portability, and extensions | Seed | Yes, inherited for projects |
| Project `README.md` | Current operational handoff | Packet generator and sync | Canonical project state |
| Project `AGENTS.md` | Runtime sidecar for read order, sources, safety, and update rules | Packet generator and approved changes | Yes, inherited locally |
| Optional Project concept | Goal, result, worklog, decision, or another useful typed document | Agent when useful | Purpose-specific content |
| Optional Project `index.md` | Packet-local progressive disclosure once the packet grows | Agent or consumer when useful | Navigation |
| Optional Project `log.md` | Sparse meaningful chronology | Agent or sync when useful | History, not current state |
| `people/*.md` | Evidence-backed collaborator context | Approved Manager updates | Canonical relationship context |
| `notes/` | Durable scratch material without a better home | Seed and approved updates | Supporting content |
| `docs/` | Optional structured documents without a stronger canonical home | Seed and approved updates | Supporting content |
| `sources/` | Curated Knowledge Shelf, read-only by default and link-first | Seed and approved imports | Supporting evidence |
| `outputs/` | Ignored device-local working memory for generated intermediates | Seed and local writes | No portable authority |
| `archive/` | Inactive durable context preserved for history | Seed and approved archival moves | Supporting history |
| `.wirenet/project-bindings.json` | Project IDs, paths, classifications | Bootstrap and routing helpers | Device-local path resolution only |
| Global managed core block | Cross-workspace reconciliation trigger | Optional bootstrap step after approval | Yes, outside Manager |
| Installed plugin skills | Bootstrap, ongoing Manager, and sync behavior | Plugin install/update | Procedural authority globally |
| Installed plugin seed | Canonical bootstrap and repair scaffold | Plugin install/update | Creation input |

## Agent Routing

```text
task begins anywhere
        │
        ▼
global AGENTS.md managed core block
        │
        ├── no durable transition ───────────────▶ no Manager write
        │
        └── meaningful transition or handoff
                    │
                    ▼
          $wirenet-manager-sync
                    │
             inspect local binding
        ┌───────────┼────────────┬────────────┐
        ▼           ▼            ▼            ▼
     tracked     untracked   experiment    ignored
        │           │            │            │
        │       ask once      stay quiet    stay quiet
        ▼
 project AGENTS.md determines read order and destinations
        │
        ├── README.md  current state and next move
        ├── AGENTS.md  local routing and safety
        ├── concepts   optional goal/result/worklog/decision/etc.
        └── log.md     optional sparse meaningful transition
```

`AGENTS.md` remains the executable routing layer under the separate
`wirenet-runtime/v0.1` schema. It deliberately has no OKF `type`. OKF metadata
describes and links knowledge documents for portable consumers; it does not
carry behavioral instructions.

## Project Creation

An approved external workspace classified as a project creates an open packet:

```text
projects/<slug>/
├── README.md
└── AGENTS.md
```

Agents add `GOAL.md`, `RESULT.md`, `WORKLOG.md`, a packet-local `index.md`,
reserved `log.md`, or other typed concepts only when they make the handoff
clearer. Every concept and the `AGENTS.md` runtime sidecar share the packet's
stable `project_id`; reserved files are scoped by directory and have no concept frontmatter. The
generator adds the packet to `projects/index.md`, then writes the absolute
external path only to the device-local binding registry.

## Supporting Shelves

- `notes/` preserves Jason's durable-scratch semantics.
- `docs/` remains an open shelf for structured documents without a stronger
  canonical home; no fixed taxonomy is imposed.
- `sources/` becomes the curated Knowledge Shelf: retained evidence,
  read-only by default, and link-first rather than a copy of large source trees.
- `outputs/` becomes ignored device-local working memory for generated
  intermediates, not canonical or synchronized knowledge.
- `archive/` receives an explicit retention policy: preserve inactive durable
  context instead of deleting it.
- `experiments/` becomes primarily a classification policy for external spikes;
  v0.1 does not copy experiment work into Manager.

These are WireNet policies, not retroactive claims about Jason's intent.
Their reusable explanations live in the plugin and runtime `AGENTS.md`, not in
generic shelf README placeholders. A shelf receives `index.md` only after real
content benefits from progressive disclosure.

## OKF Overlay

Google's OKF v0.1 defines a bundle as a directory tree of Markdown concepts,
with `index.md` for optional progressive disclosure, `log.md` for optional
history, YAML `type` metadata on concept documents, and Markdown links for graph
relationships.

WireNet makes the Manager the canonical OKF bundle with a transparent runtime
overlay:

1. Every in-scope non-reserved Markdown file requires non-empty `type`
   frontmatter; the Doctor rejects untyped drift.
2. `AGENTS.md`, ignored outputs, plugin implementation, and device-local state
   remain outside the projection.
3. Concept frontmatter adds stable type, project identity, and producer fields.
4. Root `index.md` and `projects/index.md` are required by the WireNet profile
   as stable entry points, although OKF itself makes indexes optional.
5. Packet-local indexes and all `log.md` files remain optional reserved
   supporting documents, not concepts.
6. Standard Markdown links between concepts create the only graph relationships.
7. Viewer, future export, and future sync consumers share this one projection.

Project Packs are the intended first synchronization units, but the complete
typed Manager knowledge tree is one OKF bundle. The runtime overlay remains
local and inspectable without being synchronized as knowledge.

## Memory Update Strategy

WireNet keeps Jason's durable-meaning threshold and makes it deterministic:

- the global core block is the cross-workspace trigger;
- bindings classify the current local path;
- the sync skill routes the smallest durable change to one canonical document;
- a log entry is added only when sparse chronology adds independent value;
- inferred writes are previewed and approval-gated;
- recurring reconciliation catches missed handoffs without becoming a watcher.

The viewer is a read-only human projection and never becomes another source of
truth.
