---
last_edited: 2026-07-15
---

# Vault Bootstrap Correction Result

> Historical verification record for the upstream-derived root scaffold. The
> current WireNet Manager v0.1 product contract lives in
> `architecture-v0.1.md`.

## Reproduced Baseline

A disposable fresh setup followed by onboarding project and person creation
generated eight Markdown files. All eight lacked `last_edited`; the first
integration failure was the generated root `AGENTS.md` missing frontmatter.

The pre-change repository suite also rejected the correction proposal's valid
`2026-07-11` date because it required every Markdown file to retain the template
date `2026-06-15`.

## Implemented

- Added temporary-directory integration coverage for fresh, partial, repeated,
  project/person, router, metadata, doctor repair, Git clone, and migration-copy
  behavior.
- Added canonical project and person renderers and routed onboarding and
  standalone helpers through them.
- Made generated Markdown use ISO `last_edited` metadata and made project
  creation create or update the canonical router.
- Added create-only scaffold reconciliation, tracked `notes/` and `sources/`
  placeholders, and a read-only doctor with explicit `--repair` mode.
- Added a dry-run-first migration copy that refuses non-empty destinations,
  excludes caches, compiled Python, symlinks, Git internals, and known temporary
  handoffs, and emits JSON inventory and verification results.
- Replaced fixed-date validation with one repository validator used by tests and
  packaging CI.
- Updated onboarding instructions to run doctor for brand-new, partial, and
  established vaults.
- Documented WireNet external workspace roots and replaced the assumed global
  `wirenet status` command with the stable repository-local doctor command.
- Updated packaging CI to run pytest, validate source Markdown, extract the zip,
  bootstrap a disposable generated vault, validate its Markdown, and require a
  clean doctor result.

## Decisions

- Existing canonical files are preserved byte-for-byte by setup and scaffold
  repair; nonstandard project routers are reported instead of rewritten.
- Standalone person creation no longer offers a destructive force-overwrite path.
- Filesystem migration does not claim to verify external automations or thread
  handoffs. Its JSON result marks that check as manual.
- Migration remains copy-only into a new empty destination. In-place live-vault
  migration is outside this implementation and still requires explicit approval.

## Verification

- `python3 scripts/validate_markdown.py .` — passed.
- `pytest -q` — 8 passed.
- `ruff check ...` across touched Python and tests — passed.
- `git diff --check` — passed.
- Packaged zip extraction and tests — 8 passed.
- Fresh bootstrap from the extracted package — passed; doctor returned `ok: true`.

All bootstrap and migration fixtures were disposable temporary directories. The
live `/Users/gitt/Vault` was not used as a fixture or mutated.

## Approval-Gated Follow-Up

- Review the implementation diff and decide whether to checkpoint it.
- Do not commit, push, merge, publish, change global configuration, or migrate
  the live vault without Florian's explicit approval.
- Automation/thread handoff verification remains a manual migration checklist item.
