# ADR 004: Conventions Over Frontmatter in the Personal Core

Date: 2026-07-21 · Status: accepted

## Context

v0.2 required typed OKF frontmatter (`type`, `schema`, `status`, IDs) on every
knowledge document. The rulebook grew larger than the memory it governed, and
every tool touching the vault had to learn the vocabulary.

## Decision

The personal vault is prose governed by conventions: no required frontmatter
(`title`/`description` optional, unknown keys preserved), no IDs in documents,
lifecycle expressed by location plus index grouping, and the doctor validating
conventions instead of types. "Markdown as code" means **checked like code,
not typed like code**. Machine-readable typing returns only where machines
need it — the planned shared team layer (base catalog), not the personal core.

## Consequences

Any editor and any agent can work with the vault without wirenet-specific
knowledge. Determinism moves from generation to validation. The v0.2 → v0.5
migration strips frontmatter and IDs, dry-run-first, without touching personal
prose.
