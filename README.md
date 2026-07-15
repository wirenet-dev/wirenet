---
last_edited: 2026-07-15
---

# WireNet Manager

WireNet Manager is an installable ChatGPT Work and Codex plugin for local,
reviewable work memory. It bootstraps a content-only `~/Manager`, connects
external workspaces through device-local bindings, and maintains portable
Project Packs that begin with a human handoff and local agent instructions,
then grow only when the work earns more structure.

## Metadata As Code

**Metadata as Code is the central WireNet Manager design principle.** Durable
work context should not disappear into hidden application state: its identity,
type, relationships, routing, and lifecycle live next to human-readable content
in version-controlled files.

- Markdown remains the canonical content that humans and agents can inspect.
- YAML frontmatter gives concepts explicit types, stable IDs, visibility, and
  producer-owned extensions.
- `AGENTS.md` keeps runtime routing reviewable without becoming knowledge;
  indexes and Markdown links make disclosure and concept relationships explicit.
- Small JSON registries hold only machine-local identity and path resolution,
  never the project prose itself.
- Schemas, deterministic generators, doctors, routing contracts, and regression
  tests evolve that metadata with software-level discipline.

This creates a portable foundation for future synchronization without making a
database, proprietary UI, or invisible agent memory the source of truth.

## Install And Bootstrap

```sh
codex plugin marketplace add wirenet-dev/wirenet-manager --ref main
```

Restart ChatGPT, install **WireNet Manager**, then start a new task with:

```text
$wirenet-manager-bootstrap Set up my WireNet Manager in ~/Manager.
```

The bootstrap previews every write, creates no cloud sync, and leaves external
project folders where they already are. See
[`docs/installing-wirenet-manager.md`](docs/installing-wirenet-manager.md) for
the full flow.

## v0.1 Boundary

```text
Developer repository / installed plugin       User runtime

plugins/wirenet-manager/                       ~/Manager/
├── .codex-plugin/plugin.json                  ├── AGENTS.md
├── skills/                                    ├── index.md and README.md
├── scripts/                                   ├── TODO.md and agent/
└── templates/manager/             ───────▶    ├── projects/ and people/
                                                ├── notes/, docs/, sources/
                                                ├── ignored outputs/
external project folders           ◀──────▶    └── .wirenet/
```

- The plugin owns behavior, schemas, deterministic helpers, and the seed.
- `~/Manager` owns personal context, Project Packs, local bindings, and Git
  history. It contains no copied plugin skills in v0.1.
- External projects keep code, media, datasets, and operational files.
- Client and specialist capabilities remain independently versioned plugins.
- No database, cloud sync, shared Knowledge Hub, or filesystem watcher is part
  of v0.1.

## Plugin Skills

- `$wirenet-manager`: ongoing orientation, current stack, and Manager task.
- `$wirenet-manager-bootstrap`: setup, health checks, repair, project discovery,
  installation of the global reconciliation rule, and optional user-approved
  workspace routing.
- `$wirenet-manager-sync`: classify external workspaces and reconcile meaningful
  Project Pack changes.

## Read-Only Manager Viewer

`$wirenet-manager` can open a small branded viewer for the Manager's portable
OKF knowledge projection. A non-reserved Markdown file enters that projection
only when it has a non-empty OKF `type`; `index.md` and `log.md` remain reserved
navigation and history. `AGENTS.md`, plugin metadata, skills, scripts, hidden
state, device-local bindings, and ignored outputs stay outside the knowledge
graph. The Doctor rejects any other in-scope Markdown without an OKF `type`.

The viewer follows the graph-and-detail model of Google's official OKF HTML
viewer: typed concepts become nodes, standard Markdown links between concepts
become directed graph edges, and selecting a concept renders its complete body
and backlinks. Reserved indexes and logs remain readable through a small Browse
control but never become graph nodes. A reading view hides the graph without
creating another content mode. The viewer is read-only and has no synthetic
routing edges, Node runtime, database, watcher, or edit API.

For local development:

```sh
python3 plugins/wirenet-manager/scripts/generate_manager_viewer.py \
  --manager-dir /path/to/Manager --serve
```

The script binds only to `127.0.0.1` so ChatGPT's built-in Browser can open the
page. Without `--serve`, it writes a single generated HTML file to the system
temporary directory by default.

