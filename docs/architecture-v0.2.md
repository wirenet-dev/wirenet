---
last_edited: 2026-07-16
---

# wirenet Manager v0.2 Architecture

## Core Design Principle: Metadata As Code

wirenet Manager treats metadata as a maintained architectural surface rather
than incidental application state. Markdown owns human-readable meaning;
non-empty `type` frontmatter opts a document into the portable OKF knowledge
projection; `AGENTS.md` owns executable agent routing outside that projection;
links and indexes own knowledge navigation; and device-local JSON owns only
runtime identity and path resolution. Every layer remains versioned, reviewable,
and covered by deterministic producers, validators, and regression contracts.

This separation is the guardrail for future synchronization: a database or
Knowledge Hub may index and exchange the files, but it must not silently become
the only place where their meaning or relationships exist.

## Canonical Three-Layer Model

| Layer | Responsibility | Filesystem expression |
| --- | --- | --- |
| Plugin | Reusable product behavior and its explanation | Skills, scripts, schemas, templates, viewer, and product docs under `plugins/manager/` and `docs/` |
| Runtime | Executable routing and device-local operating state | Root and nested `AGENTS.md`, `.wirenet/`, and ignored working output |
| Knowledge | Durable portable meaning | Typed Manager concepts plus reserved OKF `index.md` and `log.md` support documents |

The layers may coexist in one workspace but do not exchange authority. Plugin
templates are product assets until bootstrap materializes them. Runtime may
route agents to knowledge but is not itself a concept or graph relationship.
Knowledge may describe work but cannot define hidden executable behavior.

For any proposed addition, route universal behavior to the plugin, local
operation to runtime, and durable shared meaning to knowledge. In a generated
Manager, `AGENTS.md` is the only in-scope runtime Markdown convention;
`index.md` and `log.md` are reserved OKF support documents; every other
in-scope Markdown file must carry a non-empty OKF `type`. Generic shelf README
manuals therefore belong in plugin documentation or runtime instructions. Only
the typed root Manager Overview and typed Project Status READMEs remain as
instance knowledge.

## Routing Overview

```text
                               install / update
GitHub or local marketplace ─────────────────────▶ wirenet Manager plugin
                                                     │
                     bootstrap content seed          │ skills + scripts
                                                     ▼
                                               ~/Manager
                                          ┌──────────┴──────────┐
                                          │                     │
                               portable Project/Experiment Packs   local bindings
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
        $manager
                  │
          inspect local binding
          ┌───────┼───────────┐
          ▼       ▼           ▼
       tracked experiment  untracked
          │       │           │
          │   reconcile        └──▶ $manager
          ▼
   propose smallest diff
          │
      user approval
          ▼
     update canonical state; add a sparse log only when useful
```

## Product Files

### Marketplace And Manifest

- `.agents/plugins/marketplace.json` exposes the three public plugin packages.
- `plugins/manager/.codex-plugin/plugin.json` identifies Manager core version
  0.4.0, interface copy, and starter prompts.
- `plugins/workflows/` and `plugins/content-tools/` are independently
  installable cross-project capability plugins.

### Skills And Playbooks

- `plugins/manager/skills/manager/`: ongoing orientation and one progressively
  disclosed set of Project, Experiment, Person, routing, and sync playbooks.
- `plugins/manager/skills/manager-setup/`: technical setup, repair, QMD,
  bundled-runtime preflight, first personal meeting, and optional personal
  writing-voice setup.
- `plugins/workflows/skills/loop/`: general-purpose task-attached recurring
  checks with explicit completion and cleanup behavior.
- `plugins/workflows/skills/ultragoal/`: explicitly invoked persistent goal
  execution with implicit invocation disabled.
- `plugins/content-tools/skills/simple-html-artifact/`: restrained static HTML
  artifacts for comprehension and inspection.
- `plugins/content-tools/skills/audit-ai-writing/`: evidence-led editorial and
  citation-quality review without detector theater.
- `.agents/skills/`: repository-only Developer audits and publishing workflow;
  these do not enter the public plugin catalog.

The two visible Manager skills replace separate UI entries for onboarding,
Project, Person, and sync operations. Those procedures remain explicit as
task-loaded references. Each distributable skill keeps `SKILL.md` concise and
places detailed contracts under `references/`; UI metadata lives in
`agents/openai.yaml`.

