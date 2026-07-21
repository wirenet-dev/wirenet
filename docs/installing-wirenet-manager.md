---
last_edited: 2026-07-21
---

# Installing wirenet

The canonical install flows live in the repository [README](../README.md) —
it is written so an agent shown that page can walk the entire path (add
marketplace, install plugin, fresh session, first meeting). This page adds
the operational detail around them.

## Distribution

wirenet is distributed through the plugin marketplaces of Claude Code and
Codex from `wirenet-dev/wirenet`. Users never clone this repository and need
no git, GitHub account, or terminal skills. Installations track the
`stable` ref; releases are tags that `stable` fast-forwards to.

## After Installing

Newly installed plugins load in fresh sessions only — restart the app or
start a new session, then say "Set up my Manager." The `manager-setup`
skill runs the first meeting: it materializes the seed to `~/Manager`
(never overwriting existing content), interviews the user, and offers
global wiring, bindings, qmd registration, and continuity — each with its
own approval. See the skill and its references for the exact choreography.

## Updating

The `manager` skill performs a bounded release check on request and shows
at most three release-note bullets with the exact update command. A plugin
update never touches personal Manager content; convention changes arrive as
proposed, approved migrations (core contract, Compatibility Promise).

## Operator Notes

`bin/wirenet` (status, doctor, `init base|shelf`) is for people working
with this repository or operating installations — customers never need it.
See [managed-installations.md](managed-installations.md).
