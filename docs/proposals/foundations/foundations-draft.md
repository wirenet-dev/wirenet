
> **Status:** decided 2026-07-21 — see ADR 007–011; promoted to docs/foundations.md. Kept as provenance, no longer living.
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
- The real stock is trust — a reader-agent's confidence that a packet is
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

## Tensions Worth Revisiting

- Read-time failure has no mandated write path: an agent that finds a packet
  contradicted mid-task can quietly route around it, discarding the highest-
  signal error the system produces.
- Staleness clocks are calendar-fixed while rot scales with work velocity;
  per-pack cadence (proposal, open question 4) points the right way.
- No north-star error metric exists: "packet consulted and contradicted"
  per week would measure the goal rather than the proxy.
- Link verbs have no registry: one file declaring each verb, its inverse,
  and transitivity is nearly free now and expensive to reconstruct later.
- As-of provenance is disclosed but not stamped: qmd does not record the
  commit it was built from, so index staleness is suspected, not detectable.