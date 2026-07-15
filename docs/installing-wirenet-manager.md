---
last_edited: 2026-07-15
---

# Installing WireNet Manager v0.1

## Distribution

WireNet Manager is distributed through a Codex plugin marketplace. The public
repository may be hosted on GitHub, but users do not clone it into `~/Manager`
and do not need to work with GitHub themselves.

During local development, the repository marketplace is
`.agents/plugins/marketplace.json`. After publication, add it with:

```sh
codex plugin marketplace add wirenet-dev/wirenet-manager --ref main
```

This command becomes valid only after the repository is published under that
name. Restart the ChatGPT desktop app, choose the WireNet Manager marketplace,
and install the plugin.

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

- `project`: create a four-file Project Pack and a local binding;
- `experiment`: remember the path without creating a full packet;
- `ignored`: remember the path and do not ask again.

## Install Global Guidance

After approval, the bootstrap adds a core managed block to the user's global
Codex `AGENTS.md`. It invokes `$wirenet-manager-sync` only when a future task
would otherwise misunderstand durable project state.

A second managed block for workspace routing is optional. Bootstrap offers it
only when the user already has a stable convention or explicitly wants one. It
does not impose a folder hierarchy on an unstructured system. Project bindings
continue to work without global routing.

The optional block is the only v0.1 source for those global routing rules; the
same rules are not mirrored into Manager JSON. Existing instructions outside
the managed blocks are preserved, and an equivalent manual routing section is
removed only after the user approves the replacement.

## Business Workspace Boundary

Workspace admins may control plugin installation and sharing. WireNet Manager
can be installed from a marketplace without giving WireNet membership in a
customer's ChatGPT workspace. Customer-private capability plugins remain
separate and are installed by an authorized workspace member.
