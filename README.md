---
last_edited: 2026-06-15
---

# Personal Monorepo

A starter workspace for Codex. It gives the AI a simple map of your work: projects, experiments, people, repo-local skills, and Assistant onboarding.

Canonical repo: `jxnl/personal-monorepo-template`.

The point is simple: Codex should know where to look before it acts. Work lives under `projects/` or `experiments/`; durable context about collaborators lives under `people/`; repeatable agent behavior lives under `.codex/skills/`.

## Install

Install the current packaged version:

```sh
curl -L https://github.com/jxnl/personal-monorepo-template/releases/download/v0.1.0/personal-monorepo-template-v0.1.0.zip -o /tmp/personal-monorepo-template-v0.1.0.zip
ditto -x -k /tmp/personal-monorepo-template-v0.1.0.zip ~
```

That creates:

```text
~/personal-monorepo
```

The zip is created by the `Package template` GitHub Action when a version tag is pushed. For version `v0.1.0`, the release asset is `personal-monorepo-template-v0.1.0.zip`.

Then open Codex, create a new project, and set the project root to:

```text
~/personal-monorepo
```

Create a new thread inside that Codex project and start onboarding:

```text
$onboarding
```

That is the main entry point. Onboarding reads the workspace, summarizes what it found, asks for missing project and people context, recommends plugins, then offers any setup actions.

## Start Here

1. Install the template into a root directory.
2. Create a Codex project that starts in that directory.
3. Create a thread inside the project.
4. Run `$onboarding`.
5. Tell Assistant what projects exist, what matters, who matters, and which tools you use.

After that, use Codex normally. The structure gives each future thread enough local context to understand the workspace.

## Assistant Onboarding

Use onboarding when setting up this workspace for the first time.

Run:

```text
$onboarding
```

It covers:

- projects and experiments in this workspace
- people or agents Codex should know about
- plugins and connectors to install
- thread automations for recurring checks
- optional shared-memory setup

Use `.codex/skills/assistant` after onboarding when:

- you ask what you should know right now
- you want help preparing for a meeting, project, or week
- you want likely follow-ups, missed commitments, or useful reply drafts
- you want Assistant to keep you caught up without turning every check into noise

Assistant is draft-first. It should not send messages, change meetings, edit shared documents, create automations, or write shared memory without explicit approval for that specific action.

During onboarding, Assistant should explain what it is checking before it checks it, then show the result. It should ask before setup actions.

Setup options:

- main Assistant check-in for the current thread
- pinned daily chief-of-staff threads for major workstreams
- thread names such as `Chief of Staff: Today`, `Chief of Staff: <Project>`, and `Chief of Staff: People`
- daily loop for each approved chief-of-staff thread
- shared-memory vault for durable context outside one chat

Thread automation lets Codex resume a thread on a schedule. Use it for daily planning, project drift, follow-ups, and meeting prep. Assistant should ask before creating, pinning, renaming, or looping any thread.

## Installing Codex Plugins

Skills in this repo are local instructions. Plugins are Codex app capabilities that may add tools, connectors, assets, or account-backed access.

Install plugins before or during onboarding. Plugins are important because they decide what Assistant can actually inspect.

1. Open Codex and go to the Plugins or Marketplace area.
2. Install the plugins for the tools where your work happens.
3. Install or enable the plugin.
4. Complete any sign-in or connector authorization flow the plugin asks for.
5. Return to the onboarding thread and tell Assistant what is connected.

Good first plugins:

- Assistant
- Gmail or Outlook Email
- Google Calendar or Outlook Calendar
- Google Drive, Notion, Documents, Spreadsheets, Presentations, or PDF
- Slack or Teams
- GitHub, Linear, or Notion for project tracking
- Browser
- Chrome
- Computer Use

You do not need everything installed. Start with the tools where real work happens. During onboarding, Assistant should ask what projects exist, what matters right now, and which plugins or connectors are missing before recommending more installs.

For browser/account workflows:

1. Enable Computer Use in Codex.
2. Install the Chrome plugin in Codex.
3. Install the [Codex Chrome Extension](https://chromewebstore.google.com/detail/codex/hehggadaopoacecdllhhajmbjkdcmajg).
4. Open Chrome, sign in where needed, and approve site access only when Codex asks for a specific task.

The Chrome extension lets Codex work in Chrome where you are already signed in. The Chrome plugin and the extension are both needed for that flow.

Repo-local plugin material under `.codex/plugins/` is for carrying metadata and assets with this repository. It does not replace installing or authorizing account-backed plugins in Codex.

## Choosing Skills

Repo-local skills live under `.codex/skills/`. Read the relevant `SKILL.md` before using a skill.

- `assistant`: ongoing work support after the first meeting.
- `onboarding`: first-meeting setup for Assistant, active-project discovery, plugin readiness, and shared memory.
- `loop`: recurring heartbeat checks on the current Codex thread.
- `new-project`: create a durable project or experiment folder.
- `new-person`: create a public-safe note under `people/`.
- `ultragoal`: define or run a long-running objective with verifiers and completion proof.
- `simple-html-artifact`: build a clean single-file HTML artifact or report.
- `audit-ai-code`: clean up AI-shaped backend or general implementation code.
- `audit-ai-frontend`: review or de-slop AI-shaped UI code and screenshots.
- `audit-ai-writing`: tighten AI-shaped docs, drafts, Markdown, or source-backed writing.
- `gh-address-comments`: inspect and address actionable GitHub PR review comments.
- `gh-fix-ci`: debug failing GitHub Actions checks.
- `gh-commit`: split local changes into intentional commits.
- `yeet`: publish local changes to GitHub and open a draft PR.

If multiple skills seem relevant, start with the one closest to the user's intent. For example, start with `onboarding` before `assistant` in a new Assistant relationship, and use `loop` only when the work genuinely benefits from coming back later.

## Structure

- `projects/` holds long-lived work.
- `experiments/` holds short-lived spikes named `exp-<topic>-YYYY-MM-DD`.
- `archive/` holds paused or completed work.
- `docs/` holds repo-level references.
- `outputs/` holds generated artifacts that are not source of truth.
- `people/` holds durable notes about humans and agents.
- `.codex/` holds repo-local skills, plugin metadata, and assets.
- `templates/` holds starter files for new work.
- `scripts/` holds helper scripts.

## Agent Assets

This repo keeps skills in place. It does not install them into global Codex, Claude, or Cursor state.

Useful local skills live under `.codex/skills/`.

When adding or updating a skill, keep its `SKILL.md` frontmatter simple: `name`, `description`, and `last_edited`.

## Public-Safe Notes

This template intentionally avoids private personal data. Treat files under `people/` as lightweight working context, not a secrets vault or CRM export.
