# Inventory: `.codex/skills/onboarding/` (jxnl/personal-monorepo-template, `upstream/main`)

## File listing (complete)

```
.codex/skills/onboarding/
├── SKILL.md
├── agents/openai.yaml
├── references/first-meeting-flow.md
├── references/question-bank.md
├── references/shared-memory-vault.md
├── references/starter-capabilities.md
└── scripts/
    ├── new_person_note.py
    ├── new_project_note.py
    └── setup_shared_memory_vault.py
```

Note: the assignment mentioned only three references; there is a fourth (`question-bank.md`) plus a third script (`new_person_note.py`) and an `agents/openai.yaml` interface manifest. All covered below. All markdown files carry frontmatter `last_edited: 2026-06-15`.

---

## 1. `SKILL.md`

**Function:** Entry-point skill that runs the "first meeting" between the user and the Assistant persona — builds a work map, interviews the user, offers check-ins/monitor threads/write-like-me/shared-memory vault, and closes with rename/pin guidance and a recap.

**Conventions/rules established:**
- Frontmatter: `name`, `description` (with explicit trigger phrases including `"$onboard me"`), `last_edited`. The description itself encodes a hard output constraint: "The first user-visible sentence must be exactly 'Hi, I'm your assistant.'"
- Progressive disclosure: "Read First" mandates `references/first-meeting-flow.md`; the other three references are "Use only as needed".
- **Setup-state model** — classify *quietly* (never announced to the user) into three states:
  - `brand_new`: no useful Assistant baseline → run the full first meeting.
  - `partial`: some context exists but projects/priorities/people/plugins/memory/threads/check-ins are missing → fill only the gaps.
  - `established`: useful baseline exists → skip onboarding entirely and just help.
- **Full flow (9 numbered steps):** (1) exact hello → (2) build grounded work map from available context → (3) interview for corrections, active projects, what matters, stress points, important people, missing plugins/connectors → (4) propose the one core Assistant check-in → (5) offer monitor threads for selected projects/people/daily updates, default check-in times 9:00 AM and 4:00 PM in the user's timezone → (6) after Slack/email scans, suggest `write-like-me-bootstrap` → (7) offer the shared-memory vault → (8) tell user how to rename and pin the chat → (9) short recap ending `You can just talk to me now.`
- **Approval gates** (blanket list): ask before sending messages, changing meetings, editing shared docs, creating automations, installing plugins, creating/pinning/renaming threads, adding loops, or writing shared memory.
- **Vault default:** the monorepo root *is* the vault; never create a nested `vault/` dir or default to `~/vault` unless explicitly asked. After connector scans, proactively *propose* specific `people/*.md`, project packets, and `AGENTS.md` updates; write only after approval. Ask before deep-scanning for writing style, and ask again before writing the generated skill.
- **Definition of done:** onboarding is complete only when every offer (map, interview, plugin gaps, check-in, monitor threads, write-like-me, shared memory, rename/pin, recap) is "handled, declined, or unavailable."
- Turn discipline: "Every turn should end with a clear question, next step, setup offer, or final recap."

**Quotable phrases:**
- "Hi, I'm your assistant."
- "Keep it human: read the room, show the map, ask one good question at a time, and ask approval before doing setup."
- "Classify quietly"
- "You can just talk to me now."
- "handled, declined, or unavailable"
- "Do not create a nested `vault/` directory or default to `~/vault` unless the user explicitly asks for a separate location."

**Dependencies:** `references/first-meeting-flow.md` (required read); `references/question-bank.md`, `references/starter-capabilities.md`, `references/shared-memory-vault.md` (as needed); sibling skill `.codex/skills/write-like-me-bootstrap`; the repo root's `AGENTS.md` / `people/` / `projects/` structure (created by `scripts/setup_shared_memory_vault.py`).

---

## 2. `agents/openai.yaml`

**Function:** Interface manifest exposing the skill to an OpenAI/Codex agent surface.

**Conventions:** Three fields: `display_name: "Assistant Onboarding"`, `short_description: "Meet Assistant and set up useful work memory."`, `default_prompt: "Help me get started with Assistant."`

**Quotable:** "Meet Assistant and set up useful work memory."

**Dependencies:** None (metadata for the skill itself).

---

## 3. `references/first-meeting-flow.md`

**Function:** The step-by-step choreography of the first meeting, expanding SKILL.md's 9-step flow into 6 phases.

