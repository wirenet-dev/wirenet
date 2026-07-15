---
last_edited: 2026-07-15
---

# Installing WireNet Manager v0.2

## Distribution

WireNet Manager is distributed through a Codex plugin marketplace from
[`wirenet-dev/wirenet-manager`](https://github.com/wirenet-dev/wirenet-manager).
Users do not clone the product repository into `~/Manager` and do not need to
work with GitHub themselves.

During local development, the repository marketplace is
`.agents/plugins/marketplace.json`. After publication, add it with:

```sh
codex plugin marketplace add wirenet-dev/wirenet-manager --ref main
```

Restart the ChatGPT desktop app, choose the WireNet Manager marketplace, and
install the plugin.

## Bootstrap The Local Manager

Start a new task and use:

```text
$wirenet-manager-bootstrap Set up my WireNet Manager in ~/Manager.
```

The skill previews the operation. After approval, it:

1. copies the content-only seed bundled inside the installed plugin;
2. writes `.wirenet/manager.json` and the empty local binding registry;
3. initializes a local Git repository on `main`;
4. creates an initial local commit;
5. configures no remote and performs no cloud sync;
6. requires the Manager doctor to return `ok: true`.

Plugin code is not copied into the Manager. Reinstalling or upgrading the
plugin therefore cannot overwrite personal Project Packs.

## Connect Existing Projects

The bootstrap asks which roots may be inspected. Discovery is shallow and uses
folder names plus lightweight markers such as `.git`, `package.json`,
`pyproject.toml`, and `README.md`. It does not inspect raw media or file bodies.

The user classifies candidates as:

- `project`: create an open Project Pack with `README.md`, `AGENTS.md`, the
  collection route, and an optional local binding; add goal, result, index,
  log, or other concepts only when useful;
- `experiment`: create a lightweight Experiment Pack around a question and
  decision criterion, with an optional local binding;
- `ignored`: remember the path and do not ask again.

Manager-native projects and experiments omit the binding entirely. The user can
work directly in their packet when no external code, media, data, or operational
folder is needed. Externally bound and Manager-native packets otherwise follow
the same knowledge contract.

UltraGoal is installed with the plugin but cannot be invoked implicitly. It is
available only when the user explicitly names or activates a persistent goal;
only then may it create or update `WORKLOG.md`.

## Install Global Guidance

After approval, the bootstrap adds a core managed block to the user's global
Codex `AGENTS.md`. It invokes `$wirenet-manager-sync` only when a future task
would otherwise misunderstand durable project state.

The block is conditional on the skill being installed and enabled. Disabling
the plugin therefore stops reconciliation without blocking ordinary tasks; the
managed block can also be removed explicitly during uninstall.

A second managed block for workspace routing is optional. Bootstrap offers it
only when the user already has a stable convention or explicitly wants one. It
does not impose a folder hierarchy on an unstructured system. Project bindings
continue to work without global routing.

The optional block is the only v0.2 source for those global routing rules; the
same rules are not mirrored into Manager JSON. Existing instructions outside
the managed blocks are preserved, and an equivalent manual routing section is
removed only after the user approves the replacement.

## Update Plugin And Manager Separately

Updating the marketplace or plugin installs newer reusable skills, scripts,
templates, and checks. It does not mutate an already materialized `~/Manager`.
The local workspace records its own schema in `.wirenet/manager.json`.

After a plugin update, invoke `$wirenet-manager-bootstrap`. It previews
`scripts/upgrade_manager.py` before the ordinary health check. A current schema
needs no local write. A supported older schema receives an explicit migration
plan; apply requires approval and a clean local Git checkpoint. The updater
preserves personal Markdown bodies and agent instructions, moves superseded
runtime data into `.wirenet/migrations/`, writes the new deterministic shape,
and requires Doctor `ok: true`. The resulting diff is committed only after it
has been reviewed as the planned structural migration.

If the Manager schema is newer than the installed plugin, update the plugin
first. Unsupported layouts and ambiguous legacy experiment routes stop for
manual review rather than being guessed.

## Business Workspace Boundary

Workspace admins may control plugin installation and sharing. WireNet Manager
can be installed from a marketplace without giving WireNet membership in a
customer's ChatGPT workspace. Customer-private capability plugins remain
separate and are installed by an authorized workspace member.
