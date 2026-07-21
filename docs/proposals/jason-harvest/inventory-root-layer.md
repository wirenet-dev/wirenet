# Root Layer Inventory — jxnl/personal-monorepo-template

## Directory listing: `templates/`

```
templates/GOAL.md
templates/PROJECT_AGENTS.md
templates/RESULT.md
templates/experiment_README.md
templates/project_README.md
```

(No person template under `templates/` — person and agent templates live in `people/person.md` and `people/agent.md`, which serve double duty as live files and templates. `people/README.md` also present; all three inventoried below.)

Every file in this layer carries the same minimal YAML frontmatter — a single `last_edited: 2026-06-15` key and nothing else.

---

## `AGENTS.md` (root)

**Function:** Root-level operating instructions for any agent working in the repo — tone, discovery order, durable-state rules, safety gates, and the repo-local skill index.

**Conventions established:**
- Model policy: "Use the strongest available coding model unless the user or task explicitly calls for a different model."
- Collaboration style: direct, low-ceremony, curiosity before certainty, minor/reversible tradeoffs get a default decision instead of a question, disagreement is named plainly then work proceeds.
- Discovery order: start with `projects/`, `experiments/`, `README.md`; locate the named entity before planning; read the nearest `AGENTS.md` before working in a subdirectory.
- AGENTS.md layering rule: nested files *supplement* root rules; on conflict the more specific local rule wins and the conflict must be mentioned in the summary.
- Durable-state routing table: project status → project `README.md`; long-running objectives → `GOAL.md`; completed work + verification → `RESULT.md`; human/agent collaboration notes → `people/*.md`; cross-project discovery → repo-level docs.
- The repo root *is* the vault; never create a nested `vault/` or separate `~/vault`.
- Vault updates happen only after explicit approval; prefer updating the canonical existing file over creating adjacent notes.
- `projects/` = long-lived, `experiments/` = short-lived spikes.
- New projects/people go through `.codex/skills/new-project` / `new-person` or the templates.
- Safety: no secrets committed; no external side effects (messages, money, orders, deletions, account changes) without explicit approval; blocked validation must be stated explicitly.
- Repo-local skills are "read and used in place", never assumed globally installed.

**Quotable phrases:**
- "direct, practical, low-ceremony, and comfortable with rough edges while the work is still forming"
- "Be curious before being certain. When the request is blurry, ask the smallest useful question that would change the work."
- "Do not ask questions just to avoid making a reasonable call. If the tradeoff is minor or reversible, choose a sensible default and keep moving."
- "Name disagreements plainly and briefly. Offer the better path, explain the reason, and then proceed when the direction is clear."
- "Prefer concrete work over abstract planning. Show progress through edits, checks, and durable notes."
- "Lead with what changed, what was verified, and what still needs attention."
- "Avoid generic assistant voice. Do not over-explain obvious steps, apologize performatively, or pad responses with motivational filler."
- "Do not leave decisions only in chat when they will matter later."
- "Keep important context on disk"
- "This repository is the shared-memory vault."
- "Prefer updating the canonical existing file over creating adjacent notes."
- "Before editing, read enough surrounding context to understand the local pattern."
- "Keep changes small and reversible unless Jason explicitly asks for a larger reshaping."
- "If a request points at a symptom, look one level deeper for the cause before patching."
- "Push back instead of silently complying when the safer or more useful move is different from the literal request."
- "When validation is blocked, say exactly what was not run and why."
- "a place to look before it acts and a place to write important context after you approve it" (echoed in README)
- "Skills in `.codex/skills/` are meant to be read and used in place."

**Dependencies:** References `templates/project_README.md`, `templates/PROJECT_AGENTS.md`, `people/person.md`, `GOAL.md`/`RESULT.md` templates, `TODO.md`, the skill set in `.codex/skills/` (new-project, new-person, assistant, onboarding, loop, gh-*, audit-*, ultragoal, yeet, simple-html-artifact), and nested per-project `AGENTS.md` files.

---

## `README.md` (root)

**Function:** Human-facing setup guide for the vault — what it is, fast/manual setup, plugin installation order, what onboarding does, and the directory map.

