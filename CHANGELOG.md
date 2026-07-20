---
last_edited: 2026-07-20
---

# Changelog

Installations track the `stable` branch. Each release is a tag; `stable`
fast-forwards to the latest released tag. `main` is the integration branch and
may be ahead of the released product.

## v0.4.1 — 2026-07-20

- Consolidated the product into the `wirenet` monorepo (renamed from
  `wirenet-manager` locally and on GitHub; old URLs redirect).
- Absorbed the Base and Shelf instance seeds as `templates/` from the retired
  `wirenet-base` and `wirenet-skills` repositories, brought the Base seed onto
  the strict OKF reserved-file rules.
- Added the lean `bin/wirenet` control plane (`status`, `doctor`).
- Added Claude Code support: `.claude-plugin/marketplace.json` plus per-plugin
  manifests, so `manager`, `workflows`, and `content-tools` install in Claude
  Code and Codex from the same repository and skill sources.
- Introduced the `stable` release channel and this changelog; install
  documentation now pins `--ref stable` instead of `main`.
- Added the onboarding acceptance matrix (`docs/acceptance-onboarding.md`).

## v0.4.0 — 2026-07-16

- wirenet Manager v0.2 workspace contract: OKF projection, Project and
  Experiment Packs, bindings, Doctor, upgrade migrations, QMD integration,
  Inspector, and frozen Jason-Liu routing contracts.
