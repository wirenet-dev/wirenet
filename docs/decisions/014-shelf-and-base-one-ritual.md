# ADR 014: Shelf And Base — One Ritual, Two Channels

Date: 2026-07-21 · Status: accepted (design; layers built later)

## Context

ADR 008/009 decided the Base (typed knowledge, certification-as-merge,
clone-first) and placed the Shelf beside it with a shared certification
model. The combination needed its working design — and the first client
team's real need arrives skills-first (working client skills already exist
and want distribution).

## Decision

- **Division — claim vs. recipe.** A claim can be true or stale → Base. A
  recipe can work or break → Shelf. Base `guides/` graduate to Shelf skills
  when they become mechanical enough for an agent to execute: knowledge
  hardens into capability.
- **One governance ritual.** Both are org git repositories with `owner`,
  `draft/verified/deprecated`, and certification as the owner's merge — the
  team learns one ritual for knowledge and capability alike.
- **Kernel-native channels per content type.** Knowledge is *pulled* (clone
  + a qmd collection); capability is *installed* (marketplace). The Shelf is
  an org marketplace repository using the existing plugin standards — no new
  format; only the Base needed its own spec (ADR 010).
- **Coupling.** The verb pair `automates` / `automated-by` links skills to
  the entities and guides they implement — the org's capability lineage,
  grep-traversable. The contradiction rule spans both repos: an agent whose
  skill run contradicts a Base entity proposes deltas to each.
- **Push-on-work covers both.** Finished work may yield a knowledge delta
  and a recipe delta under the same update threshold.
- **Team onboarding is three moves.** Clone the Base (know what we know),
  add the Shelf (do what we do), keep your Manager (yours, connected by
  reference, never by copy).

## Consequences

Zero new infrastructure — the marketplace pattern is already proven by this
product repository. Sequencing freedom: the Shelf may precede the Base where
a team's first need is distributing working skills; the first pilot points
that way. Detailed contracts land in `base-contract.md` when the layer is
built.
