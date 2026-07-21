# ADR 012: The Vault Carries Its Own Operating System

Date: 2026-07-21 · Status: accepted

## Context

Close reading of the upstream template showed that its entire behavioral
system is an 86-line root `AGENTS.md` — no global skill, no machinery. Any
agent behaves correctly because nearest-instructions discovery is built into
the runtimes themselves. The model's only limits are distribution (you must
understand git to start), reach (it ends at the monorepo boundary), and
upkeep (conventions drift with nobody checking). Meanwhile wirenet's manager
skill had accumulated the behavioral core — routing table, thresholds,
lifecycle — inside the plugin, making the plugin quietly load-bearing.

## Decision

The vault carries its own operating system. The seed root `AGENTS.md` (one
page, upstream's register) holds the complete behavioral core: read order,
what-lives-where routing, the "does it end?" classification, update threshold,
replace-don't-append, derivability, the contradiction rule, approval gates.
The plugin delivers and maintains, never constitutes: setup creates the vault
and personalizes its instructions; the manager skill defers to the vault's
`AGENTS.md` and adds only reach (cross-workspace sync), retrieval, and upkeep
(doctor, updates); new conventions arrive as proposed, approved edits to the
vault's own instructions — never as plugin behavior the vault cannot see.
The same pattern governs future layers: every wirenet element (Base, Shelf)
is self-describing in its own repository.

## Consequences

A vault is fully operable by any agent with no wirenet software installed —
including tools that do not exist yet, and including the day WireNet itself
disappears. This is simultaneously the strongest trust argument the product
has and the completion of the degrade-gracefully principle. The manager
skill slims accordingly (behavior moves to the seed); the plugin's honest
value — delivery, reach, upkeep — becomes its stated role.
