---
last_edited: 2026-07-21
---

# wirenet: Foundations

wirenet's architecture was not derived from theory, but it lands squarely on
ground that three schools have already mapped: systems thinking (Meadows),
data-systems engineering (Kleppmann, Petrov), and knowledge graphs. Naming
that ground here lets design debates cite a principle instead of re-arguing
it from scratch. Nothing below adds mechanism; it says why the existing
mechanisms are shaped the way they are.

## Systems — Meadows

**Concepts.** Stocks and flows; balancing and reinforcing feedback loops;
the leverage ordering (rules and information flows beat parameter tuning);
system traps (drift to low performance, shifting the burden).

**Where it already lives.**
- The real stock is trust — a reader-agent's confidence that a pack is
  still true — not file count. Memory rot is its silent outflow.
- The update threshold and the approval gate are two valves in series on the
  inflow; together they keep the stock compact.
- The doctor's staleness check is the balancing loop: a thermostat on trust
  whose finding — review, archive, or reaffirm — is the system's only
  deliberate outflow.
- Certification-as-merge gives the Base's inflow a named valve-keeper: the
  entity owner.

**Rules.**
- The product sells trust, not files; judge every mechanism by its effect on
  the trust stock.
- Regulated inflow demands an outflow: archive proposals are first-class
  doctor findings, not housekeeping.
- Reach for rules and information flows (thresholds, doctor visibility, git
  history) before tuning parameters.
- Never optimize the proxy: "files look maintained" is not "future tasks
  understand."

## Data Systems — Kleppmann, Petrov

**Concepts.** Log/state duality; derived data as redundant and rebuildable,
never authoritative; asynchronous replication and honest staleness; conflicts
surfaced as siblings, not silently converged.

**Where it already lives.**
- Git history is the append-only log; the working tree is materialized state.
  Recovery is checkout, audit is log replay, and the approval gate sits at
  the write path — the correct place to gate a log.
- qmd is a materialized view: disposable, rebuilt by one command, and
  canonical Markdown wins over a stale index. Retrieval ends with a read of
  the file — read-repair against staleness.
- Safe push windows are deliberately bounded replication lag; a clone answers
  "as of last pull," never "now."
- Certification-as-merge keeps conflicting versions visible: the PR is the
  sibling-presentation UI, the owner is the resolver, and the Base doctor is
  the pre-merge constraint check.

**Rules.**
- Files are the sole system of record; every index or cache must be
  rebuildable from a clean checkout.
- Staleness is disclosed, never papered over: an answer from a clone or an
  index carries its as-of.
- Convergence is not correctness: overlapping semantic edits halt and
  surface; resolution is a reviewed write, never a storage-layer guess.
- Shared history is append-only; compaction requires an owner's sign-off.

## Knowledge Graphs & Ontologies

**Concepts.** The ontology cost curve (SKOS outlived OWL by dropping formal
semantics; schema.org won by refusing rigor; Shirky: links plus search
degrade gracefully where taxonomies shatter); the query layer, not the
ontology, is what practice retrofits; typed edges as convention, validation
as lint.

**Where it already lives.**
- Directory is kind, flat: the container is the type (ADR 004). Typing
  returns only in the Base, as four frontmatter keys a doctor actually
  enforces (ADR 003).
- Typed links are a `## Links` section with lightweight verbs — a lineage
  graph traversable by grep, no triple store.
- `GLOSSARY.md` is SKOS reduced to the part that survived contact with
  practice: one plain-English line per term.
- qmd is the retrofitted query layer — the move every vault community makes
  at scale — while prose stays the payload and search stays the reasoner.

**Rules.**
- The container is the type; routing facts never hide inside files.
- Lint for dangling targets, not "invalid" ones: any verb may connect any
  kinds.
- A schema exists only where a doctor enforces it; everything else is
  convention.
- One definition per term; the glossary's rigor stops at label and
  definition.

## Deliberately Informal

We refuse to formalize: class hierarchies and subtyping (where ontology
projects go to die); cardinality, domain, and range rules; reified edges
carrying confidence, provenance, or validity as fields — prose in the link
note suffices; status enums and IDs in the personal core; structured prose
bodies. Every refusal has one reason: formal semantics buy machine agreement
at the price of human agreement, and at personal and small-team scale the
humans are the bottleneck. A fifty-line lint buys most of what SHACL would.

The thresholds are re-examined when any one signal arrives — not at any
entity count: multiple writers with divergent vocabularies inside one Base;
a real need for interactive multi-hop queries, where grep loses; or an
external system consuming the graph, where formats beat conventions. Before
a threshold is crossed, added formality is speculation; after, refusing it
is debt. Stable Base ids — the one thing that cannot be retrofitted — are
already placed.

## Tensions — Dispositions (2026-07-21)

Raised by this document's first draft; each now has a home:

- Read-time failure had no mandated write path → resolved as the
  contradiction rule ([ADR 011](decisions/011-contradiction-rule.md)).
- Staleness clocks were calendar-fixed while rot scales with work velocity →
  resolved: areas carry a self-chosen review cadence
  ([ADR 007](decisions/007-areas-flexibility-model.md)).
- No north-star error metric → assigned: "pack consulted and contradicted per
  week" becomes the pilot success metric, tracked in the business workstream.
- Link verbs had no registry → committed: `VERBS.md` is a required component
  of the future base contract ([ADR 008](decisions/008-base-entity-model.md)).
- As-of provenance was disclosed but not stamped → assigned to the plugin
  scripts station: qmd sync records the commit it was built from.
