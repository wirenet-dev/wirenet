---
last_edited: 2026-07-21
---

# wirenet Manager v0.5 Core Contract

Status: governing contract for v0.5, implemented on branch `v0.5-core`.
This document defines the product core and what moves into optional layers.
Migration mechanics are out of scope here and become their own dry-run-first
release step. The product essence and its reasoning live in
[`product.md`](product.md); individual decisions are recorded in
[`decisions/`](decisions/).

## Product Statement

The core product is four things:

1. **A folder** (`~/Manager`): plain Markdown, git-versioned, readable and
   editable by the user, structured by Jason Liu's proven filename conventions.
2. **One skill** (`$manager`): read order, update threshold, approval gate,
   lifecycle — one page plus three references (vault model, workspace sync,
   maintenance).
3. **Retrieval** (`qmd`): a derived search layer over the folder, configured at
   onboarding, never a hard dependency.
4. **Onboarding** (`$manager-setup`): an interview that builds the first
   vault and installs the global wiring, so the user never learns the
   structure — they experience it.

Everything else — typed knowledge projection, Inspector, Base/Shelf sync,
client runtime, control plane — is an optional layer on top of a stable core,
opened only on real demand.

## Design Principles

- **Agent-maintained, human-auditable.** The user talks; the agent routes and
  writes after approval. No workflow may require the user to know a folder
  name, a frontmatter key, or a reserved word.
- **Conventions over schemas.** The doctor validates conventions; documents do
  not carry schema declarations. Value ships as behavior, not vocabulary.
- **Visible simplicity, invisible engineering.** IDs, bindings, health checks,
  and migrations live in `.wirenet/` and the plugin. The visible tree looks
  like Jason's vault, not like a schema system.
- **Grow on first use.** Optional folders and files exist only once real
  content needs them. No empty placeholders, no seeded catalogs.
- **Degrade gracefully.** Every feature works without qmd, without a network,
  and without the doctor. Missing tooling reduces convenience, never access.
- **One fact, one home.** Canonical facts live in exactly one document; other
  documents link. Portfolio facts live in `projects/index.md`.

## Visible File Model

```text
~/Manager/
├── README.md                 who the user is, how this folder works (short)
├── TODO.md                   ordered cross-project stack (Now / Next / Waiting / Later)
├── AGENTS.md                 one page: read order, update threshold, approval gate
├── agent/USER_CONTEXT.md     durable working style and boundaries
├── projects/
│   ├── index.md              the only portfolio catalog, grouped by state
│   └── <slug>/
│       ├── README.md         required: status, decisions, next move, sources
│       ├── AGENTS.md         only when real local deltas exist
│       ├── GOAL.md           optional: durable outcome contract
│       └── RESULT.md         optional: completed evidence
├── people/<slug>.md          work-relevant collaborator context
└── .wirenet/                 machine-local: bindings, versions, health state
```

Created lazily, on first real content: `experiments/<slug>/`, `notes/`,
`sources/`, `docs/`, `archive/`, `outputs/` (git-ignored). Their meaning is
defined in the skill's routing reference, not in per-folder README files.

## Frontmatter

- No frontmatter is required. The H1 is the canonical title.
- `title` and `description` are the only core-defined keys and are optional.
- Unknown keys are preserved verbatim (producer metadata stays safe).
- Removed from the core: `type`, `schema`, `visibility`, `status`,
  `created_at`, `updated_at`, `last_edited`, `project_id`, `experiment_id`,
  OKF profile declarations. Git carries history; location and the index carry
  lifecycle; typed projection becomes an optional layer.

## Identity And Bindings

- A pack's identity is its slug (directory name). Renames are explicit moves.
- `.wirenet/workspace-bindings.json` maps slug → absolute external path and
  lists ignored folders. It is the only place absolute paths live.
- No UUIDs in documents. If a future sync layer needs stable IDs, it maintains
  them in `.wirenet/`, invisibly.

## Lifecycle Without Status Fields

State is expressed by location and by grouping in `projects/index.md`:

- `projects/index.md` groups packs under **Active**, **Waiting / Blocked**,
  and **Later**. The group is the status; no enum field exists.
- Completing or retiring a pack moves it to `archive/<slug>/` and moves its
  index entry to an **Archived** section (or removes it).
- Waiting and blocked stay live in `projects/`; never archive open handoffs.
- Experiments live in `experiments/<slug>/` with a question and a decision
  criterion in their README; they end by conclusion, promotion (move to
  `projects/`), or archive. The original stays referenced as origin evidence.
- The doctor validates consistency (every pack has an index entry, every entry
  resolves, archived packs receive no new active state) instead of validating
  frontmatter.

## Update Contract

Write when a future task would otherwise misunderstand: the desired outcome,
durable status or a milestone, an owner or responsibility, a decision, a
blocker, a deadline, a canonical source, a verified result, or the next step.

Do not write: activity logs, raw messages or media, generated files,
speculative inference presented as fact, secrets or credentials, or
implementation detail that will not matter next session.

Preview every inferred durable write and obtain approval, unless the user
already approved that exact change. Distinguish sent, received, drafted,
discussed, and approved. External side effects (messages, meetings, cloud
documents, automations, sync) each require their own explicit approval.

## Global Wiring

Two mechanisms make the Manager present in every session; both are installed
and maintained by the plugin (with approval), never hand-edited by the user:

