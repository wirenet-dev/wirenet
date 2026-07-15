---
last_edited: 2026-07-15
---

# WireNet Manager v0.1 Model

## Product And Runtime

The public Developer repository distributes an installable plugin. The plugin
contains skills, deterministic scripts, and a versioned content seed. Bootstrap
materializes only the seed as the user's local Manager.

```text
WireNet Manager plugin                  ~/Manager
├── skills/                             ├── AGENTS.md
├── scripts/                            ├── TODO.md
├── templates/manager/        ───────▶  ├── agent/
└── .codex-plugin/plugin.json           ├── people/
                                        ├── projects/
                                        ├── notes/ and sources/
                                        └── .wirenet/
```

No plugin skills are copied into `~/Manager`. A user may add personal
repo-local skills under `.agents/skills/` later, but v0.1 does not create that
folder.

## Project Packs

```text
projects/<slug>/
├── GOAL.md       # stable outcome; OKF Project Brief
├── README.md     # current state; OKF Project Status
├── RESULT.md     # completed evidence; Project Result
└── AGENTS.md     # read order and routing; Runtime Adapter
```

YAML frontmatter is safe in `AGENTS.md` as ordinary Markdown metadata. Codex
does not require or interpret it as configuration; the instructions below it
remain normal `AGENTS.md` content. Keep the metadata small and unambiguous.

## Portable And Local State

- `project_id` is stable and portable across devices.
- `.wirenet/project-bindings.json` maps that ID to local absolute paths.
- `.wirenet/manager.json` records Manager, plugin, schema, and OKF-profile
  versions.
- Project Pack files never contain device-local paths.

## Trigger Layers

1. Global instruction checks for meaningful durable state before a task ends.
2. `$wirenet-manager-sync` classifies the workspace and proposes a focused diff.
3. A long-running Manager task reconciles TODOs, packets, and signals.

There is no hidden filesystem watcher in v0.1.

The global instruction has an always-on core managed block and may have a
separate routing block. Add routing only for a convention the user explicitly
recognizes as stable. The block itself is the v0.1 source of truth: do not copy
the same routes into Manager JSON or portable Project Packs. Users without a
stable layout need only individual project bindings.
