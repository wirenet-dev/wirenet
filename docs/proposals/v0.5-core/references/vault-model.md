# Vault Model

What a healthy Manager vault looks like, where content belongs, how lifecycle
works, and which tools help. This reference ships with the plugin; the user
never needs to read it — the agent applies it so the user only experiences it.

## Structure

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

Created lazily, on first real content — never seeded empty:

- `experiments/<slug>/`: bounded spike with a question and decision criterion.
- `notes/`: durable scratch without a better home.
- `sources/`: curated retained evidence — never large, private, or operational
  source trees.
- `docs/`: structured cross-project documents with no stronger home.
- `archive/`: inactive durable context that stays reviewable.
- `outputs/`: git-ignored transient intermediates under `outputs/<task-slug>/`.

## Rules

- No frontmatter is required; the H1 is the canonical title. `title` and
  `description` are the only defined keys. Preserve unknown keys verbatim.
- One fact, one home: canonical facts live in exactly one document; others
  link. Portfolio facts live only in `projects/index.md`.
- Absolute external paths live only in `.wirenet/workspace-bindings.json`,
  keyed by slug. No IDs in documents.
- Never store secrets, credentials, raw mails, private attachments, or copies
  of external source trees.
- Do not force content into a conventional filename to fill a template, and do
  not create empty optional documents.

## Lifecycle

State is location plus index group — no status fields:

- `projects/index.md` groups packs under **Active**, **Waiting / Blocked**,
  **Later**, and a compact **Archived** section. Moving the entry is the
  transition.
- Classify new work once: project (multi-session, durable state), experiment
  (bounded question + decision criterion), or ignored (recorded in bindings,
  never re-asked). Knowledge-first projects stay Manager-native; bind an
  external workspace only when code, media, data, or a toolchain need their
  own working tree.
- Complete or retire: confirm no open next move or waiting handoff remains,
  then move the pack to `archive/<slug>/` and its entry to Archived. Never
  archive merely because work is blocked or waiting.
- Reactivate before writing new active state into an archived pack. Promote an
  experiment by moving it to `projects/`, transferring its binding, and
  linking the origin.
- When a workspace is bound, one approved line in that workspace's own
  `AGENTS.md`/`CLAUDE.md` points back to the pack, so nearest-instructions
  routing works in both directions.

## Tools

All tools are optional conveniences; the vault must stay fully usable with
nothing but a file reader and git.

- **git** carries history, review, and backup; approved push windows sync a
  private remote. Never configure remotes or automation without approval.
- **qmd** indexes the vault as one collection (registered at onboarding, with
  approval). Search results are candidate routing; read the full documents
  before answering; canonical Markdown wins over a stale index. Never run a
  global `qmd update` implicitly — the collection refresh is an explicit
  maintenance action.
- **The doctor** (plugin script) validates conventions — every pack has a
  resolving index entry, bindings resolve, no seeded placeholders — instead of
  validating frontmatter. Run it after structural moves.
- **Obsidian or any Markdown editor** may open the folder directly as a local
  view; `.obsidian/` stays git-ignored, device-local UI state.
