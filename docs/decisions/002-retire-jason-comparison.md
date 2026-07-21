# ADR 002: Jason's Template Is Inspiration, Not a Tracked Upstream

Date: 2026-07-21 · Status: accepted

## Context

wirenet began as a deliberate downstream of `jxnl/personal-monorepo-template`
and maintained a frozen routing contract, comparison scripts, prose analyses,
and tests to audit behavioral drift against the original.

## Decision

Retire the comparison machinery: the frozen contracts, `compare_upstream.py`,
`compare_routing_contracts.py`, the `docs/routing/` analyses,
`docs/upstream-reference.md`, and their tests. Jason's ideas remain the
acknowledged inspiration; attribution stays (README note, LICENSE files in
adopted dev skills). From v0.5 the product evolves on its own terms.

## Consequences

Less meta-maintenance and no third artifact to keep in sync. We lose the
mechanical regression check against the original — accepted, because v0.5
deliberately diverges and the valuable upstream ideas are now encoded in the
core contract itself.
