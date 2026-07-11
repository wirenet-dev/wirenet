---
last_edited: 2026-07-11
---

# Vault Bootstrap Correction Proposal

## Objective

Make a freshly bootstrapped, partially onboarded, cloned, or migrated WireNet
vault converge on the same explicit shared-memory structure without relying on
one agent to infer and manually reconcile overlapping generators.

This proposal preserves Jason Liu's upstream template as the conceptual base
while making WireNet's external-workspace architecture and bootstrap invariants
explicit and testable.

## Evidence From The Live Vault

The live `/Users/gitt/Vault` retained every path tracked by upstream, but it was
missing the generated shared-memory scaffold:

- `TODO.md`;
- `agent/USER_CONTEXT.md`;
- `projects/README.md`;
- `projects/AGENTS.md`;
- `notes/`;
- `sources/`.

Its first commit copied the upstream tracked tree. The next setup pass manually
created project packets and people notes without first running the shared-memory
setup script. A later workspace migration preserved that partial state and told
the replacement Assistant task to treat onboarding as established or partial,
so the missing bootstrap step was not revisited.

Additional live-vault drift included:

- a temporary migration handoff left after its completion condition;
- copied Python bytecode retaining a pre-migration absolute path;
- a generated `write-like-me` skill and style profile missing required metadata;
- stale monitor-routing context after PAULUS received its own project manager;
- no `wirenet` command available on `PATH` for the migration's suggested status check.

## General Bootstrap Defects

### Competing project and person generators

The repository currently has two project creation paths:

- `.codex/skills/new-project/scripts/new_project.py` creates a template-based
  `README.md` and optional `AGENTS.md`, but does not require or update
  `projects/README.md`;
- `.codex/skills/onboarding/scripts/new_project_note.py` creates a different
  packet schema and requires the project router.

The same duplication exists for person notes. The two paths produce different
frontmatter, headings, routing behavior, and discoverability.

### Generated output violates repository validation

The shared-memory setup, project-packet, and person-note generators omit
`last_edited`, while the test suite and packaging workflow require it on every
Markdown file. A clean integration run currently produces eight invalid files.

The unit test also pins template Markdown dates to `2026-06-15`, which makes
normal live-vault maintenance fail as soon as a user updates `last_edited`.
Its hand-written parser rejects valid nested YAML. The packaging workflow uses
a different, weaker validator and does not run `pytest`.

### Partial-state detection is too coarse

Onboarding classifies a vault as established when useful context exists, but it
does not run an invariant check for the canonical scaffold. The setup script is
idempotent, yet the onboarding flow does not require a dry-run or doctor pass
for partial and established vaults.

### Empty shelves do not survive Git

`notes/` and `sources/` are created as empty directories. They disappear when a
live vault is cloned or migrated through Git unless setup runs again.

### WireNet workspace policy is implicit

Upstream calls `projects/` active or long-lived work, while the Assistant setup
calls its contents rolling workstream packets. WireNet additionally keeps code,
domain work, and data in `/Users/gitt/Projects`, `/Users/gitt/Developer`,
`/Users/gitt/Documents`, and `/Users/gitt/Data`. That external-workspace policy
currently lives outside this template and can be lost during bootstrap.

## Proposed Corrections

### 1. Define one canonical vault model

- State in the WireNet template README and root `AGENTS.md` that
  `projects/<project>/` is an Assistant workstream packet by default.
- Allow a packet to point to an external repository or workspace; do not claim
  upstream universally forbids code inside the monorepo.
- Document the WireNet workspace roots and their intended promotion rules.
- Keep the packet contract explicit:
  - `README.md`: durable state, owners, decisions, blockers, open loops, evidence;
  - `AGENTS.md`: recurring source routes and update-routing instructions;
  - optional `GOAL.md`: stable long-running outcome contract;
  - optional `RESULT.md`: completed milestone and verification evidence.

### 2. Unify generators

- Create one shared packet renderer and one shared person-note renderer.
- Make both the onboarding helpers and the standalone `new-project` /
  `new-person` skills call those renderers.
- Make project creation always verify and update `projects/README.md`.
- Use one frontmatter schema and one set of headings for each artifact type.
- Preserve compatibility for existing packets; update rather than duplicate.

### 3. Add a vault doctor and migration mode

- Add a read-only doctor that checks required files, router entries, metadata,
  stale temporary handoffs, ignored caches, repository roots, and configured remotes.
- Run the doctor during brand-new, partial, and established onboarding states.
- Add an explicit migration mode that:
  - inventories before writing;
  - runs canonical scaffold reconciliation;
  - clears generated caches without copying them;
  - records path changes;
  - checks automation/thread handoffs;
  - verifies and removes temporary migration files;
  - emits a machine-readable result.
- Make `wirenet status` availability explicit: install it, invoke it through a
  stable repository script, or remove it from migration instructions.

### 4. Make generated Markdown valid

- Add ISO `last_edited` values to every generated Markdown artifact.
- Ensure generated skills and their reference profiles follow their supplied templates.
- Replace the fixed-date unit assertions with ISO-date validation.
- Parse frontmatter as YAML or deliberately inspect only top-level keys while
  allowing nested mappings and lists.
- Decide whether skill frontmatter permits additional platform fields; test the
  chosen contract consistently.

### 5. Make the generated vault the tested product

- Run `pytest` in the package workflow.
- Add temporary-directory integration tests for:
  - fresh shared-memory setup;
  - setup over a partial existing vault;
  - idempotent repeat setup;
  - project and person creation after setup;
  - project-router updates;
  - metadata validation of every generated Markdown file;
  - a clone/migration simulation that proves tracked shelves survive.
- Validate the packaged zip by bootstrapping a vault from it, not only by
  validating the template source tree.

### 6. Preserve empty canonical shelves

- Track `.gitkeep` files or small documented READMEs in `notes/` and `sources/`,
  or make the doctor recreate them and clearly treat them as runtime scaffold.
- Prefer tracked placeholders for WireNet so independent Git clones converge
  before onboarding runs.

## Suggested Implementation Order

1. Add failing integration tests that reproduce the eight invalid generated files.
2. Define and test the canonical packet and person schemas.
3. Extract shared renderers and route all four generators through them.
4. Add doctor and partial-state reconciliation.
5. Add WireNet workspace-root configuration and migration checks.
6. Update README, AGENTS, onboarding references, templates, and packaging CI.
7. Bootstrap a temporary vault from the packaged artifact and run the complete suite.
8. Test a migration copy of `/Users/gitt/Vault` before changing the live vault again.

## Acceptance Criteria

- A fresh bootstrap creates the full canonical scaffold and passes all tests.
- A partial vault converges without overwriting personalized canonical files.
- Re-running setup is idempotent.
- Every generated Markdown artifact passes the same validator used by CI.
- Project and person creation cannot bypass their canonical indexes or schemas.
- Empty canonical shelves survive a normal Git clone or are deterministically recreated.
- WireNet workspace roots and linked implementation repositories remain explicit.
- Migration leaves no stale handoff, cache path, automation duplication, or
  unresolved path reference.
- The live vault can be audited against the template with a single documented command.

## Non-Goals

- Do not absorb implementation repositories, private source archives, Base, or
  Skills into the vault.
- Do not rewrite existing live packets merely for stylistic uniformity.
- Do not add orchestration beyond the failures demonstrated by bootstrap and migration.