Skills use the current installable plugin structure. The repo marketplace is at
`.agents/plugins/marketplace.json`; the plugin manifest is at
`plugins/wirenet-manager/.codex-plugin/plugin.json`.

## Project Pack Contract

Every v0.1 Project Pack contains:

| File | Responsibility | WireNet OKF mapping |
| --- | --- | --- |
| `README.md` | Current status and next move | `Project Status` |
| `AGENTS.md` | Read order, sources, safety, update rules | runtime sidecar outside OKF |

These two files are the open core, not a fixed form. The Manager may add
`GOAL.md`, `RESULT.md`, `WORKLOG.md`, reserved `index.md` or `log.md`, and other
typed concepts when they improve the handoff. All concepts and the runtime
sidecar share one stable `project_id`; reserved files are identified by their
packet path and carry no duplicate concept metadata. Manager `index.md` and
`projects/index.md` are required by the WireNet profile as navigational entry
points, even though OKF itself makes both indexes and logs optional. Packet-local
indexes and all logs remain optional.

Machine-local paths live only in
`~/Manager/.wirenet/project-bindings.json`. Project Pack metadata follows a
small WireNet OKF profile; the binding registry itself is device-local runtime,
not part of the knowledge bundle or a claim that v0.1 implements the complete
OKF mirror system.

`AGENTS.md` uses the separate `wirenet-runtime/v0.1` metadata schema and has no
OKF `type`. Codex reads its Markdown instructions normally; the knowledge
projection and future Knowledge Hub do not reinterpret those instructions as
concept relationships.

## Developer Layout

- `.agents/plugins/marketplace.json`: local and future public marketplace.
- `plugins/wirenet-manager/`: installable plugin package.
- `plugins/wirenet-manager/templates/manager/`: content-only runtime seed.
- `plugins/wirenet-manager/scripts/`: deterministic shared Manager helpers,
  including the common OKF projection and read-only viewer generator.
- `plugins/wirenet-manager/viewer/`: one-file viewer template.
- `docs/architecture-v0.1.md`: file-by-file architecture and routing diagram.
- `docs/project-pack-contract.md`: Project Pack and OKF profile.
- `docs/testing-markdown-as-code.md`: contract surfaces, test layers, and
  regression invariants for the natural-language product.
- `docs/routing/`: frozen Jason and WireNet routing descriptions plus the
  regression strategy.
- `contracts/routing/`: machine-readable routing entities, producers,
  consumers, evidence, and route contracts.
- `docs/installing-wirenet-manager.md`: installation and bootstrap path.
- `scripts/compare_upstream.py`: read-only comparison with Jason's upstream.
- `scripts/compare_routing_contracts.py`: deterministic semantic contract
  comparison without fetching or mutating Git state.
- `tests/`: plugin, bootstrap, routing, template, and frozen-reference checks.

## Upstream Reference

WireNet Manager is a deliberate downstream of Jason Liu's
[`personal-monorepo-template`](https://github.com/jxnl/personal-monorepo-template).
It preserves the useful plain-file, Git-backed Assistant model while separating
installable intelligence from personal content and adding portable Project
Packs, local bindings, global reconciliation, and OKF-compatible navigation.

The root `.codex/`, shelves, and template files remain as a downstream reference
to Jason's original repository while v0.1 is developed. They are not copied
into the generated Manager by the plugin. This boundary keeps upstream changes
mechanically reviewable without making the user's runtime depend on the
repo-local reference implementation.

## Local Development

```sh
python3 scripts/validate_markdown.py .
python3 /Users/gitt/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py \
  plugins/wirenet-manager
pytest -q
git diff --check
```

Preview a disposable bootstrap without mutating the destination:

```sh
python3 plugins/wirenet-manager/skills/wirenet-manager-bootstrap/scripts/bootstrap_manager.py \
  --manager-dir /tmp/wirenet-manager-review
```

Apply only to a disposable directory during development:

```sh
python3 plugins/wirenet-manager/skills/wirenet-manager-bootstrap/scripts/bootstrap_manager.py \
  --manager-dir /tmp/wirenet-manager-review \
  --apply
```

Compare with upstream without merging:

```sh
python3 scripts/compare_upstream.py --fetch
```

Compare the frozen routing contracts without network access:

```sh
python3 scripts/compare_routing_contracts.py
```

## Release Status

Plugin `0.1.2` is the current reviewed implementation of the v0.1 architecture.
The repository's `main` branch is the canonical installation source.
