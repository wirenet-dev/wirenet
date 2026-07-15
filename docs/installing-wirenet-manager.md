---
last_edited: 2026-07-15
---

# Installing WireNet Manager v0.2

## Fast Start With An Appshot

The public README is also the clean-install contract. Open the repository page,
press both Command keys to attach an Appshot to a new Codex task, and say:

```text
Set me up with wirenet-dev/wirenet-manager as ~/Manager. Read the repository README first, install WireNet Manager from its marketplace, then run the guided first-time bootstrap. Preview system changes and ask before connected services, global instructions, durable memory, or automations.
```

This works from a task with no selected project and an empty global `AGENTS.md`.
It does not assume an existing WireNet skill. The first task reads the public
contract, previews the marketplace and plugin commands, and installs only after
approval. Because newly installed plugins become available to fresh tasks,
restart ChatGPT if requested and continue in a new task with:

```text
$wirenet-manager-bootstrap Start my guided first run.
```

The restart boundary is intentional. An Appshot can carry the visible GitHub
page and its text into a task, but it does not install a plugin by itself.

## Distribution

WireNet Manager is distributed through a Codex plugin marketplace from
[`wirenet-dev/wirenet-manager`](https://github.com/wirenet-dev/wirenet-manager).
Users do not clone the product repository into `~/Manager` and do not need to
work with GitHub themselves.

During local development, the repository marketplace is
`.agents/plugins/marketplace.json`. After publication, add it with:

```sh
codex plugin marketplace add wirenet-dev/wirenet-manager --ref main
codex plugin add wirenet-manager@wirenet-manager
```

Restart the ChatGPT desktop app when requested, then start the guided first run.

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

After the workspace is healthy, bootstrap checks QMD separately. It previews
registration of `~/Manager` as `qmd://manager/`. If QMD is missing or unhealthy,
the user can approve installation or repair of the pinned tested package. QMD
configuration remains outside the Manager and does not enter its Git history.

The initial collection indexes Manager knowledge lexically while excluding
runtime `AGENTS.md`, hidden state, and `outputs/`. Semantic embeddings are an
additional opt-in because they may download local models. QMD is not required:
the Manager continues through canonical indexes and direct Markdown reads when
retrieval is unavailable.

Plugin code is not copied into the Manager. Reinstalling or upgrading the
plugin therefore cannot overwrite personal Project Packs.

## Guided First Run

The first run should feel like a useful first conversation, not a filesystem
wizard. After the deterministic workspace checks, the Manager:

1. asks what is currently on the user's plate and returns a compact work map;
2. asks for corrections before proposing any durable Manager content;
3. inspects which communication and work-source plugins are already available;
4. recommends only sources that match the user's actual work, such as email,
   messages, calendar, files, or repositories;
5. asks separately before installing or connecting a service, reading it for
   onboarding, or writing inferred durable context;
6. discovers only explicitly approved project roots and classifies relevant
   folders as projects, experiments, or ignored;
7. explains how Manager work, external project work, global reconciliation,
   QMD retrieval, and the Inspector fit together;
8. offers to keep the current task as the Manager home and create one quiet
   recurring check-in there.

The default check-in recommendation is hourly and silent unless a meaningful
new ask, deadline, blocker, decision, or dropped follow-up appears. It reads the
current stack and relevant packets, checks only approved connected sources, and
does not send messages, change meetings, edit shared files, or write inferred
memory. The user may choose another cadence or decline it. Local scheduled work
requires the computer and ChatGPT desktop app to be running.

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