A generated `~/.agents/skills/write-like-me/` is personal global behavior. It
does not enter the Manager OKF bundle and is not copied into `~/Manager`.

### Deterministic Scripts

- `scripts/manager_model.py`: schemas, IDs, JSON helpers, and packet renderers.
- `scripts/create_person_note.py`: dry-run-first typed person concept generator.
- `scripts/manager_doctor.py`: read-only Manager, Project Pack, Experiment Pack,
  binding, and lifecycle validation.
- `scripts/manager_qmd.py`: dry-run-first QMD health, approved installation,
  Manager collection registration, retrieval context, and optional embeddings.
- `scripts/upgrade_manager.py`: dry-run-first version negotiation and supported
  local workspace migrations without template overwrite.
- `scripts/create_project_pack.py`: dry-run-first Manager-native or externally
  bound Project Pack creation.
- `scripts/create_experiment_pack.py`: dry-run-first lightweight Experiment Pack
  creation.
- `scripts/promote_experiment.py`: linked Experiment-to-Project promotion and
  workspace-binding transfer.
- `scripts/transition_packet.py`: deterministic lifecycle transition checks.
- `scripts/discover_projects.py`: shallow approved-root discovery.
- `scripts/okf_projection.py`: the single typed-concept, reserved-file, and
  Markdown-link projection shared by Inspector and future export or sync consumers.
- `scripts/generate_manager_viewer.py`: one-shot read-only wirenet Inspector and
  optional loopback-only transport for ChatGPT's built-in Browser.
- Bootstrap and sync skill scripts provide their task-specific entry points.

### wirenet Inspector

`viewer/manager-viewer.html` is a single HTML template based on the official
Google Cloud OKF graph-and-detail viewer model. The generator embeds typed
Manager concepts without filtering or rewriting their bodies. A
non-reserved Markdown file must have a non-empty `type` to enter the projection.
`index.md`, `log.md`, `AGENTS.md`, technical plugin files, skills, scripts,
hidden state, ignored outputs, and local binding JSON never enter the generated
Inspector. The Doctor rejects any other in-scope Markdown without an OKF `type`.

Standard Markdown links between concepts create the only graph edges. The page
renders complete concept Markdown and backlinks, with Google's search, type
filter, layout, reset, graph, and detail interactions. wirenet adds its identity,
safe Markdown rendering, link normalization, and loopback-only serving. The
Inspector adds no packet, folder, agent-routing, or inferred semantic edges and
offers no editing or filesystem API.

### Layer Boundary

wirenet preserves Jason Liu's plain-file operating model instead of replacing
it with OKF:

1. Project `README.md` remains canonical current state; optional `GOAL.md`,
   `RESULT.md`, and additional concepts remain normal Markdown. `WORKLOG.md` is
   reserved for an explicitly invoked UltraGoal.
2. `AGENTS.md` remains executable routing and behavioral guidance for agents,
   uses a separate runtime schema, and is never an OKF concept.
3. `.wirenet/workspace-bindings.json` stores only device-local Project and
   Experiment Pack IDs, paths, and ignored classifications; it does not contain
   instructions or project prose.
4. OKF `type` frontmatter, `index.md`, `log.md`, and Markdown links define the
   portable knowledge projection, progressive disclosure, chronology, and graph
   relationships.
5. Root `README.md` is a typed `Manager Overview`; Project Pack `README.md`
   files are typed `Project Status`; generic shelf README placeholders do not
   exist.
6. Inspector, future export, and future sync consumers derive from that same
   deterministic model; the Inspector emits only typed concepts, while runtime
   routing stays inspectable in the filesystem but separate.

The frozen entity and route definitions under `contracts/routing/` make this
boundary testable. They distinguish committed placeholders from semantically
routed shelves, and they keep the Jason reference separate from wirenet's OKF,
binding, plugin, and viewer additions. The human-readable analysis lives under
`docs/routing/`.

### Seed

`plugins/manager/templates/manager/` is the only runtime seed shipped by
the plugin. It contains content and operating rules, not copies of plugin
skills. Bootstrap adds the dynamic `.wirenet/manager.json` file.

### Derived QMD Retrieval

