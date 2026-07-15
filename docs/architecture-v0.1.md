---
last_edited: 2026-07-15
---

# WireNet Manager v0.1 Architecture

## Routing Overview

```text
                               install / update
GitHub or local marketplace ─────────────────────▶ WireNet Manager plugin
                                                     │
                     bootstrap content seed          │ skills + scripts
                                                     ▼
                                               ~/Manager
                                          ┌──────────┴──────────┐
                                          │                     │
                                  portable Project Packs   local bindings
                                          │                     │
                         future sync       │                     │ path lookup
                                          ▼                     ▼
                                  Knowledge Hub later     external workspace
                                                          code / media / data

External task ends
       │
       ├─ no meaningful durable change ───────────────▶ no Manager write
       │
       └─ meaningful durable change
                  │
                  ▼
        $wirenet-manager-sync
                  │
         classify local path
          ┌───────┼───────────┬───────────┐
          ▼       ▼           ▼           ▼
       tracked  project   experiment    ignored
          │       │           │           │
          │   create pack   remember     stay quiet
          ▼
   propose smallest diff
          │
      user approval
          ▼
     update canonical state and compact log
```

## Product Files

### Marketplace And Manifest

- `.agents/plugins/marketplace.json` exposes the local plugin package.
- `plugins/wirenet-manager/.codex-plugin/plugin.json` identifies version 0.1.1,
  bundled skills, interface copy, and starter prompts.

### Skills

- `skills/wirenet-manager/`: ongoing Manager task and orientation behavior.
- `skills/wirenet-manager-bootstrap/`: seed, repair, discovery, and global rule.
- `skills/wirenet-manager-sync/`: cross-workspace classification and durable
  reconciliation.

Each skill keeps its `SKILL.md` concise and places detailed contracts under
`references/`. UI metadata lives in `agents/openai.yaml`.

### Deterministic Scripts

- `scripts/manager_model.py`: schemas, IDs, JSON helpers, and Project Pack renderers.
- `scripts/manager_doctor.py`: read-only Manager and Project Pack validation.
- `scripts/create_project_pack.py`: dry-run-first packet and binding creation.
- `scripts/discover_projects.py`: shallow approved-root discovery.
- Bootstrap and sync skill scripts provide their task-specific entry points.

### Seed

`plugins/wirenet-manager/templates/manager/` is the only runtime seed shipped by
the plugin. It contains content and operating rules, not copies of plugin
skills. Bootstrap adds the dynamic `.wirenet/manager.json` file.

## Runtime Files

- `AGENTS.md`: Manager-wide read order, durable-state rules, and safety.
- `README.md`: human explanation of the local workspace.
- `TODO.md`: cross-project current stack.
- `agent/USER_CONTEXT.md`: durable user working context.
- `projects/index.md`: compact catalog for progressive disclosure and search.
- `projects/<slug>/`: four portable state documents plus one OKF `log.md`.
- `people/`: recurring collaborator notes.
- `notes/`: durable scratch material without a canonical home.
- `sources/`: retained evidence, read-only by default.
- `experiments/`, `outputs/`, `archive/`: bounded supporting shelves.
- `.wirenet/manager.json`: schema, Manager ID, plugin version, and OKF profile.
- `.wirenet/project-bindings.json`: device-local project paths and ignored or
  experimental routes.

## Global Guidance

Bootstrap manages two independent regions in the user's global Codex
`AGENTS.md`:

- `wirenet-manager:core` is the reliable cross-project reconciliation trigger;
- `wirenet-manager:routing` is optional and contains only conventions the user
  explicitly wants applied everywhere.

The routing block is absent for users without a stable workspace layout. It is
the sole v0.1 source for global creation routes; no parallel workspace-roots
JSON is created. Device-local bindings for already known projects remain in
`.wirenet/project-bindings.json`.

## Deliberate Non-Goals

- no database or multi-device synchronization;
- no automatic background filesystem watcher;
- no raw source, media, or implementation copy;
- no customer-specific capability shelf inside the generic Manager;
- no forced rewrite of older personal vaults;
- no imposed global folder hierarchy.
