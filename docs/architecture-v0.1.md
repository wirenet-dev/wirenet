---
last_edited: 2026-07-15
---

# WireNet Manager v0.1 Architecture

## Core Design Principle: Metadata As Code

WireNet Manager treats metadata as a maintained architectural surface rather
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
| Plugin | Reusable product behavior and its explanation | Skills, scripts, schemas, templates, viewer, and product docs under `plugins/wirenet-manager/` and `docs/` |
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
     update canonical state; add a sparse log only when useful
```

## Product Files

### Marketplace And Manifest

- `.agents/plugins/marketplace.json` exposes the local plugin package.
- `plugins/wirenet-manager/.codex-plugin/plugin.json` identifies version 0.1.2,
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
- `scripts/okf_projection.py`: the single typed-concept, reserved-file, and
  Markdown-link projection shared by Inspector and future export or sync consumers.
- `scripts/generate_manager_viewer.py`: one-shot read-only WireNet Inspector and
  optional loopback-only transport for ChatGPT's built-in Browser.
- Bootstrap and sync skill scripts provide their task-specific entry points.

### WireNet Inspector

`viewer/manager-viewer.html` is a single HTML template based on the official
Google Cloud OKF graph-and-detail viewer model. The generator embeds typed
Manager concepts without filtering or rewriting their bodies. A
non-reserved Markdown file must have a non-empty `type` to enter the projection.
`index.md`, `log.md`, `AGENTS.md`, technical plugin files, skills, scripts,
hidden state, ignored outputs, and local binding JSON never enter the generated
Inspector. The Doctor rejects any other in-scope Markdown without an OKF `type`.

Standard Markdown links between concepts create the only graph edges. The page
renders complete concept Markdown and backlinks, with Google's search, type
filter, layout, reset, graph, and detail interactions. WireNet adds its identity,
safe Markdown rendering, link normalization, and loopback-only serving. The
Inspector adds no packet, folder, agent-routing, or inferred semantic edges and
offers no editing or filesystem API.

### Layer Boundary

WireNet preserves Jason Liu's plain-file operating model instead of replacing
it with OKF:

1. Project `README.md` remains canonical current state; optional `GOAL.md`,
   `RESULT.md`, `WORKLOG.md`, and additional concepts remain normal Markdown.
2. `AGENTS.md` remains executable routing and behavioral guidance for agents,
   uses a separate runtime schema, and is never an OKF concept.
3. `.wirenet/project-bindings.json` stores only device-local project IDs,
   paths, and classifications; it does not contain instructions or project prose.
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
routed shelves, and they keep the Jason reference separate from WireNet's OKF,
binding, plugin, and viewer additions. The human-readable analysis lives under
`docs/routing/`.

### Seed

`plugins/wirenet-manager/templates/manager/` is the only runtime seed shipped by
the plugin. It contains content and operating rules, not copies of plugin
skills. Bootstrap adds the dynamic `.wirenet/manager.json` file.

## Runtime Files

- `AGENTS.md`: Manager-wide read order, durable-state rules, and safety; runtime only.
- `README.md`: typed `Manager Overview` and human landing page for this instance.
- `index.md`: required WireNet bundle catalog and OKF version declaration.
- `TODO.md`: cross-project current stack.
- `agent/USER_CONTEXT.md`: durable user working context.
- `projects/index.md`: canonical catalog for progressive disclosure and search.
- `projects/<slug>/`: open packet with required `README.md` and `AGENTS.md`;
  other concepts, packet-local indexes, and logs are optional.
- `people/`: recurring collaborator notes.
- `notes/`: durable scratch material without a canonical home.
- `docs/`: optional structured documents without a stronger canonical home.
- `sources/`: curated Knowledge Shelf, read-only by default and link-first.
- `experiments/` and `archive/`: bounded supporting shelves.
- `outputs/`: ignored device-local working memory for generated intermediates.
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
- no translation layer for other workspace layouts;
- no imposed global folder hierarchy.
