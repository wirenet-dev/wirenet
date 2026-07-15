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
2. `docs/architecture-v0.2.md`
3. `docs/project-pack-contract.md`
4. `plugins/wirenet-manager/.codex-plugin/plugin.json`
5. The relevant plugin skill, script, template, and tests
6. `docs/upstream-reference.md` and `docs/routing/` when comparing Jason Liu's
   original model or changing routing semantics

## Metadata As Code

Treat metadata as a versioned product interface. Identity, type, links, routing,
and lifecycle must remain explicit, inspectable, diffable, and testable beside
the Markdown they describe. Do not move durable meaning into hidden application
state, and do not let structured metadata replace canonical human prose or
`AGENTS.md` instructions.

## Product Boundaries

- The plugin owns reusable skills, deterministic behavior, schemas, and seed
  templates.
- A generated `~/Manager` owns personal content, local bindings, and local Git
  history. Do not copy plugin skills into it by default.
- External projects keep implementation code, media, and large data.
- Client or domain capability shelves remain separate plugins.
- Database sync and the Knowledge Hub are outside v0.2.

## Project Pack Contract

Generated Project Packs must begin with `README.md` and `AGENTS.md`. Agents may
add `GOAL.md`, `RESULT.md`, reserved `index.md` or `log.md`, and other useful
concepts when the work earns them. Only an explicitly invoked UltraGoal may
create or update `WORKLOG.md`. Every concept in a packet shares
one stable `project_id` and has a descriptive OKF `type`; `AGENTS.md` shares the
ID as a `wirenet-runtime/v0.1` sidecar without `type`; reserved files are scoped
by their path and carry no concept frontmatter.
Portable files must not contain machine-local paths; store those only in
`.wirenet/workspace-bindings.json`.

Experiment Packs begin with the same two-file core, use a stable
`experiment_id`, and remain bounded by a question plus decision criterion.
Promotion creates a linked Project Pack and preserves the experiment as origin
evidence. Lifecycle status changes must follow
`plugins/wirenet-manager/contracts/lifecycle-v0.2.json`.

## Skills And Plugins

- Use the current `.agents/plugins/marketplace.json` marketplace location.
- Keep the installable manifest at
  `plugins/wirenet-manager/.codex-plugin/plugin.json`.
- Keep each skill focused and validate it with the official skill validator.
- Keep detailed contracts in skill `references/` and deterministic repeated
  behavior in scripts.

## Upstream Reference

Jason Liu's `jxnl/personal-monorepo-template` is configured as fetch-only
`upstream`. Review upstream changes by intent with
`python3 scripts/compare_upstream.py --fetch`. Never blindly merge, rebase,
reset, or push to upstream.

## Development Safety

- Use disposable temporary directories for bootstrap and repair tests.
- Never bootstrap or repair a live Manager workspace during automated tests.
- Bootstrap and repair must be dry-run-first and create-only for existing
  folders.
- Do not configure remotes, cloud sync, customer workspaces, messages,
  automations, or shared documents without explicit approval.
- Do not commit secrets, credentials, raw private sources, or generated caches.

## Validation

Run before handoff:

```sh
python3 scripts/validate_markdown.py .
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator/scripts/validate_plugin.py" \
  plugins/wirenet-manager
pytest -q
git diff --check
```
