# Skills Inventory — Remaining Skills (`.codex/skills/`)

## `.codex/skills/README.md`

**Function:** One-page index of repo-local Codex skills; declares the usage model (read `SKILL.md` in place, no install step).

**Conventions/rules:**
- Skills are repo-local and used by reading the relevant `SKILL.md` directly — no packaging or registration.
- Frontmatter carries `last_edited: YYYY-MM-DD` (dateline convention appears across all skill files).
- Flat bullet list of included skills as the whole directory documentation.
- Explicit public/private boundary for the template itself.
- Note: the README's list omits `write-like-me-bootstrap` even though the directory exists (index drift).

**Quotable phrases:**
- "Repo-local Codex skills. Use them in place by reading the relevant `SKILL.md`."
- "Do not put private identity, finance, or account-specific skills in a public template. Add those locally in your own repo if needed."

**Dependencies:** References all skill directories; none required to function.

**Also present (handled elsewhere, listed only):** `assistant`, `audit-ai-code`, `audit-ai-frontend`, `audit-ai-writing`, `gh-address-comments`, `gh-commit`, `gh-fix-ci`, `onboarding`, `simple-html-artifact`, `yeet`.

---

## `.codex/skills/new-project/` (`SKILL.md` + `scripts/new_project.py`)

**Function:** Bootstraps a new project or experiment directory with README and optional `AGENTS.md` so agents can discover the work later.

**Conventions/rules:**
- Read root `AGENTS.md` and `README.md` first; classify work as long-lived `project` vs short-lived `experiment` before scaffolding.
- Lowercase hyphenated slugs; experiments MUST be named `exp-<topic>-YYYY-MM-DD`.
- Prefer the helper script over hand-scaffolding ("Run the helper when possible").
- After generation, only add project-specific commands, data sources, and safety gates to `AGENTS.md` "if they matter."
- Output contract: report the created folder plus missing fields needing human input.