1. **Managed global block** (global `AGENTS.md` / `CLAUDE.md`), ~5 lines: the
   Manager lives at `~/Manager`; before working in a project folder, check the
   bindings and read the bound pack's README first; after meaningful progress,
   propose a pack update (preview, then approval).
2. **Local binding line**: when a workspace is bound, one line is added to that
   workspace's own `AGENTS.md`/`CLAUDE.md`: durable context for this project
   lives at `~/Manager/projects/<slug>/`. This makes the nearest-instructions
   mechanism of Codex and Claude Code work in both directions.

## Continuity

The felt product is an assistant that keeps an eye on things. Two optional,
approval-gated mechanisms provide it, implemented per runtime (scheduled tasks
in Claude Code, thread automations in Codex):

- a recurring silent check-in that reconciles missed handoffs and surfaces the
  stack only when something needs attention;
- semantic local commits with safe push windows (e.g. 09:00 and 16:00) under
  strict git safety boundaries, each window separately approved.

Neither is required for core operation; both default to off until onboarding
offers them.

## Retrieval

qmd indexes the Manager as one collection, registered at onboarding with
approval. It is candidate routing: search results route, full document reads
answer, and canonical Markdown wins over a stale index. Known entry points
(`TODO.md`, `projects/index.md`, a named pack) are read directly. Nothing in
the core requires qmd to be installed.

## Onboarding

Interview-first, following the upstream flow: resolve or create the folder,
interview the user, scan approved connectors, propose the first packs and
people files, install the global block and qmd registration (each with its own
approval). Success criterion: after ~30 minutes the user has `TODO.md`, two or
three packs, and at least one person file — and has not learned a single
structure word.

## Skill Surface

Exactly two skills; maintenance is a reference, not a skill:

- `$manager`: one page. Orient (read order), retrieve (qmd optional), work
  (stack, signals, next move), write (threshold, routing, approval), lifecycle
  (five lines). Three references: `vault-model.md` (structure, routing,
  lifecycle, tools), `workspace-sync.md` (bound external workspaces), and
  `maintenance.md` (doctor, plugin update checks, qmd upkeep).
- `$manager-setup`: first-time setup, adopting an existing folder, and
  structural repair. Interview-first; personalizes the vault's `AGENTS.md`,
  offers the write-like-me voice bootstrap (generated skill lives at the
  global skill root, outside the vault), and hands off to `$manager` when
  done. Runs once per machine.
- Scripts drop from 18 to a doctor (health + update check), a qmd sync helper,
  and optionally the viewer. Creation generators are removed: the agent writes
  packs from templates; the doctor validates the result. Determinism lives in
  validation, not generation.

## Optional Layers (Explicitly Not Core)

- `GOAL.md` / `RESULT.md`: core-named conventions, created only when a project
  earns them (upstream's own generators never create them by default).
- `WORKLOG.md`: owned exclusively by an explicitly invoked `$ultragoal`.
- `log.md`, packet-local `index.md`, `docs/communication-and-files.md`: allowed
  when real content earns them; never seeded.
- Typed OKF projection, Inspector/viewer payloads, Base/Shelf synchronization,
  client runtime, control plane: separate layers with their own contracts,
  opened on real demand. The core must not depend on any of them.

## Memory Hygiene

Agent-maintained memory rots without a counterweight. The doctor flags a pack
as possibly stale when its last change is clearly old (around 90 days) while
it sits in an active index group without a waiting handoff. A staleness
finding is a proposal to review, archive, or reaffirm — never an automatic
action.

## Compatibility Promise

Any plugin from v0.5 onward reads any vault from v0.5 onward. New conventions
arrive as optional capabilities; migrations are always explicit, dry-run-first,
and approved. A plugin update never rewrites personal content.

## Migration From v0.2 (Summary Only)

A separate dry-run-first, doctor-validated release step: strip non-core
frontmatter (preserving unknown producer keys), remove IDs from documents,
re-key bindings by slug, replace status fields with index grouping, and
deduplicate root documents so portfolio facts live only in
`projects/index.md`. Personal prose is never rewritten without approval.

## Upstream Preservation

Preserved from `jxnl/personal-monorepo-template`: the repository-as-vault
model, `projects/` + `experiments/` + `people/`, per-pack `README.md` +
`AGENTS.md` with identical filenames, nearest-AGENTS routing, interview
onboarding, approval before shared-memory writes, durable meaning over raw
activity. Added beyond upstream: installation without git knowledge, external
workspace bindings with two-way wiring, health checks and managed updates,
optional retrieval, and the managed-service path.

Upstream's skill set maps into the plugin as follows: `onboarding`,
`new-project`, and `new-person` → `$manager-setup` plus the `$manager`
lifecycle and people sections; `assistant` → `$manager` with the continuity
model; `write-like-me-bootstrap` → the onboarding voice step; `ultragoal`
stays an optional, separately invoked layer owning `WORKLOG.md`. Upstream's
developer and utility skills (`gh-commit`, `gh-fix-ci`, `gh-address-comments`,
`audit-ai-code`, `audit-ai-frontend`, `loop`, `yeet`) are deliberately not
part of the Manager plugin; content skills (`audit-ai-writing`,
`simple-html-artifact`) ship separately in `content-tools@wirenet`.

## Resolved Review Questions

1. `agent/USER_CONTEXT.md` stays a separate file: README remains the short
   human landing page, USER_CONTEXT the agent-facing profile.
2. "Match the language of the existing documents" replaces the
   `content_language` frontmatter field; no machine-readable home is needed.
3. `projects/index.md` keeps a compact **Archived** section alongside
   `archive/`.
