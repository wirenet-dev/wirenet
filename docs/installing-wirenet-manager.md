---
last_edited: 2026-07-20
---

# Installing wirenet manager v0.2

> **Status (2026-07-21):** This document describes the v0.2 install flow and
> is superseded on the `v0.5-core` branch (one plugin `wirenet`, two skills).
> [`core-contract.md`](core-contract.md) governs; the rewrite lands with the
> README station.

## Fast Start With An Appshot

The public README is also the clean-install contract. Open the repository page,
keep its Fast Start section visible, press both Command keys to attach an
Appshot to a new Codex task, and say only:

```text
Set me up.
```

Use `Richte das für mich ein.` to begin in German. The request language selects
conversation and new human-readable Manager prose; stable system structure and
metadata remain English. If the language is ambiguous, bootstrap asks once.

This works from a task with no selected project and an empty global `AGENTS.md`.
It does not assume an existing wirenet skill. The first task reads the public
contract, previews the marketplace and plugin commands, and installs only after
approval. Because newly installed plugins become available to fresh tasks,
restart ChatGPT if requested and continue in a new task with:

```text
$manager-setup Set up my local Manager, then continue with onboarding.
```

The restart boundary is intentional. An Appshot can carry the visible GitHub
page and its text into a task, but it does not install a plugin by itself.

## Distribution

