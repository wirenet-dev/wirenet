---
last_edited: 2026-07-15
---

# WireNet Manager

WireNet Manager is an installable ChatGPT Work and Codex plugin for local,
reviewable work memory. It bootstraps a content-only `~/Manager`, connects
external workspaces through device-local bindings, and maintains portable
four-file Project Packs.

The project is based on Jason Liu's
[`personal-monorepo-template`](https://github.com/jxnl/personal-monorepo-template).
WireNet keeps its plain-file, Git-backed Assistant model while separating the
installable intelligence from each user's personal content.

## v0.1 Boundary

```text
Developer repository / installed plugin       User runtime

plugins/wirenet-manager/                       ~/Manager/
├── .codex-plugin/plugin.json                  ├── AGENTS.md
├── skills/                                    ├── TODO.md
├── scripts/                                   ├── agent/
└── templates/manager/             ───────▶    ├── people/
                                                ├── projects/
external project folders           ◀──────▶    ├── notes/ and sources/
                                                └── .wirenet/
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

Skills use the current installable plugin structure. The repo marketplace is at
`.agents/plugins/marketplace.json`; the plugin manifest is at
`plugins/wirenet-manager/.codex-plugin/plugin.json`.

## Project Pack Contract

Every v0.1 Project Pack contains:

| File | Responsibility | WireNet OKF mapping |
| --- | --- | --- |
| `GOAL.md` | Stable outcome and completion criteria | `Project Brief` |
| `README.md` | Current status and next move | `Project Status` |
| `RESULT.md` | Completed outcomes and verification | `Project Result` |
| `AGENTS.md` | Read order, sources, safety, update rules | `Runtime Adapter` |

All four files share a stable `project_id`. Machine-local paths live only in
`~/Manager/.wirenet/project-bindings.json`. The mapping is a small WireNet OKF
profile, not a claim that v0.1 implements the complete OKF mirror system.

YAML frontmatter in `AGENTS.md` is intentionally limited to metadata. Codex
still reads the Markdown instructions normally; the metadata is not treated as
Codex configuration.

## Developer Layout

- `.agents/plugins/marketplace.json`: local and future public marketplace.
- `plugins/wirenet-manager/`: installable plugin package.
- `plugins/wirenet-manager/templates/manager/`: content-only runtime seed.
- `plugins/wirenet-manager/scripts/`: deterministic shared Manager helpers.
- `docs/architecture-v0.1.md`: file-by-file architecture and routing diagram.
- `docs/project-pack-contract.md`: Project Pack and OKF profile.
- `docs/installing-wirenet-manager.md`: installation and bootstrap path.
- `scripts/compare_upstream.py`: read-only comparison with Jason's upstream.
- `tests/`: plugin, bootstrap, routing, template, and legacy-reference checks.

The root `.codex/`, shelves, and template files remain as a downstream reference
to Jason's original repository while v0.1 is developed. They are not copied
into the generated Manager by the plugin. This boundary keeps upstream changes
mechanically reviewable without making the user's runtime depend on legacy
repo-local skill discovery.

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

## Installation Status

The repo marketplace is prepared for local development. Publishing and adding
`wirenet-dev/wirenet-manager` as a remote marketplace happen only after v0.1 is
reviewed, committed, and the repository remote is corrected from the earlier
`wirenet-vault` name.
