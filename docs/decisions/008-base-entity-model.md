# ADR 008: The Base Is a Git Repo of Typed Markdown Entities

Date: 2026-07-21 · Status: accepted (model decided; layer built later)

## Context

Organizations need a shared knowledge layer. Enterprise catalogs (Atlan,
Collibra, DataHub) solved ownership, certification, and lineage — under heavy
infrastructure. Glean solved assistant access — as a hosted service. wirenet
needs their substance on a git+Markdown, local-first footing (ADR 004 reserved
exactly this layer for the return of typing).

## Decision

The Base is a per-organization git repository of Markdown entity files: a
thin, typed index of what the org knows and who vouches for it, pointing at
canonical sources, never mirroring them. Directory = entity kind (starter set:
`systems/`, `guides/`, `decisions/`, `people/` — org-visible facts only —
plus `GLOSSARY.md`, one definition per term). Exactly four enforced
frontmatter keys: `id` (stable), `owner` (one accountable human), `status`
(`verified | draft | deprecated`), `reviewed` (date). Everything else is
prose plus conventions: typed links as a `## Links` section with verbs; a
verb registry (`VERBS.md`: verb, inverse, transitivity, one-line meaning) is
a required component of the layer, softly enforced — unknown verbs are
findings, not rejections. **Certification is a merge**: changes arrive as
PRs, the owner merges; setting `verified` plus today's `reviewed` date is the
certification act. **Capture is push-on-work**: the agent finishing work in an
org repo proposes the Base delta it just learned — no crawlers. Boundaries:
the Manager references entities and never copies them; the Base never reads a
Manager; one repo = one trust boundary (finer access = another repo); shared
projects carry their pack in the shared workspace — the Base is a knowledge
layer, not project coordination.

## Consequences

The approval-gate primitive scales to team size as PR review; no workflow
engine, no role matrices, no connector fleets. The schema lives in
`contracts/` because a Base doctor enforces it (ADR 003). Built later as
`base-contract.md` — after the v0.5 release, before the first team pilot.
