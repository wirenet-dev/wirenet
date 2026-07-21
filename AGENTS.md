# wirenet Development Instructions

## Purpose

This repository develops and distributes the wirenet plugin — the Manager
for Claude Code and Codex. It is a product source tree, never a personal
Manager runtime: the seed lives under `plugins/wirenet/templates/manager/`
and is materialized elsewhere by `manager-setup`.

## Read Order

1. `docs/product.md` — what this is and why.
2. `docs/core-contract.md` — the governing behavior contract.
3. `docs/decisions/` — why it is built this way (ADRs; cite them in reviews).
4. The relevant skill, reference, template, script, and test.

## Conventions

- **Markdown as code, checked not typed** (ADR 004): prose is validated by
  `scripts/validate_markdown.py` and the tests; no required frontmatter in
  the personal core; schemas exist only where code enforces them (ADR 003,
  `contracts/`).
- **Naming**: `wirenet` lowercase is the product; `WireNet` is the company;
  the user's folder is "the Manager" (see `docs/product.md` § Naming).
- **Both platform manifests stay in sync** (`.claude-plugin/` and
  `.codex-plugin/` — CI enforces version and name equality).
- **Seed changes follow the contract**: any change under
  `templates/manager/` must be consistent with `docs/core-contract.md` and
  the skill references, and never seeds empty placeholder content.
- Repo-local dev skills live in `.agents/skills/` (Codex) and are symlinked
  from `.claude/skills/` (Claude Code): gh-commit, gh-fix-ci,
  gh-address-comments, audit-ai-code, yeet.

## Testing And Release

- `pytest -q` and `python3 scripts/validate_markdown.py .` must pass; CI
  runs both plus manifest checks on every PR.
- Release: bump the version in both plugin manifests, update
  `plugins/wirenet/RELEASE_NOTES.md` and `CHANGELOG.md`, tag `v<version>`;
  CI verifies the tag against the manifest and publishes the GitHub release.
  `stable` fast-forwards only after a successful release.

## Boundaries

- No personal Manager content, customer data, or secrets in this repository —
  including test fixtures.
- No hidden hooks, home-directory scans, or automatic memory writes in
  product code.
- Plugin updates never rewrite personal vault content; conventions arrive as
  proposed, approved migrations (see core contract, Compatibility Promise).