wirenet Manager is distributed through a Codex plugin marketplace from
[`wirenet-dev/wirenet`](https://github.com/wirenet-dev/wirenet).
Users do not clone the product repository into `~/Manager` and do not need to
work with GitHub, Git, Python, Node.js, or a terminal themselves. A public
marketplace needs no GitHub account; the installing agent runs the approved
marketplace commands. A Business workspace may instead have an administrator
add the plugin once for workspace members.

During local development, the repository marketplace is
`.agents/plugins/marketplace.json`. After publication, add it with:

```sh
codex plugin marketplace add wirenet-dev/wirenet --ref stable
codex plugin add manager@wirenet
```

Restart the ChatGPT desktop app when requested, then start the technical setup
and personal first meeting.

The same marketplace also offers two optional cross-project plugins:

```sh
codex plugin add workflows@wirenet
codex plugin add content-tools@wirenet
```

They are deliberately not prerequisites for Manager bootstrap. Customer-private
plugins remain separate marketplaces and Developer-only skills remain local to
their repositories.

## Bootstrap The Local Manager

Start a new task and use:

```text
$manager-setup Set up my wirenet manager in ~/Manager.
```

The skill previews the operation. After approval, it:

1. resolves Python and Git from the bundled Codex workspace runtime when
   available, then from the existing system `PATH`;
2. stops without writing if the required local runtime is unavailable;
3. copies the content-only seed bundled inside the installed plugin;
4. writes `.wirenet/manager.json` and the empty local binding registry;
5. initializes a local Git repository on `main` through the resolved Git path;
6. creates an initial local commit;
7. configures no remote and performs no cloud sync;
8. requires the Manager doctor to return `ok: true`.

After the workspace is healthy, bootstrap checks QMD separately. It previews
registration of `~/Manager` as `qmd://manager/`. If QMD is missing or unhealthy,
the user can approve installation or repair of the pinned tested package through
resolved `npm` or bundled `pnpm`. Because QMD officially targets npm, the pnpm
fallback first bootstraps a pinned npm in a dedicated user-local wirenet
directory, then uses it to install QMD with the required native build scripts.
It does not alter shell startup files. QMD configuration remains outside the
Manager and does not enter its Git history.

The initial collection indexes Manager knowledge lexically while excluding
runtime `AGENTS.md`, hidden state, and `outputs/`. Semantic embeddings are an
additional opt-in because they may download local models. QMD is not required:
the Manager continues through canonical indexes and direct Markdown reads when
retrieval is unavailable.

Plugin code is not copied into the Manager. Reinstalling or upgrading the
plugin therefore cannot overwrite personal Project Packs.

When this technical baseline is healthy, bootstrap hands the same task to
`$manager-setup`. It does not treat a Doctor report as completed
personal onboarding.

## Personal First Meeting

The onboarding should feel like a useful first conversation, not a filesystem
wizard. It follows Jason Liu's sequence as closely as wirenet's explicit source
approvals allow:

1. opens with `Hi, I'm your Manager.` or its selected-language equivalent;
2. reads existing local Manager and task context and shows a first map when
   grounded context exists;
3. when context is thin, asks what is currently on the user's plate;
4. interviews one open question at a time for corrections, active work,
   near-term importance, dropped-ball patterns, important people, project
   locations, and missing source capabilities;
5. after each answer, explains and requests any useful targeted connected-source
   read, then updates the map rather than producing a generic digest;
6. asks separately before installing or connecting a service, reading a named
   scope, or writing inferred durable context;
7. starts source discovery with a small recent high-signal window and widens
   selectively, using roughly 90 days only when recurring durable evidence
   warrants it rather than importing a fixed mailbox period;
8. optionally proposes a typed `docs/communication-and-files.md` when confirmed
   cross-project accounts, file surfaces, or source boundaries deserve a durable
   map; it never seeds an empty placeholder or raw mail archive;
9. discovers only explicitly approved project roots and classifies relevant
   folders as projects, experiments, or ignored;
10. proposes one core current-task Manager check-in, optionally extending that
    same heartbeat with hourly semantic commits and safe push windows around
    09:00 and 16:00 after separate approvals, then offers only those additional
    project, people, or daily monitor tasks that reduce noise;
11. detects an existing global or approved repo-local `write-like-me` profile
    before offering migration, refresh, or a fresh approved sent-message scan;
12. explains shared memory and daily use, offers to rename or pin the Manager
    task, and closes with `You can just talk to your Manager now.`

The default check-in recommendation is hourly and silent unless a meaningful
new ask, deadline, blocker, decision, or dropped follow-up appears. It reads the
current stack and relevant packets, checks only approved connected sources, and
does not send messages, change meetings, edit shared files, or write inferred
memory. The user may choose another cadence or decline it. Local scheduled work
requires the computer and ChatGPT desktop app to be running.

For a Git-tracked Manager, onboarding recommends one-chat continuity: the same
hourly heartbeat can be separately authorized to group coherent approved
Manager changes into semantic commits and to push safely during its 09:00 and
16:00 local-hour runs. It must require a clean `main`, an explicitly approved
private remote, and fast-forward-only history. A standalone push automation is
an opt-in alternative for users who value exact clock scheduling over keeping
all Manager activity in one task.

## Connect Existing Projects

Onboarding asks which roots may be inspected. Discovery is shallow and uses
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

UltraGoal is installed through `workflows@wirenet`, not Manager core, and cannot
be invoked implicitly. It is available only when the user explicitly names or
activates a persistent goal; only then may it create or update `WORKLOG.md`.

## Install Global Guidance

During approved onboarding setup, the bootstrap helper adds a core managed
block to the user's global
Codex `AGENTS.md`. It invokes `$manager` only when a future task
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

Manager Doctor can perform an explicit read-only release check:

```sh
python3 plugins/manager/scripts/manager_doctor.py \
  --manager-dir ~/Manager \
  --check-updates
```

It compares the installed plugin manifest with the latest published GitHub
Release and returns up to three user-facing release-note bullets. Manager uses
that result during the first check-in of a fresh task, stays quiet when current,
and asks before running the returned update command. Existing Codex users update
the stable Marketplace with:

```sh
codex plugin marketplace upgrade wirenet
```

They then start a fresh task and invoke `$manager-setup`. The setup skill reports
the installed version, packaged release notes, whether a workspace migration was
needed, and the final Doctor result.

After a plugin update, invoke `$manager-setup`. It previews
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

The metadata fields have distinct responsibilities:

- `schema_version` selects and validates workspace migrations.
- Workspace `plugin_version` records the plugin version that created or last
  structurally migrated that workspace; a behavior-only plugin update does not
  rewrite it.
- The active installed version comes from the plugin manifest and is the value
  compared with the latest GitHub Release.

## Business Workspace Boundary

Workspace admins may control plugin installation and sharing. wirenet Manager
can be installed from a marketplace without giving wirenet membership in a
customer's ChatGPT workspace. Customer-private capability plugins remain
separate and are installed by an authorized workspace member.
