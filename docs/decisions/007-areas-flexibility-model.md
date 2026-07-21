# ADR 007: The Flexibility Model — areas/ and the "Does It End?" Test

Date: 2026-07-21 · Status: accepted

## Context

Not everything is a project, an experiment, or a workflow. The strain was live
in the first real vault: a "Personal Finance" pack that can never complete, and
recurring client upkeep (invoicing) squatting inside a delivery project's pack.
Every container system that survived contact with real life (PARA, GTD,
org-mode) grew an explicit home for ongoing responsibility without an end date.

## Decision

Add exactly one container: `areas/<slug>/`, lazily created, for
responsibilities with a standard to maintain but no end. Classification is one
decidable question — "Does it end?" — and `projects/` admission tightens to
require a nameable completion state (prose, no field). `projects/index.md`
stays the only catalog and gains an **Ongoing** group. `TODO.md` gains a final
`## Someday` section (Later = committed but not now; Someday = not committed).
`people/` widens from work-relevant to durable relationships — the
relationship decides the file, the interaction decides the content; evidence
and privacy rules stay strict and unchanged. The doctor proposes — never
performs — project→area reclassification; declined proposals are remembered.
Refinements: an area starts as a single README (`routines/` and `reference/`
are lazy conventions); areas archive only when the responsibility itself ends,
never for being quiet; staleness measures areas against their self-chosen
review cadence; the agent proposes new areas only when recurring upkeep has no
home.

## Consequences

Zero new frontmatter — the container stays the type (ADR 004 strengthened).
Zombie packs end by construction; `archive/` stays meaningful; staleness
heuristics gain their discriminating power (an idle active project is a
finding, an idle area is normal). Rejected alternatives: typing areas via
frontmatter (hides the most routing-relevant fact inside files) and a full
lifecycle-typed root (high ceremony, breaks every link).
