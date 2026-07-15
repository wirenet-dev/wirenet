---
last_edited: 2026-07-15
---

# Testing Markdown As Code

WireNet Manager treats natural-language workspace behavior as a software
product. Markdown bodies carry human meaning and agent instructions; non-empty
`type` frontmatter is required for every non-reserved knowledge document;
standard Markdown links define knowledge-graph edges; folder placement and inherited
`AGENTS.md` files define a separate runtime-routing plane. Changes to those
surfaces can therefore be breaking changes even when no Python code changes.

The central product principle is **Metadata as Code**: identity, type,
relationships, routing, and lifecycle are explicit versioned interfaces rather
than hidden application state. **Knowledge as Code** is the broader result, and
**Markdown as Code** is the engineering discipline used to develop and verify
the natural-language parts of that system.

Google's OKF specification does not name this discipline "Markdown as Code."
It describes a minimal Markdown-and-YAML knowledge format that is human- and
agent-readable, portable, and diffable in version control, and explicitly
relates it to "metadata as code." WireNet adopts that principle directly and
extends its engineering consequences from knowledge representation to agent
behavior and routing.

## Contract Surfaces

Treat these as public interfaces:

1. folder and reserved-filename conventions;
2. frontmatter fields, stable IDs, and producer-defined extensions;
3. README and nearest-`AGENTS.md` read order;
4. collection indexes and Markdown links;
5. skill descriptions, shared references, and the global managed trigger;
6. dry-run, approval, and create-only safety gates;
7. bootstrap, repair, doctor, sync, and viewer producer-consumer boundaries.

Tests should assert stable semantics rather than incidental prose. Exact text is
appropriate only for managed markers, reserved headings, CLI errors, or a
sentence that intentionally acts as a routing contract.

## Test Layers

| Layer | Question | Primary checks |
| --- | --- | --- |
| Syntax | Can tools parse the product? | Markdown metadata, JSON, plugin and skill validation |
| Schema | Are required identities and reserved files valid? | OKF `type`, runtime sidecars, packet `project_id`, index and log shape |
| Routing | Does each durable concept have one canonical owner? | Frozen routing contracts, read/write routes, approval gates |
| Production | Do generators materialize the contract? | Bootstrap seed, open Project Pack core, optional concepts, canonical project index |
| Safety | Are previews and repair non-destructive? | Dry-run has no writes, repair is create-only, rejected routes leave no partial packet |
| Reconciliation | Does an external path resolve predictably? | Longest binding, experiment and ignored routes, untracked classification |
| Consumption | Can humans inspect the portable knowledge source? | Full concept rendering, typed nodes, real link edges, and complete exclusion of reserved, runtime, and hidden-state documents |
| Reference | Did WireNet accidentally erase a useful Jason behavior? | Frozen upstream contract and explicit semantic delta |

## Core Regression Invariants

- A fresh bootstrap contains exactly the seed entities declared by the routing
  contract, plus generated device-local Manager metadata.
- Bootstrap preview writes nothing; repair creates only missing scaffold and
  never overwrites personalized content.
- Project creation preview writes nothing. A rejected duplicate path, slug, or
  project ID leaves indexes, bindings, and packets unchanged.
- Every packet starts with typed `README.md` and runtime `AGENTS.md`; optional
  concepts require the packet schema and non-empty OKF `type`; the sidecar and
  concepts share one `project_id`.
- `projects/index.md` routes every active packet; no generic shelf README
  placeholder exists.
- Every in-scope Markdown file is either typed knowledge, reserved `index.md` or
  `log.md`, or runtime `AGENTS.md`; the Doctor rejects any other case.
- Reserved `log.md` files, when present, use newest-first ISO dates and remain
  free of concept frontmatter.
- Read-only routes have no canonical writes. Mutating routes declare preview or
  explicit-approval behavior.
- The global managed block recalls the sync skill only when it is installed and
  enabled; disabling the plugin does not block ordinary tasks.
- The viewer never becomes a source of truth and never exposes hidden bindings,
  runtime `AGENTS.md`, plugin implementation, or ignored outputs.
- Reserved indexes, logs, and runtime `AGENTS.md` never enter the generated
  WireNet Inspector payload.
- Every graph edge comes from a standard Markdown link between two typed
  concepts; no runtime, folder, packet, or inferred edge may be synthesized.

## Change Rule

When adding a shelf, document, skill, or route:

1. update the human contract;
2. update the machine-readable routing contract;
3. update its producer and consumer;
4. add or adjust a semantic regression test;
5. run the full validation suite before review.

Do not update a test merely to match an implementation change until the
contract change itself is deliberate and documented.
