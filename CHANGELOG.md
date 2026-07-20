---
last_edited: 2026-07-20
---

# Changelog

Installations track the `stable` branch. Each release is a tag; `stable`
fast-forwards to the latest released tag. `main` is the integration branch and
may be ahead of the released product.

## v0.4.4 — 2026-07-20

- Fixed multiline GitHub Release bullets so Manager presents complete concise
  notes instead of cutting them off at Markdown line wraps.
- Re-ran the real installed-plugin update path against the public Release API.

## v0.4.3 — 2026-07-20

- Added a read-only stable-release check to Manager Doctor. It compares the
  installed manifest version with the latest GitHub Release and returns a short
  user-facing note plus the single Codex Marketplace update command.
- Manager check-ins now surface an available update and ask before refreshing
  the Marketplace; no plugin update mutates the personal Manager workspace.
- `$manager-setup` now closes an update with the installed version, packaged
  release notes, workspace-migration result, and final Doctor status.
- Defined `plugin_version` in workspace metadata as the plugin version that
  created or last structurally migrated the workspace. Runtime update checks
  read the installed plugin manifest instead of treating workspace metadata as
  the active version.

## v0.4.2 — 2026-07-20

- Manager skill: current-stack and day-planning answers now combine the
  Manager with a fresh, bounded, approved calendar window (30-minute reuse
  rule, explicit "not checked" statement, no shadow-calendar copies), and the
  same discipline applies to other approved live sources.
- Onboarding: first meeting offers a one-time translation of the seeded
  README/TODO bodies when the content language is not English.
- Added the first-bootstrap demo runbook (docs/demo-runbook.md).

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