QMD is an optional device-local runtime index outside `~/Manager`. Bootstrap
registers the Manager as one collection after explicit approval. Its collection
mask includes portable concept Markdown and reserved OKF indexes and logs, but
excludes `AGENTS.md`, hidden runtime state, and `outputs/`. The index therefore
accelerates retrieval without redefining the OKF projection or becoming
portable state.

Direct reads remain authoritative for known current state. QMD routes broad,
historical, cross-project, and semantic questions to candidate documents, which
must then be fetched in full. The Manager degrades cleanly to indexes, links,
and direct reads if QMD is missing, unhealthy, or stale. No background watcher
or implicit global QMD update is part of v0.2.

## Runtime Files

- `AGENTS.md`: Manager-wide read order, durable-state rules, and safety; runtime only.
- `README.md`: typed `Manager Overview`, human landing page, and portable
  `content_language` policy for this instance.
- `index.md`: required wirenet bundle catalog and OKF version declaration.
- `TODO.md`: cross-project current stack.
- `agent/USER_CONTEXT.md`: durable user working context.
- `projects/index.md`: lifecycle-aware catalog for progressive disclosure and search.
- `projects/<slug>/`: open packet with required `README.md` and `AGENTS.md`;
  other concepts, packet-local indexes, and logs are optional.
- `experiments/index.md`: created when the first real Experiment Pack exists.
- `experiments/<slug>/`: bounded packet with required `README.md` and
  `AGENTS.md`, optional result, and promotion lineage.
- `people/`: recurring collaborator notes.
- `notes/`: durable scratch material without a canonical home.
- `docs/`: optional structured documents without a stronger canonical home,
  including a grounded cross-project communication-and-file map when useful.
- `sources/`: curated Knowledge Shelf, read-only by default and link-first.
- `archive/`: inactive durable supporting knowledge retained rather than deleted.
- `outputs/`: ignored device-local working memory for generated intermediates.
- `.wirenet/manager.json`: schema, Manager ID, plugin version, and OKF profile.
- `.wirenet/workspace-bindings.json`: device-local project paths, experiment
  paths, and ignored routes.

## Global Guidance

Bootstrap manages two independent regions in the user's global Codex
`AGENTS.md`:

- `wirenet-manager:core` is the reliable cross-project reconciliation trigger;
- `wirenet-manager:routing` is optional and contains only conventions the user
  explicitly wants applied everywhere.

The routing block is absent for users without a stable workspace layout. It is
the sole v0.2 source for global creation routes; no parallel workspace-roots
JSON is created. Device-local bindings for already known projects remain in
`.wirenet/workspace-bindings.json`.

The core block makes Manager reconciliation available from external workspaces.
The current path is classified against the registry or a Manager-native packet;
the semantic skill decides whether a meaningful handoff is worth proposing.
There is no background watcher and no write for routine edits.

## Upgrade Boundary

The plugin package and generated Manager are independently versioned. A plugin
update replaces reusable behavior and the seed used by future bootstraps, but
never copies that seed over an existing Manager. `.wirenet/manager.json` records
the materialized workspace schema. The updater compares it with the installed
plugin, previews a supported migration, requires a clean local Git checkpoint,
preserves personal prose and routing, applies only known structural transforms,
and validates the result with Doctor. A newer workspace schema stops with a
plugin-update instruction; an unsupported or ambiguous older layout stops for
manual review.

## Lifecycle Model

Project statuses are `active`, `waiting`, `blocked`, `completed`, and
`archived`. Experiment statuses are `active`, `concluded`, `promoted`, and
`archived`. The JSON lifecycle contract and transition helper validate allowed
edges; the agent still judges whether completion, archival, or promotion is
semantically warranted.

Manager-native and externally bound packets use the same knowledge contract.
The only difference is whether `.wirenet/workspace-bindings.json` contains a
local path. Promotion preserves the Experiment Pack, links both packets, and
transfers any external binding to the new Project Pack.

## Deliberate Non-Goals

- no database or multi-device synchronization;
- no automatic background filesystem watcher;
- no raw source, media, or implementation copy;
- no customer-specific capability shelf inside the generic Manager;
- no translation layer for other workspace layouts;
- no imposed global folder hierarchy.