**Conventions established:**
- Vault identity: canonical repo `jxnl/personal-monorepo-template`, cloned to `~/vault`, `.git` stripped and re-initialized; "This repo is the vault. Do not create a second `vault/` directory inside it."
- Setup order: install plugins *before* onboarding "so Assistant can read the right context."
- Fast Start is a single natural-language command: "Set me up with jxnl/personal-monorepo-template as ~/vault"; onboarding trigger is "$onboard me".
- Onboarding contract: explain what it checks before checking; read workspace, ask about projects and people, check for missing plugins, offer thread automations and monitors (default 9:00 AM and 4:00 PM check-ins in user timezone), offer `write-like-me` bootstrap from sent Slack/email, propose people/project/AGENTS updates after scanning connectors.
- Broad approval gate: ask before sending messages, changing meetings, editing shared docs, creating automations, thread operations, installing plugins, or writing shared memory.
- Structure map: `projects/` long-lived work, `experiments/` short-lived spikes, `people/` notes about people or agents, `.codex/` skills/plugin metadata/assets, `templates/` starter files, `tests/` "checks for template integrity."

**Quotable phrases:**
- "Starter workspace for giving Codex durable context: projects, people, skills, onboarding, recurring checks, and writing-style memory."
- "This template gives Codex a place to look before it acts and a place to write important context after you approve it"
- "This repo is the vault. Do not create a second `vault/` directory inside it."
- "Install plugins before onboarding so Assistant can read the right context."
- "Start with the tools where your work happens"
- "Onboarding should explain what it is checking before it checks it."
- "ask who Codex should know about"
- "offer to bootstrap a `write-like-me` skill from your sent Slack and email writing"
- "`experiments/`: short-lived spikes"
- "`tests/`: checks for template integrity"

**Dependencies:** Names the skills `onboarding`, `assistant`, `loop`, `new-project`, `new-person`, `write-like-me-bootstrap` (all in `.codex/skills/`); relies on `templates/` and `people/` structure; parallels and partially duplicates the vault rules in `AGENTS.md`.

---

## `templates/GOAL.md`

**Function:** Skeleton for a long-running objective, framed as an observable outcome plus how to prove progress and where approval is required.

**Conventions established:** Five fixed sections — Outcome, Baseline, Constraints, Verifiers, Approval Gates. Goals are defined by observable completion, not activity; constraints include non-goals; every goal names its verifiers up front.

**Quotable phrases:**
- "The observable result that means this goal is complete."
- "Current state before work begins."
- "Important limits, preferences, or non-goals."
- "Command, check, screenshot, review, or artifact that can prove progress."
- "Actions that require explicit user approval."

**Dependencies:** Root `AGENTS.md` routes "long-running objectives" here; pairs with `templates/RESULT.md` as the goal→result lifecycle; used by the `ultragoal` skill context.

---

## `templates/PROJECT_AGENTS.md`

**Function:** Skeleton for per-project agent instructions that supplement the root `AGENTS.md`.

**Conventions established:** Five fixed sections — Purpose, Source Of Truth, Commands, Safety Gates, Local Conventions. Source Of Truth is an ordered priority list with `README.md` always first. Commands live in a shell block. Local Conventions explicitly *supplement* (not replace) root rules.

**Quotable phrases:**
- "Describe what this project owns and when agents should work here."
- "List canonical files, services, datasets, or docs in priority order."
- "State any actions that require explicit user approval."
- "State any files, services, or accounts that must not be modified."
- "Add naming, style, test, or data-handling rules that supplement the root `AGENTS.md`."

**Dependencies:** Instantiated by `.codex/skills/new-project`; governed by the root `AGENTS.md` layering rule (specific-wins-on-conflict); Source Of Truth section points at the project's `README.md` (from `templates/project_README.md`).

---

## `templates/RESULT.md`

**Function:** Skeleton for recording completed work with evidence.

**Conventions established:** Three fixed sections — Completed, Verification, Remaining Work. Results are inseparable from their proof; gaps are stated, not omitted.

**Quotable phrases:**
- "What changed."
- "Commands, checks, screenshots, or review evidence."
- "Follow-ups, blockers, or known gaps."

**Dependencies:** Counterpart to `templates/GOAL.md` (Verifiers → Verification); root `AGENTS.md` routes "completed work and verification" here.

---

## `templates/experiment_README.md`

**Function:** Skeleton for a short-lived spike with explicit continue/pause/graduate framing.

**Conventions established:** Six sections — Goal, Status, How To Run, Decision Criteria, Notes (plus title). Every experiment carries its own kill/promote criteria; status must state whether it should "continue, pause, or graduate." Notes are explicitly short-lived.