**Choreography, step by step:**
1. **Hello** — exact string `Hi, I'm your assistant.`, then briefly say you will learn the user's work and where you can help.
2. **Setup State** — decide quietly among `brand_new` / `partial` / `established` by checking: chat context, repo docs, connected tools, existing check-ins, existing threads, and any real memory or vault surface. Repeats the repo-root-is-vault rule.
3. **First Map** — read before asking the user to steer. Return a concise map covering: who the user seems to be; active projects and workstreams; what matters now; important people and places; useful plugin/connector gaps; what is uncertain; durable files that should likely be created or updated in this repo. "If context is thin, say so and begin the interview."
4. **Interview** — one open question at a time, covering: what you got wrong; active/paused/background/ignored work; what matters soon; stress and dropped-ball patterns; important people; missing plugins/connectors. "Use each answer to update the map and, when tools are available, do a targeted reread."
5. **Setup Offers** — only "after enough calibration": one core check-in and what it watches; monitor threads (daily/people/project) with 9:00 AM & 4:00 PM defaults; write-like-me-bootstrap "when Slack and email scans include enough authored messages to infer the user's writing postures"; the vault ("this repo is the vault and will be updated in place"); the specific people files/project packets/agent instructions derived from scans + interview. Explicit approval before automations, threads, loops, installs, or memory files. Includes a canned write-like-me pitch (see quotes).
6. **Close** — rename/pin guidance and a recap under fixed bold headings: `**Here Is The Map I Am Carrying**`, `**How I Will Help**`, `**What I Set Up**`, `**Shared Memory**`, `**Keep This Handy**`, `**You Can Just Talk To Me Now**`.

**Rules established:** anti-wizard tone; read-before-ask; one question at a time; calibration precedes offers; a completed close never ends on a config question.

**Quotable phrases:**
- "Make this feel like a capable assistant saying hello, not a setup wizard."
- "When context exists, read before asking the user to steer."
- "If context is thin, say so and begin the interview."
- "Do not end completed onboarding with another configuration question."
- "I can also bootstrap a write-like-me skill from your sent email and Slack messages, split by posture like quick replies, pushback, delegation, intros, and status updates. Want me to do that?"
- "**Here Is The Map I Am Carrying**" / "**You Can Just Talk To Me Now**"

**Dependencies:** Referenced by SKILL.md as mandatory; hands off to `question-bank.md` (interview wording), `starter-capabilities.md` (offers), `shared-memory-vault.md` (vault offer), and `write-like-me-bootstrap` skill.

---

## 4. `references/question-bank.md`

**Function:** The exact interview questions and per-answer loop discipline.

**Conventions/rules:**
- "Ask one question at a time. Do not use menus or reply codes."
- Fixed interview opener block:
  ```md
  **Your Interview Starts Here**

  I am going to ask a few open questions, one at a time. Rambling is welcome; I will do the cleanup.

  **First Question For You**
  ```
- Six core questions (verbatim, in order):
  1. "What did I misunderstand or underweight about your role, your work, or the people around you?"
  2. "What projects or workstreams are active right now, paused, background, or safe to ignore unless you bring them up?"
  3. "What feels most important over the next few days or weeks?"
  4. "What usually creates stress, dropped balls, or mental overhead?"
  5. "Who should I learn especially well, and what should I understand about how you work with them?"
  6. "Which tools should I have connected to be useful here, and what feels missing?"
- After each answer: say what changed in your understanding; reread connected context when useful; ask the next still-missing question.
- "Save durable memory only after the user has calibrated the map and only through a real memory or vault surface."

**Quotable phrases:**
- "Rambling is welcome; I will do the cleanup."
- "ask the next still-missing question"
- "safe to ignore unless you bring them up"
- "stress, dropped balls, or mental overhead"

**Dependencies:** Consumed during step 4 of first-meeting-flow; its "real memory or vault surface" rule points at shared-memory-vault.md.

---

## 5. `references/shared-memory-vault.md`

**Function:** Defines what the shared-memory vault is, its shape, its inclusion/exclusion rules, and the exact setup procedure and user-facing pitch.

**Conventions/rules:**
- "The vault is optional plain-file memory for durable work context outside one chat."
- Default path = the personal monorepo root containing the skill; repo-root-is-vault rule restated a third time.
- Default shape:
  ```
  personal-monorepo/
  |-- AGENTS.md
  |-- TODO.md
  |-- agent/
  |   `-- USER_CONTEXT.md
  |-- people/
  |-- projects/
  |-- notes/
  `-- sources/
  ```