**What the script generates:**
- CLI: `new_project.py "Name" [--type project|experiment] --summary "..." [--slug] [--no-agents]`; `--summary` is required.
- Projects go to `projects/<slug>/`, experiments to `experiments/exp-<slug>-<today>/` (auto-prefixes `exp-` and appends today's date if missing).
- Writes `README.md` from `templates/project_README.md` or `templates/experiment_README.md`, substituting `<Project Name>`/`<Experiment Name>` and `<Summary>` placeholders.
- Writes `AGENTS.md` from `templates/PROJECT_AGENTS.md` unless `--no-agents`.
- Refuses to overwrite (`FileExistsError` if the path exists); prints `created: <rel-path>`.
- `slugify`: lowercase, non-alphanumerics collapsed to `-`, fallback `new-project`.

**Quotable phrases:**
- "Create a project or experiment that agents can discover later."
- "Experiments must use `exp-<topic>-YYYY-MM-DD`."
- "Report the created folder and any missing fields that need human input."
- "Add project-specific commands, data sources, and safety gates to the generated `AGENTS.md` if they matter."

**Dependencies:** `templates/project_README.md`, `templates/experiment_README.md`, `templates/PROJECT_AGENTS.md`; root `AGENTS.md` and `README.md`; the `projects/` and `experiments/` top-level directories. Script assumes it sits 4 levels below repo root (`parents[4]`).

---

## `.codex/skills/new-person/` (`SKILL.md` + `scripts/new_person.py`)

**Function:** Creates or updates a public-safe person note under `people/` from the repo's `people/person.md` template.

**Conventions/rules:**
- Read `people/README.md` and `people/person.md` before creating.
- Lowercase hyphenated slug from the person's name → `people/<slug>.md`.
- Content rule: "only useful, non-sensitive context"; explicitly exclude private facts, secrets, health details, account data, confidential content.
- Freshness rule: add/update a `Last Verified` date "when facts may go stale."
- Output contract: report path + fields still needing human input.

**What the script generates:**
- CLI: `new_person.py "Person Name" [--role "..."] [--slug] [--force]`.
- Copies `people/person.md`, replacing `<Person Name>`, the role placeholder line ("What this person does or how they relate to this workspace." → role or `TBD`), and `YYYY-MM-DD` → today.
- Idempotent by default: if the note exists, prints `exists: <path>` and exits 0; `--force` overwrites. Creates `people/` if missing. Prints `created: <rel-path>`.

**Quotable phrases:**
- "Create a durable, public-safe note for a human collaborator."
- "Edit the generated note with only useful, non-sensitive context."
- "Keep private facts, secrets, health details, account data, and confidential content out of the note."
- "Add or update `Last Verified` when facts may go stale."

**Dependencies:** `people/person.md` template, `people/README.md`; complements the `assistant` skill's people-note usage. Same `parents[4]` root assumption and `slugify` as new-project.

---

## `.codex/skills/write-like-me-bootstrap/` (`SKILL.md`, `agents/openai.yaml`, `references/generated-skill-template.md`, `references/style-profile-template.md`)

**Function:** A skill that generates another skill — inspects the user's real Slack/email writing and bootstraps a durable repo-local `write-like-me` drafting skill without persisting raw private messages.

**Conventions/rules:**
- Output location fixed: `.codex/skills/write-like-me/` with `SKILL.md`, `references/style-profile.md`, optional `agents/openai.yaml` — i.e., generated skills follow the same directory shape as authored ones.
- Source scan: prefer authored messages (sent Slack + sent email), last 90–180 days; older writing only when it clarifies stable style. Degrade gracefully if a connector is missing.
- Hard privacy boundary: no raw excerpts in durable files; synthetic examples only; evidence recorded as compact descriptors (e.g., "sent email follow-ups, March-June 2026"). Reading connected context is allowed only when the user asked for onboarding or this skill; writing requires explicit approval.
- Voice is modeled as **postures**, not one generic voice: quick Slack reply, decision/pushback, delegation/ask, executive/status update, email reply, intro/relationship note, scheduling/admin, apology/correction/repair.
- "Compare Slack and email. Preserve differences instead of flattening them."
- Preview-then-approve loop before writing files.
- Generated-skill requirements: route by channel and posture before drafting; ask only when audience/channel/goal would materially change the draft; include critique mode; never reveal source messages; instruct future assistants to update the profile on correction.
- Onboarding hook: offer the bootstrap after the first connected scan finds enough authored writing, with a scripted concrete offer.
- Skill UI metadata lives in `agents/openai.yaml` (`display_name`, `short_description`, `default_prompt` using `$skill-name` invocation).

**Quotable phrases:**
- "Cluster writing into postures rather than one generic voice."
- "Compare Slack and email. Preserve differences instead of flattening them."
- "default to concise, useful drafts rather than style analysis"
- "include a critique mode that says what feels unlike the user"
- "Keep synthetic examples synthetic; do not quote private Slack or email."
- "Preserve the user's directness. Do not over-soften, over-format, or add generic assistant phrasing." (from the generated-skill template's Guardrails)
- "Default to drafting the message, not explaining the style." (generated-skill template)
- "For critique requests, say what feels unlike the user and provide a tighter rewrite."
- "Prefer adding or revising posture rules over preserving stale wording." (style-profile template Update Rules)
- Onboarding offer: "I can also bootstrap a write-like-me skill from your sent email and Slack messages, split by posture like quick replies, pushback, delegation, intros, and status updates. Want me to do that?"

**Reference-file structure worth noting:**
- `style-profile-template.md`: Source Basis (scope/date range/confidence/gaps) → Global Voice (stance, pacing, directness, warmth, humor, formality, common moves, avoid) → per-posture blocks each with Use when / Shape / Patterns / Avoid / Synthetic example → Critique Checklist (too formal / too verbose / too generic / too soft / too sharp / missing context) → Update Rules.
- `generated-skill-template.md`: full fenced `SKILL.md` skeleton including frontmatter, "Read First" pointer to the profile, 5-step workflow, and Guardrails.

**Dependencies:** Slack/Gmail connectors; the `assistant`/`onboarding` skills (this bootstrap is suggested during onboarding); its own two reference templates; the `.codex/skills/` directory convention. Notably absent from the README skill index.

---

## `.codex/skills/ultragoal/` (`SKILL.md` only)

**Function:** Governs designing, critiquing, and activating durable long-running Codex goals with verifiers, durable state files, approval gates, and completion proof.

**Conventions/rules:**
- Threshold test for a real goal: "an observable finish line, a verifier that can fail, and enough context for Codex to recover after interruptions."
- "Do not activate a goal from vague planning language." Never set a token budget unless explicitly requested.
- Four modes: Design (packet only, no `create_goal`), Critique, Activate (`create_goal` as the final step), Goal tree (only with explicit authorization for goal-backed subagents).
- Default Activation Rule: explicit skill invocation + concrete "do it" objective = Activate by default; don't stop at writing files.
- Goal-fit criteria: repeated attempts/waiting/recovery needed; success externally measurable; next failure actionable without new preference decisions; "completion evidence is stronger than Codex saying 'done.'"
- Loop definition must include: Outcome, Baseline, Primary verifier, Supporting checks, Iteration loop, Anti-cheating rules, Approval gates, Blocker standard, Completion proof.
- Anti-cheating: "do not weaken tests, narrow scope, hide failures, swap in mocks, or change benchmarks without approval."
- Blocker standard: "external blocker plus smallest next action; difficulty or uncertainty is not enough."
- Flaky checks require clean-state reproduction and consecutive passes "to rule out luck."
- Durable state file convention: `GOAL.md` (outcome/baseline/constraints/criteria), `WORKLOG.md` (attempts/evidence/next action), `RESULT.md` (final change/verification/risks).
- Delegation: parent keeps scope, integration, conflict resolution, final completion; delegate only separable lanes with named objective, non-goals, boundary, verifier, stop condition, evidence.
- Pre-activation red-team checklist (can success be faked, are words satisfiable while missing the outcome, are gates explicit, what happens after a failed attempt, is completion observable outside the agent).
- Compact objective format: `Complete and verify the objective defined in <absolute-path-to-GOAL.md>.`
- Goal packet output shape: Fit / Grounding / Goal brief / Delegation map / Exact objective / Activation state (`drafted`, `active`, `not recommended`).
- Active Goal Discipline: inspect state on resume; continue while a safe relevant step remains; complete only with proof; preserve partial results when stopping.

**Quotable phrases:**
- "A good goal has an observable finish line, a verifier that can fail, and enough context for Codex to recover after interruptions."
- "Do not activate a goal from vague planning language."
- "Ask only when the missing answer changes the finish line, grants consequential approval, or chooses between incompatible goals. Otherwise state the assumption and continue."
- "Stop once the finish line and verifier are grounded."
- "Separate observed facts, user requirements, and inferred choices."
- "completion evidence is stronger than Codex saying 'done.'"
- "inspect, change one meaningful thing, run verifier, record evidence, choose next action"
- "external blocker plus smallest next action; difficulty or uncertainty is not enough"
- "enough consecutive passes to rule out luck"
- "Could the words be satisfied while missing the user's real outcome?"
- "Preserve dirty work and read existing goal files before editing them."
- "do not merely say a goal should be set"

**Dependencies:** Codex `create_goal` / `update_goal` platform tools; project file conventions (proposes `GOAL.md`/`WORKLOG.md`/`RESULT.md` only when no convention exists). No repo-file dependencies.

---

## `.codex/skills/loop/` (`SKILL.md` only)

**Function:** Turns a plain-English "keep checking on this" request into a heartbeat automation attached to the current Codex thread.

**Conventions/rules:**
- Decide first whether a heartbeat is even useful; "continue immediately instead when the task can simply be finished now."
- Cadence chosen from expected feedback latency, urgency, cost, and noise risk; "Do not poll faster than the underlying state can plausibly change."
- Self-contained task prompt carries the work + completion condition + terminal behavior; timing/targeting stays in automation fields.
- Fixed automation-tool call shape: `mode=create`, `kind=heartbeat`, `destination=thread`, `status=ACTIVE`, plus inferred `name`, `prompt`, `rrule`.
- Thread-title lifecycle protocol: rename to `loop: <short task name>` on creation, `done: <short task name>` only after successful completion — never after a failed run, pause, or retry. Verb-led names.
- Never create a new thread, invent a thread ID, expose raw RRULE syntax, or substitute a detached cron job.
- Ambiguity handling: ask one concise question only for material ambiguity; offer task-appropriate cadence choices and recommend one ("Do not make Jason translate the task into scheduling jargon"); minor ambiguity → assume and state it.
- "Treat 'loop,' 'keep going,' and 'check again' as authorization to create the heartbeat requested in that message."
- Prefer updating an existing matching automation over creating a duplicate; on lifecycle operations preserve unchanged fields; restore `loop:` title on resume.
- "If the automation tool is unavailable, say so plainly. Never emit a raw automation directive as a workaround."
- Return only: loop name, cadence, what it will do. Note: description is personalized ("when Jason invokes $loop") — needs renaming when adopting the template.

**Quotable phrases:**
- "Turn a plain-English request into a heartbeat on the current thread with as little ceremony as possible."
- "Do not poll faster than the underlying state can plausibly change."
- "Do not make Jason translate the task into scheduling jargon."
- "If the ambiguity is minor, make a reasonable assumption and state it instead of interrupting setup."
- "say so plainly. Never emit a raw automation directive as a workaround."
- "Prefer updating an existing matching automation over creating a duplicate."

**Dependencies:** Codex automation tool (heartbeat/RRULE-based) and thread-title tool; current-thread context. No repo-file dependencies. Distinct from this environment's `loop` plugin skill — the repo version is Codex-automation-specific.