**Quotable phrases:**
- "Current state and whether the experiment should continue, pause, or graduate."
- "What would make this worth turning into a project?"
- "What would make this worth archiving?"
- "Short-lived context and observations."

**Dependencies:** Lives under `experiments/` per root `AGENTS.md`; "graduate" implies conversion to `templates/project_README.md`; instantiated via `.codex/skills/new-project`.

---

## `templates/project_README.md`

**Function:** Skeleton for the canonical status file of a long-lived project — the first thing an agent reads.

**Conventions established:** Seven sections — Goal, Status, How To Run, Source Of Truth, Next Steps, Notes. Status includes "last meaningful update"; Source Of Truth splits into Primary docs / Data sources / Related projects; Next Steps is a checkbox list starting with one "first concrete next step"; Notes hold context that must survive the chat.

**Quotable phrases:**
- "Current state, known constraints, and last meaningful update."
- "First concrete next step."
- "Durable context that should not live only in chat."

**Dependencies:** Ranked #1 in `PROJECT_AGENTS.md`'s Source Of Truth order; root `AGENTS.md` requires updating it "when adding, archiving, renaming, or changing the status of work"; instantiated via `.codex/skills/new-project`.

---

## `people/README.md`

**Function:** Folder policy for durable notes about humans and agents.

**Conventions established:** Public-safe by default — no secrets, private account data, sensitive health details, or confidential personal info; content should be preferences, working agreements, recurring responsibilities, open threads; stale-prone facts get a `last verified` date. `person.md` is the template for humans, `agent.md` for agents.

**Quotable phrases:**
- "Durable notes about humans and agents you collaborate with."
- "Keep this folder public-safe by default"
- "Prefer preferences, working agreements, recurring responsibilities, and open threads."
- "Add a `last verified` date when a fact may go stale."

**Dependencies:** Governs `people/person.md` and `people/agent.md`; root `AGENTS.md` routes "human and agent collaboration notes" here.

---

## `people/person.md`

**Function:** Template for a note about a human collaborator, with explicit boundaries on what agents may assume or do on their behalf.

**Conventions established:** Seven sections — Role, Relationship / Context, Preferences (Communication / Decision style / Useful context bullets), Ongoing Threads (checkboxes), Boundaries, Last Verified (ISO date). People notes include agent-facing boundaries, not just facts; freshness is tracked per file.

**Quotable phrases:**
- "What this person does or how they relate to this workspace."
- "How you usually work together."
- "Open topic or responsibility."
- "Things agents should not assume, share, or do on this person's behalf."

**Dependencies:** Governed by `people/README.md` public-safe policy; instantiated via `.codex/skills/new-person`; onboarding (per root `AGENTS.md` and README) proactively proposes these files after connector scans.

---

## `people/agent.md`

**Function:** Template for a note about a non-human collaborator (an agent), symmetric to `person.md` but focused on capability, rules, and failure modes.

**Conventions established:** Eight sections — Role, Strengths, Tool Access, Operating Rules, Handoff Notes, Known Failure Modes, Last Verified. Agents are documented like teammates, including what to tell the next worker and known mistakes to watch for; same `Last Verified` freshness convention as `person.md`.

**Quotable phrases:**
- "What this agent is responsible for."
- "Tools, connectors, services, or repos this agent can use."
- "What another agent or human should know before continuing work."
- "Mistakes to watch for."

**Dependencies:** Governed by `people/README.md`; parallels `people/person.md`; root `AGENTS.md` treats agents and humans uniformly under `people/*.md`.

---

## Cross-cutting patterns in this layer

- Uniform frontmatter: only `last_edited: YYYY-MM-DD`, no other metadata.
- Placeholder convention: `# <Name>` angle-bracket titles; `<Summary>` inline; comment-only shell blocks (`# Add setup or run commands here.`).
- Section prompts are written as one-line imperative or definitional sentences that tell the filler-in exactly what qualifies — the template *is* the instruction.
- Evidence discipline everywhere: Verifiers (GOAL) → Verification (RESULT) → "checks for template integrity" (tests/).
- Approval/safety gates appear at every level: root AGENTS.md Safety, template Approval Gates / Safety Gates, person Boundaries, agent Operating Rules.
- Freshness discipline: `last_edited` frontmatter plus per-file `Last Verified` sections for people/agents.