- Use it for: the user's working profile; durable projects and workstreams; important people; open loops and decisions; "source routes future Assistant chats should know."
- Do NOT use it for: "raw email/chat dumps, one-off names, weak guesses, or activity logs."
- Setup procedure (5 steps): explain in one short paragraph → ask before creating/extending → if approved, run `../scripts/setup_shared_memory_vault.py` (no `--vault-dir` unless user chose a different root) → personalize `AGENTS.md` and `agent/USER_CONTEXT.md` → mention the path in the final recap.
- If vault files already exist: "inspect them first and preserve their structure. Extend the existing repo in place instead of creating another vault root."
- Canned user-facing explanation block (see quote).

**Quotable phrases:**
- "This chat is where we talk. The check-in is what brings me back. The vault is the plain-file memory I maintain so durable work context does not live only inside one chat."
- "Want me to set that up?"
- "raw email/chat dumps, one-off names, weak guesses, or activity logs"
- "Extend the existing repo in place instead of creating another vault root."

**Dependencies:** Invokes `scripts/setup_shared_memory_vault.py`; describes the target structure that `new_person_note.py` / `new_project_note.py` populate; used in step 5/7 of the flow.

---

## 6. `references/starter-capabilities.md`

**Function:** Menu-discipline for what automation to offer after calibration: one check-in, a few monitor lanes, and concrete help defaults.

**Conventions/rules:**
- "Recommend from the user's actual map, not a generic menu."
- One core hourly check-in, with canned pitch:
  ```md
  Every hour, I will check the workstreams, people, messages, meetings, and loose ends we identified. If something matters, I will bring it here. If nothing useful changed, I will stay quiet.
  ```
  "Say what it will watch. Ask before creating or changing it."
- Monitor threads — "Offer separate daily lanes only when they reduce noise": `Daily Update Monitor` (broad daily scan across work, meetings, messages, and open loops); `People Monitor` (relationship follow-ups, replies, important people context); `Project Monitor: <Project>` (selected active projects needing their own thread).
- "Do not create a chief-of-staff thread for every workstream. Use that label only when the user asks for it or when a workstream truly needs broad coordination." Create/rename/pin/loop only after approval.
- Specific-help defaults once calibrated: reply drafts in the user's tone; meeting prep; open-loop maps; what-changed briefs; follow-up and prep-gap checks.

**Quotable phrases:**
- "If something matters, I will bring it here. If nothing useful changed, I will stay quiet."
- "Offer separate daily lanes only when they reduce noise."
- "Do not create a chief-of-staff thread for every workstream."
- "open-loop maps", "what-changed briefs", "prep-gap checks"

**Dependencies:** Feeds steps 4–5 of the flow; monitor-thread defaults (9 AM / 4 PM) live in SKILL.md/first-meeting-flow, not here.

---

## 7. `scripts/setup_shared_memory_vault.py`

**Function:** Idempotent scaffolder that creates the vault directories and seed files at the repo root, printing a JSON result.

**Behavior:**
- `default_vault_dir()` = `Path(__file__).resolve().parents[4]` — four levels up from the script, i.e. the monorepo root above `.codex/skills/onboarding/scripts/`. `--vault-dir` overrides; `--dry-run` reports without writing.
- Creates dirs (only if missing): `agent/`, `people/`, `projects/`, `notes/`, `sources/`.
- Creates files (only if missing, never overwrites): `AGENTS.md`, `TODO.md`, `agent/USER_CONTEXT.md`, `projects/README.md`, `projects/AGENTS.md`.
- Prints JSON: `{ok, dry_run, vault_dir, created_dirs, created_files, next_steps}` with next_steps: "Personalize AGENTS.md and agent/USER_CONTEXT.md from the calibrated first meeting."; "Propose initial person notes and project packets, then create only explicitly approved items."; "Treat sources/ as read-only by default when retaining imported evidence."

**Embedded templates (the real payload):**

