---
last_edited: 2026-07-15
---

# Jason Liu Original Routing Contract

This document freezes the routing and usage strategy in
`jxnl/personal-monorepo-template` at commit
`df863768495aaf524a2bf9b5b25ef2622a2591a1`. The matching machine-readable
contract is
[`contracts/routing/jason-liu-original.json`](../../contracts/routing/jason-liu-original.json).

The contract records only behavior supported by a committed file, skill,
script, template, or explicit Git-ignore rule. A folder name by itself is not
treated as a routing contract.

## System Boundary

Jason's repository has one deliberately broad boundary: the repository itself
is the Assistant shared-memory vault, the skill shelf, and a place where
projects or experiments can be created. It does not formally separate a
portable project packet from an external implementation workspace.

```text
personal-monorepo/
├── AGENTS.md                 root behavior and routing
├── README.md                 human setup and workspace guide
├── TODO.md                   created during onboarding, not in pristine tree
├── agent/USER_CONTEXT.md     created during onboarding
├── projects/
│   ├── README.md             created during onboarding as packet router
│   ├── AGENTS.md             created during onboarding as collection rules
│   └── <slug>/
│       ├── README.md         canonical state or project workspace guide
│       ├── AGENTS.md         nearest local instructions
│       ├── GOAL.md           optional, manually introduced
│       └── RESULT.md         optional, manually introduced
├── experiments/<exp-slug>/  short-lived work inside the monorepo
├── people/                   collaborator and agent notes
├── notes/                    created by onboarding for durable scratch notes
├── sources/                  created by onboarding for retained evidence
├── outputs/                  committed empty placeholder; contents ignored
├── archive/                  committed empty placeholder
├── docs/                     committed empty placeholder
├── templates/                project, experiment, goal, result, and AGENTS seeds
└── .codex/skills/            repo-local procedures used in place
```

## Entity Roles

| Entity | Canonical role | Created how | Routing authority |
| --- | --- | --- | --- |
| Root `AGENTS.md` | Discovery, inheritance, durable-state routing, safety | Seed; onboarding creates only if missing | Yes |
| Root `README.md` | Human setup and top-level map | Seed | Human guide only |
| `TODO.md` | Cross-workstream follow-ups | Onboarding | State, not instructions |
| `agent/USER_CONTEXT.md` | Durable working profile | Onboarding | Context, not instructions |
| `projects/README.md` | Short explanation and active-packet router | Onboarding | Navigation |
| `projects/AGENTS.md` | Packet namespace, canonical files, and recurring-source placement | Onboarding | Yes, inherited for projects |
| Project `README.md` | Project status, handoff, sources, or run guide | Either project generator | Canonical project state |
| Project `AGENTS.md` | Nearest source order, commands, rules, and safety | Either project generator | Yes, inherited locally |
| Project `GOAL.md` | Long-running objective contract | Optional manual use of template | Canonical intent when present |
| Project `RESULT.md` | Completed work and verification | Optional manual use of template | Canonical evidence when present |
| `people/*.md` | Public-safe collaborator context | Person generators | Canonical relationship context |
| `notes/` | Durable scratch notes without a better home | Onboarding creates directory | Defined by onboarding guidance |
| `sources/` | Retained imported evidence, read-only by default | Onboarding creates directory | Defined by onboarding guidance |
| `.codex/skills/` | Repeatable repo-local procedures | Seed and customization | Procedural authority inside repo |
| `templates/` | Reusable creation scaffolds | Seed | Creation inputs, not runtime state |

## Agent Routing

```text
task begins inside repo
        │
        ▼
root AGENTS.md
        │
        ├── start with projects/, experiments/, README files
        ├── locate a named project, person, agent, prompt, or skill
        └── read nearest relevant AGENTS.md
                    │
                    ▼
             project AGENTS.md
                    │
                    ├── README.md  current state and handoff
                    ├── GOAL.md    long objective, when present
                    ├── RESULT.md  completed evidence, when present
                    └── recurring external sources named in AGENTS.md
```

The nearest `AGENTS.md` mechanism is the executable routing layer. A README may
explain structure or hold project state, but it does not override agent
instructions.

The `.github/` packaging workflow and `tests/` verification files are part of
the repository scaffold but not part of the personal-memory routing graph.

## Project Creation Has Two Overlapping Flows

The original contains two different project creators that write into the same
`projects/<slug>/` namespace:

1. `new-project` creates a project or experiment with `README.md` and normally
   `AGENTS.md`. The README includes setup/run fields, so the folder can be an
   actual working project.
2. Assistant onboarding's project-note generator creates a rolling workstream
   packet with `README.md` and `AGENTS.md`, then adds it to
   `projects/README.md`.

Neither generator creates `GOAL.md` or `RESULT.md`, even though the root
instructions route long objectives and completed evidence to those files and
templates for both exist. This is an original gap, not WireNet behavior.

## What The Supporting Shelves Actually Mean

### `notes/`

This shelf is intentional. Onboarding defines it as durable scratch notes that
do not yet belong in a person or project note. It is missing from the pristine
Git tree only because the bootstrap creates an otherwise empty directory.

### `sources/`

This shelf is also intentional. Onboarding defines it as retained imported
evidence and source material, read-only by default. It is not a location for
ordinary project repositories.

### `outputs/`

The repository commits only `outputs/.gitkeep`, and `.gitignore` ignores every
other file below `outputs/`. No README, AGENTS file, skill, or script defines
its lifecycle. The strongest supported conclusion is that it is a disposable
or local output shelf, not canonical memory and not a place Jason explicitly
routes repositories.

### `archive/` and `docs/`

Both are empty placeholders with no original routing rules. Their names suggest
possible uses, but the reference contract deliberately records their authority
as undefined.

## Memory Update Strategy

Assistant is expected to preserve durable meaning rather than raw activity:

- connector scans and user corrections may support proposed updates;
- explicit approval is required before shared-memory writes;
- canonical existing files should be updated before adjacent notes are made;
- project status goes to project README files;
- recurring project sources and routing go to the nearest project AGENTS file;
- raw messages, transcripts, source dumps, and weak inference stay out.

There is no background filesystem watcher, external path registry, OKF graph,
or multi-device synchronization protocol in the original.

## Reference Evidence

The most important source files are:

- upstream `AGENTS.md` and `README.md`;
- `.codex/skills/onboarding/references/shared-memory-vault.md`;
- `.codex/skills/onboarding/scripts/setup_shared_memory_vault.py`;
- `.codex/skills/onboarding/scripts/new_project_note.py`;
- `.codex/skills/new-project/scripts/new_project.py`;
- `.codex/skills/assistant/references/memory-guidance.md`;
- `templates/GOAL.md`, `templates/RESULT.md`, `templates/project_README.md`, and
  `templates/PROJECT_AGENTS.md`;
- `.gitignore` for the only evidence about `outputs/` contents.
