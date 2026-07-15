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

## Canonical Three-Layer Model

Every WireNet Manager file belongs to exactly one architectural layer. This is
the primary decision rule for extending the product:

| Layer | Owns | Canonical location | Portability |
| --- | --- | --- | --- |
| Plugin | Reusable behavior, schemas, generators, validators, templates, and product documentation | Installed `plugins/wirenet-manager/` package | Versioned and distributed as the product |
| Runtime | Agent routing and device-local operating state | `AGENTS.md`, nested `AGENTS.md`, `.wirenet/`, and ignored working output | Inspectable and versionable where useful, but never interpreted as OKF knowledge |
| Knowledge | Durable user meaning: context, projects, people, decisions, goals, results, and sources | In-scope Markdown inside `~/Manager` | Portable OKF bundle and future synchronization source |

Use three questions whenever a new file or rule is proposed:

1. Should every installation behave this way? Put it in the plugin.
2. Does an agent or this device need it to operate? Put it in runtime.
3. Is it durable meaning another person or device should understand? Store it
   as OKF knowledge.

Inside a generated Manager, the Markdown boundary is intentionally strict:
`AGENTS.md` is runtime; `index.md` and `log.md` are reserved OKF support
documents; every other in-scope Markdown file is a typed OKF concept. Untyped
guide Markdown is invalid. This is why generic shelf `README.md` files do not
belong in `~/Manager`: reusable shelf rules live in the plugin and local routing
lives in `AGENTS.md`. The root Manager `README.md` and Project Pack `README.md`
files remain because they are not manuals—they are typed instance knowledge,
respectively `Manager Overview` and `Project Status`.

The distinction also applies during development: templates in the plugin are
reusable blueprints, not user knowledge. They become runtime or knowledge only
when bootstrap materializes them in a particular user's Manager. See
[`docs/architecture-v0.2.md`](docs/architecture-v0.2.md) for the file-level
contract.

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

## v0.2 Boundary

```text
Developer repository / installed plugin       Generated Manager workspace

plugins/wirenet-manager/                       ~/Manager/
├── .codex-plugin/plugin.json                  ├── AGENTS.md             runtime
├── skills/                                    ├── .wirenet/             runtime
├── scripts/                                   ├── README.md, TODO.md    knowledge
└── templates/manager/             ───────▶    ├── index.md, log.md     OKF support
                                                ├── projects/, experiments/ knowledge
                                                ├── people/, notes/, docs/  knowledge
                                                ├── sources/                knowledge
external project folders           ◀──────▶    └── ignored outputs      local work
```

- The plugin owns behavior, schemas, deterministic helpers, and the seed.
- `~/Manager` owns personal context, Project and Experiment Packs, local
  bindings, and Git history. It contains no copied plugin skills in v0.2.
- External projects keep code, media, datasets, and operational files.
- Client and specialist capabilities remain independently versioned plugins.
- No database, cloud sync, shared Knowledge Hub, or filesystem watcher is part
  of v0.2.

## Plugin Skills

- `$wirenet-manager`: ongoing orientation, current stack, and Manager task.
- `$wirenet-manager-bootstrap`: setup, health checks, repair, project discovery,
  installation of the global reconciliation rule, and optional user-approved
  workspace routing.
- `$wirenet-manager-sync`: classify external workspaces and reconcile meaningful
  Project or Experiment Pack changes.
- `$ultragoal`: explicit-only persistent goal execution. It is installed with
  the plugin but cannot be selected implicitly.

## WireNet Inspector

`$wirenet-manager` can open the branded WireNet Inspector for the Manager's
portable OKF knowledge projection. A non-reserved Markdown file enters that projection
only when it has a non-empty OKF `type`. `index.md`, `log.md`, `AGENTS.md`,
plugin metadata, skills, scripts, hidden state, device-local bindings, and
ignored outputs do not enter the generated Inspector. The Doctor rejects any
other in-scope Markdown without an OKF `type`.

The Inspector follows the graph-and-detail model of Google's official OKF HTML
viewer: typed concepts become nodes, standard Markdown links between concepts
become directed graph edges, and selecting a concept renders its complete body
and backlinks. WireNet changes only the identity, safe Markdown rendering,
loopback transport, and the explicit projection boundary above. The Inspector
is read-only and has no synthetic routing edges, Node runtime, database,
watcher, or edit API.

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

Every Project Pack contains:

| File | Responsibility | WireNet OKF mapping |
| --- | --- | --- |
| `README.md` | Current status and next move | `Project Status` |
| `AGENTS.md` | Read order, sources, safety, update rules | runtime sidecar outside OKF |

These two files are the open core, not a fixed form. The Manager may add
`GOAL.md`, `RESULT.md`, reserved `index.md` or `log.md`, and other typed concepts
when they improve the handoff. Only an explicitly invoked `$ultragoal` may add
or update `WORKLOG.md`. All concepts and the runtime
sidecar share one stable `project_id`; reserved files are identified by their
packet path and carry no duplicate concept metadata. Manager `index.md` and
`projects/index.md` are required by the WireNet profile as navigational entry
points, even though OKF itself makes both indexes and logs optional. Packet-local
indexes and all logs remain optional.

Experiment Packs use the same open two-file core but are bounded by a question
and decision criterion. They can be concluded, archived, or promoted into a
linked Project Pack while preserving the experiment as origin evidence.

Machine-local paths live only in
`~/Manager/.wirenet/workspace-bindings.json`. Project and Experiment Pack
metadata follows small WireNet OKF profiles; the binding registry itself is
device-local runtime, not part of the knowledge bundle or a claim that v0.2
implements the complete OKF mirror system.

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
- `plugins/wirenet-manager/viewer/`: one-file WireNet Inspector template.
- `docs/architecture-v0.2.md`: file-by-file architecture and routing diagram.
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

The original scaffold is not duplicated inside this product repository. A
fetch-only `upstream` remote and the frozen contracts under `docs/routing/` and
`contracts/routing/` preserve the comparison boundary without mixing upstream
runtime files into the canonical WireNet implementation.

## Local Development

```sh
python3 scripts/validate_markdown.py .
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator/scripts/validate_plugin.py" \
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

Plugin `0.2.0` is the current implementation of the v0.2 lifecycle architecture.
The repository's `main` branch is the canonical installation source.