- **`ROOT_AGENTS_TEMPLATE`** (root `AGENTS.md`) — sections:
  - *Shared Memory Goal*: "Treat this vault as durable work memory for the user." / "It is not a transcript dump and it is not a replacement for the user's repos, docs, email, or chat systems." / vault "should make future chats easier to resume from something explicit and reviewable."
  - *User Snapshot*: blank bullets to personalize — User; Role and work context; How they spend their time; What useful help feels like; Important people and spaces to learn first.
  - *Source Order* (evidence hierarchy): 1. existing vault notes and canonical packets → 2. the user's current self-report and corrections → 3. connected work context (messages, email, calendar, docs, project systems) → 4. current chat context and artifacts. Plus: "Use absolute dates. Separate facts, self-report, and inference when that distinction changes how future work should read the note."
  - *Writing Rules*: "Preserve durable meaning, not activity logs." / "Prefer updating existing canonical notes before creating adjacent notes." / route TODOs/people/projects/daily summaries/scratch explicitly / preserve decisions, blockers, owners, dates, useful links, open loops / people notes keep confirmed Slack handles, emails, teams, relationship context, collaboration guidance, dated evidence / project packets: owners and open loops in `README.md`, recurring routes in nearest `AGENTS.md` / no raw dumps, secrets, or noisy transcripts / no external actions without explicit approval of "that specific action" / "If nothing meaningful changed, do not churn the vault."
  - *Vault Conventions*: role of each path (`AGENTS.md` = "root operating guide"; `TODO.md` = "vault-wide list for cross-workstream follow-ups"; `agent/` = user context, daily summaries, agent-authored syntheses; `people/` = recurring collaborators; `projects/` = "rolling workstream packets"; per-project README = durable state, per-project AGENTS.md = "recurring source and routing instructions"; `notes/` = "durable scratch notes that do not yet belong in a person or project note"; `sources/` = "retained imported evidence and source material; treat it as read-only by default").
  - *Where To Write*: exact routing table — `agent/USER_CONTEXT.md`; `agent/daily-summary-YYYY-MM-DD.md`; `TODO.md`; `people/<person>.md`; `projects/<project>/README.md`; `projects/<project>/AGENTS.md`; `notes/`; `sources/`.
  - *Update Thresholds*: update root AGENTS.md only for durable operating preferences/routing rules; project AGENTS.md when recurring sources become "meaningfully clearer"; person notes when relationship/role/ownership/guidance becomes meaningfully clearer; packets when "the source of truth, status, blocker, owner, decision, or open loop changes"; TODO.md "when a follow-up should survive beyond one chat or one project note"; "Keep weak guesses tentative until the user confirms them or repeated evidence supports them."
- **`TODO_TEMPLATE`**: Purpose ("cross-workstream follow-ups and open loops that should not live only inside one chat") + empty `## Active` / `## Waiting` / `## Completed`.
- **`USER_CONTEXT_TEMPLATE`** (`agent/USER_CONTEXT.md`): "This note is Assistant's durable working profile for the user." Sections: Snapshot (User / Role and work context / How they spend their time); Important People And Spaces; Workstreams; Stress And Attention Patterns; How Assistant Should Help; Action Boundaries — "Draft or propose first. Act only after the user explicitly approves that specific external or shared action."
- **`PROJECTS_README_TEMPLATE`** (`projects/README.md`): "This folder holds pages for ongoing projects." / "Prefer one page per project over scattered status notes." / `## Active packets` heading (the anchor `new_project_note.py` depends on).
- **`PROJECTS_AGENTS_TEMPLATE`** (`projects/AGENTS.md`): structure of the packet system (README indexes packets; `<project>/README.md` holds durable state, decisions, blockers, open loops, evidence links; `<project>/AGENTS.md` holds recurring sources and update-routing) and defaults: "Prefer updating an existing canonical packet over creating an adjacent status note." / recurring Slack/DM/email/doc/meeting/repo inputs in nearest AGENTS.md / current status and one-off evidence links in README / "Use absolute dates and label inference when it matters."

**Quotable phrases:**
- "Preserve durable meaning, not activity logs."
- "If nothing meaningful changed, do not churn the vault."
- "Prefer one page per project over scattered status notes."
- "Draft or propose first."
- "Keep weak guesses tentative until the user confirms them or repeated evidence supports them."
- "Use absolute dates and label inference when it matters."
- "It is not a transcript dump."

**Dependencies:** Invoked by shared-memory-vault.md step 3; creates the `projects/README.md` with `## Active packets` that `new_project_note.py` requires; parent-directory math (`parents[4]`) hard-codes the skill's depth in the repo.

---

## 8. `scripts/new_project_note.py`

**Function:** Creates one project packet (`projects/<slug>/README.md` + `projects/<slug>/AGENTS.md`) and registers it in the `projects/README.md` router under `## Active packets`, printing a JSON result.

