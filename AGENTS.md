---
last_edited: 2026-07-15
---

# WireNet Manager Development Instructions

## Purpose

This repository develops and distributes the WireNet Manager plugin. It is not
the user's personal Manager runtime. The runtime seed lives under
`plugins/wirenet-manager/templates/manager/` and is materialized into a separate
folder only through the bootstrap flow.

## Read Order

1. `README.md`
2. `docs/architecture-v0.1.md`
3. `docs/project-pack-contract.md`
4. `plugins/wirenet-manager/.codex-plugin/plugin.json`
5. The relevant plugin skill, script, template, and tests
6. `docs/upstream-reference.md` when comparing Jason Liu's original model

## Product Boundaries

- The plugin owns reusable skills, deterministic behavior, schemas, and seed
  templates.
- A generated `~/Manager` owns personal content, local bindings, and local Git
  history. Do not copy plugin skills into it by default.
- External projects keep implementation code, media, and large data.
- Client or domain capability shelves remain separate plugins.
- Database sync and the Knowledge Hub are outside v0.1.

## Project Pack Contract

Generated Project Packs must contain `GOAL.md`, `README.md`, `RESULT.md`,
`AGENTS.md`, and the reserved OKF history file `log.md`. The four concept
documents share one stable `project_id`; `log.md` is scoped by the packet path
and carries no concept frontmatter. Portable files must not contain
machine-local paths; store those only in `.wirenet/project-bindings.json`.

## Skills And Plugins

- Use the current `.agents/plugins/marketplace.json` marketplace location.
- Keep the installable manifest at
  `plugins/wirenet-manager/.codex-plugin/plugin.json`.
- Keep each skill focused and validate it with the official skill validator.
- Keep detailed contracts in skill `references/` and deterministic repeated
  behavior in scripts.
- The root `.codex/` tree is retained as an upstream/downstream reference. Do
  not present it as the current distributed plugin structure.

## Upstream Reference

Jason Liu's `jxnl/personal-monorepo-template` is configured as fetch-only
`upstream`. Review upstream changes by intent with
`python3 scripts/compare_upstream.py --fetch`. Never blindly merge, rebase,
reset, or push to upstream.

## Development Safety

- Use disposable temporary directories for bootstrap and migration tests.
- Never bootstrap or migrate the live `/Users/gitt/Vault` or a live `~/Manager`
  during automated tests.
- Bootstrap and repair must be dry-run-first and create-only for existing
  folders.
- Do not configure remotes, cloud sync, customer workspaces, messages,
  automations, or shared documents without explicit approval.
- Do not commit secrets, credentials, raw private sources, or generated caches.

## Validation

Run before handoff:

```sh
python3 scripts/validate_markdown.py .
python3 /Users/gitt/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py \
  plugins/wirenet-manager
pytest -q
git diff --check
```
