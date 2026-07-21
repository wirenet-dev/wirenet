# Vault Model

What a healthy Manager looks like, where content belongs, how lifecycle
works, and which tools help. This reference ships with the plugin; the user
never needs to read it — the agent applies it so the user only experiences it.

## Structure

```text
~/Manager/
├── README.md                 who the user is, how this folder works (short)
├── TODO.md                   ordered cross-project stack (Now / Next / Waiting / Later / Someday)
├── AGENTS.md                 one page: read order, update threshold, approval gate
├── agent/USER_CONTEXT.md     durable working style and boundaries
├── projects/
│   ├── index.md              the only portfolio catalog, grouped by state
│   └── <slug>/
│       ├── README.md         required: status, decisions, next move, sources
│       ├── AGENTS.md         only when real local deltas exist
│       ├── GOAL.md           optional: durable outcome contract
│       └── RESULT.md         optional: completed evidence
├── areas/<slug>/README.md    ongoing responsibility: standard, state, cadence
├── people/<slug>.md          durable relationship context
└── .wirenet/                 machine-local: bindings, versions, health state
```

Created lazily, on first real content — never seeded empty:

- `areas/<slug>/`: an ongoing responsibility with a standard to maintain but
  no end date. Starts as a single README (what "healthy" means, current state
  against that standard, related projects, a self-chosen review cadence);
  `routines/` (procedures this area owns) and `reference/` (material it
  maintains) appear only when real content earns them.
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

- Classify with one question: **does it end?** A defined outcome → project,
  and its README must be able to say when it is done. A bounded question with
  a decision criterion → experiment. A responsibility with a standard but no
  end → area. Example: a client *relationship* is an area (standard: client
  healthy, invoiced, next opportunity visible; routines: invoicing); each
  *mandate* for that client is a project that ends with delivery. Areas spawn
  projects; the project links its parent area in prose, and status lives only
  in the project.
- Propose a new area only when recurring upkeep work has no home — never
  prophylactically. Not every client or topic earns one.
- `projects/index.md` groups packs under **Active**, **Waiting / Blocked**,
  **Later**, **Ongoing** (the areas), and a compact **Archived** section.
  Moving the entry is the transition.
- Folders that should never produce reminders are recorded as ignored in the
  bindings, never re-asked. Knowledge-first packs stay Manager-native; bind an
  external workspace only when code, media, data, or a toolchain need their
  own working tree.
- Complete or retire: confirm no open next move or waiting handoff remains,
  then move the pack to `archive/<slug>/` and its entry to Archived. Never
  archive merely because work is blocked or waiting. An area archives only
  when the responsibility itself ends — never for being quiet; idle is normal
  for areas, and staleness is measured against the area's own review cadence.
- Reactivate before writing new active state into an archived pack. Promote an
  experiment by moving it to `projects/`, transferring its binding, and
  linking the origin.
- When a workspace is bound, one approved line in that workspace's own
  `AGENTS.md`/`CLAUDE.md` points back to the pack, so nearest-instructions
  routing works in both directions.

## Tools

All tools are optional conveniences; the Manager must stay fully usable with
nothing but a file reader and git.

- **git** carries history, review, and backup; approved push windows sync a
  private remote. Never configure remotes or automation without approval.
- **qmd** indexes the Manager as one collection (registered at setup, with
  approval). Search results are candidate routing; read the full documents
  before answering; canonical Markdown wins over a stale index. Never run a
  global `qmd update` implicitly — the collection refresh is an explicit
  maintenance action.
- **The doctor** (plugin script) validates conventions — every pack has a
  resolving index entry, bindings resolve, no seeded placeholders — instead of
  validating frontmatter. Run it after structural moves.
- **Obsidian or any Markdown editor** may open the folder directly as a local
  view; `.obsidian/` stays git-ignored, device-local UI state.
