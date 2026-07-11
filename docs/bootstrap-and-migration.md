---
last_edited: 2026-07-11
---

# Vault Bootstrap And Migration

## Canonical Model

`projects/<project>/` is an Assistant workstream packet by default. Its
`README.md` carries durable state, owners, decisions, blockers, open loops, and
evidence. Its `AGENTS.md` carries recurring source routes and update rules.
Optional `GOAL.md` and `RESULT.md` files record durable outcomes and completed
verification. A packet may link to an external repository or workspace.

Project and person creation share the renderers in
`.codex/skills/onboarding/scripts/vault_model.py`. Both onboarding and standalone
helpers therefore emit the same schemas, and project creation cannot bypass the
project router.

## Bootstrap And Doctor

Use disposable directories while developing or testing:

```sh
scratch="$(mktemp -d)"
python3 .codex/skills/onboarding/scripts/setup_shared_memory_vault.py --vault-dir "$scratch"
python3 .codex/skills/onboarding/scripts/vault_doctor.py --vault-dir "$scratch"
```

Setup is create-only and idempotent. The doctor is read-only unless `--repair`
is supplied. Repair creates only missing scaffold and missing project-router
entries; it does not rewrite personalized canonical files or delete reported
caches and temporary handoffs.

The doctor reports missing scaffold, invalid Markdown metadata, missing router
entries, Python caches, known temporary migration handoffs, repository status,
and configured remotes. Use this stable repository command instead of assuming
a global `wirenet status` executable is installed.

## Conservative Migration Copy

Migration is dry-run by default and accepts only a different, absent or empty
destination:

```sh
python3 .codex/skills/onboarding/scripts/migrate_vault.py \
  --source /path/to/old-vault \
  --destination /path/to/disposable-copy
```

Review the JSON inventory, then opt in to the copy:

```sh
python3 .codex/skills/onboarding/scripts/migrate_vault.py \
  --source /path/to/old-vault \
  --destination /path/to/disposable-copy \
  --apply
```

The copy excludes Git internals, common Python/test caches, compiled Python
files, and known temporary migration handoffs. It then reconciles missing
canonical scaffold and emits a machine-readable doctor result and path-change
record. Automation and thread handoffs remain an explicit manual verification;
the local filesystem tool does not infer or mutate external automation state.

Do not target a live vault until the disposable copy passes review and the vault
owner explicitly approves the migration.

## Verification

```sh
python3 scripts/validate_markdown.py .
pytest -q
git diff --check
```

Packaging CI runs these checks, builds the zip, extracts it, bootstraps a fresh
temporary vault from the packaged scripts, and requires a clean doctor result.