**Behavior/conventions:**
- Args: `--vault-dir` (same `parents[4]` default), `--title` (required), `--slug` (optional; defaults to normalized title — lowercase, non-`[a-z0-9._-]` collapsed to `-`), `--dry-run`.
- Guard rails as hard exits: existing packet dir → "Project packet already exists; inspect and update that packet instead"; missing router → "Missing projects list; run vault setup before creating project packets"; router without the `## Active packets` heading → "does not contain '## Active packets'; inspect the nonstandard router before writing."
- Router entry format: `- [[projects/<slug>/README|<Title>]]` (Obsidian-style wikilink), inserted directly after the `## Active packets` line; duplicate entries silently skipped.
- **Packet README template**: YAML frontmatter (`title`, `status: "active"`, `owner:`, `created_at`, `updated_at`, `tags: [project]`) + sections `## Purpose`, `## Current Status` ("Replace with the latest durable status, dated when timing matters."), `## People` ("owners, decision makers, collaborators, and links to canonical people notes"), `## Open Loops` ("pending decisions, blockers, and follow-ups"), `## Sources` ("Add direct evidence links with absolute dates."), `## Update History` (seeded with `- \`<date>\`: Created project packet.`).
- **Packet AGENTS.md template**: `## Purpose` ("This packet tracks `<title>` as a canonical workstream."), `## Canonical Files`, `## Recurring Sources To Revisit` (Slack channels/threads; DMs/group DMs; email threads; docs/meetings/repos — each a "Replace with…" stub), `## Update Rules` ("Update `README.md` when durable status, ownership, blockers, decisions, or open loops change." / "Update this file only when recurring sources or packet routing change." / one-off evidence links in README under Sources / absolute dates + label inference).
- JSON output: `{ok, dry_run, packet_path, routing_path, router_path, router_entry, slug}`.

**Quotable phrases:**
- "inspect and update that packet instead"
- "This packet tracks `<title>` as a canonical workstream."
- "Recurring Sources To Revisit"
- "dated when timing matters"

**Dependencies:** Requires `projects/README.md` (with `## Active packets`) created by `setup_shared_memory_vault.py`; implements the packet shape declared in `PROJECTS_AGENTS_TEMPLATE` and the root AGENTS.md routing rules.

---

## 9. `scripts/new_person_note.py`

**Function:** Creates one person-note scaffold at `people/<key>.md`, printing a JSON result.

**Behavior/conventions:**
- Args: `--vault-dir` (same default), `--name` (required, display name), `--key` (optional stable file key; "Prefer a durable handle when known" — normalization strips everything after `@`, so an email becomes its local-part), `--dry-run`.
- Refuses to overwrite: "Person note already exists; update the canonical note instead."
- **Template**: YAML frontmatter (`title`, `usernames: []`, `aliases: []`, `emails: []`, `github_usernames: []`, `teams: []`, `tags: [people]`, `last_seen_at:`, `created_at`, `updated_at`) + sections: `## Snapshot` (Name; "Slack: Replace with handle and user ID when known."; "Email: Replace with a confirmed address when known."; Team/role), `## Why They Matter Now` ("Replace with a short, dated reason this relationship matters."), `## Working Style & Interaction Notes` ("Replace with evidence-backed collaboration patterns."), `## Collaboration Guidance` ("practical guidance for future work with this person"), `## Evidence Log` ("Add dated links to relevant Slack threads or DMs, email threads, docs, meetings, or project notes."), `## Open Questions` (empty).
- JSON output: `{ok, dry_run, path, stable_key}`.

**Quotable phrases:**
- "update the canonical note instead"
- "Why They Matter Now"
- "a short, dated reason this relationship matters"
- "evidence-backed collaboration patterns"
- "Replace with a confirmed address when known."

**Dependencies:** Writes into `people/` (created by `setup_shared_memory_vault.py`, though it will `mkdir` if missing); implements the people-note content rules from `ROOT_AGENTS_TEMPLATE` ("confirmed Slack handles, email addresses, teams, relationship context, collaboration guidance, and dated evidence").

---

## Cross-cutting patterns worth noting

- **Repo-root-is-vault** is stated three times (SKILL.md, first-meeting-flow.md, shared-memory-vault.md) — critical rules are repeated in every file where an agent might arrive without the others.
- **Approval-gate phrasing** is consistent everywhere: propose specifics, act only on "that specific action"; scripts mirror this with `--dry-run` on every one and never-overwrite semantics.
- **Scripts speak JSON**: every script prints a machine-parseable `{ok, dry_run, ...}` result, with human guidance embedded as `next_steps` or error strings that name the correct remedy ("run vault setup", "update the canonical note instead").
- **Calibration before persistence**: the interview must correct the map before any durable write; the setup-state model lets the whole flow degrade gracefully from full ceremony (`brand_new`) to nothing (`established`).
- **Template stubs are self-instructing**: every placeholder starts "Replace with…" and encodes its own quality bar (dated, confirmed, evidence-backed).