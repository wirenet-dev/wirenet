# wirenet Adoption Map — upstream `jxnl/personal-monorepo-template` → wirenet v0.5

Targets are relative to `/Users/gitt/Developer/wirenet-v0.5/plugins/wirenet/`. Seed = `templates/manager/AGENTS.md`.

## Root layer

| Upstream artifact/function | Disposition | Target | Wording to carry |
|---|---|---|---|
| Root `AGENTS.md` — collaboration posture | ADAPT | `templates/manager/AGENTS.md` (Collaboration) | "ask the smallest useful question that would change the work"; "Name disagreements plainly and briefly… then proceed"; "Lead with what changed, what was verified, and what still needs attention" |
| Root `AGENTS.md` — discovery order + nearest-AGENTS layering | ALREADY PORTED | seed "Start Here" | — |
| Root `AGENTS.md` — durable-state routing table | ALREADY PORTED | seed "What Lives Where"; `skills/manager/SKILL.md` Write table | — |
| Root `AGENTS.md` — vault-update approval, prefer canonical file | ADAPT | seed "Keeping This Current" | "Prefer updating the canonical existing file over creating adjacent notes."; "Do not leave decisions only in chat when they will matter later." (latter already in seed) |
| Root `AGENTS.md` — blocked-validation rule | ADAPT | seed "Collaboration" | "When validation is blocked, say exactly what was not run and why." |
| Root `AGENTS.md` — symptom/cause rule | ADOPT VERBATIM | seed "Collaboration" | "If a request points at a symptom, look one level deeper for the cause before patching." |
| Root `README.md` — vault identity pitch | ADAPT | `templates/manager/README.md`; `skills/manager-setup/references/manager-model.md` | "a place to look before it acts and a place to write important context after you approve it" |
| Root `README.md` — install-plugins-before-onboarding order | ADAPT | `skills/manager-setup/references/runtime-preflight.md` | "Install plugins before onboarding so [the Manager] can read the right context." |
| `templates/GOAL.md` | ADOPT VERBATIM (lazy, per core) | `skills/manager/references/vault-model.md` (embedded skeleton) | "The observable result that means this goal is complete."; "Command, check, screenshot, review, or artifact that can prove progress."; "Actions that require explicit user approval." |
| `templates/RESULT.md` | ADOPT VERBATIM (lazy) | `skills/manager/references/vault-model.md` | "What changed." / "Commands, checks, screenshots, or review evidence." / "Follow-ups, blockers, or known gaps." |
| `templates/PROJECT_AGENTS.md` | ADAPT (only-for-real-deltas rule) | `skills/manager/references/vault-model.md` | "List canonical files, services, datasets, or docs in priority order."; "State any files, services, or accounts that must not be modified."; "supplement the root `AGENTS.md`" |
| `templates/project_README.md` | ADAPT | `skills/manager/references/vault-model.md` (pack skeleton) | "Current state, known constraints, and last meaningful update."; "First concrete next step."; "Durable context that should not live only in chat." |
| `templates/experiment_README.md` | ADAPT (graduate→promote, per core lifecycle) | `skills/manager/references/vault-model.md` | "What would make this worth turning into a project?"; "What would make this worth archiving?" |
| `people/README.md` — public-safe policy | ALREADY PORTED | seed "What Lives Where" (relationship/interaction rule) | — |
| `people/README.md` — `last verified` freshness | ADAPT | `skills/manager/references/vault-model.md` (people skeleton) | "Add a `last verified` date when a fact may go stale." |
| `people/person.md` — sections incl. Boundaries | ADAPT | `skills/manager/references/vault-model.md` | "Things agents should not assume, share, or do on this person's behalf."; "How you usually work together." |
| `people/agent.md` — agents-as-teammates note | ADAPT (folded into `people/<slug>.md`, no separate template) | `skills/manager/references/vault-model.md` | "What another agent or human should know before continuing work."; "Mistakes to watch for." |
| `last_edited` frontmatter convention | SUPERSEDED by ADR 004 | — | — |
| Repo-root-is-vault / never nest a second vault | ALREADY PORTED | core contract; `skills/manager-setup/SKILL.md` resolve step | — |

## Assistant core

| Upstream artifact/function | Disposition | Target | Wording to carry |
|---|---|---|---|
| `assistant/SKILL.md` — persona posture | ADAPT | `skills/manager/SKILL.md` intro | "Sound like capable work support, not setup software."; "Push back when a request is risky, underspecified, or likely to create noise."; "Prefer judgment over giant summaries." |
| Exact greeting "Hi, I'm your assistant." + no narration before it | ADAPT | `skills/manager-setup/references/first-meeting-flow.md` | "Hi, I'm your assistant." (localized); "Do not send process narration before that sentence." |
| Three-state setup detection (brand_new/partial/established) | ADAPT | `skills/manager-setup/SKILL.md` | "Classify quietly"; "Do not replay onboarding; orient briefly and help with the actual request." |
| Hard action boundary (that-specific-action approval) | ALREADY PORTED | seed "Safety"; core Update Contract | — |
| Day-to-day scope list (buried asks, prep gaps, drift) | ADAPT | `skills/manager/SKILL.md` Work | "changes that alter what matters this week" |
| `heartbeat-philosophy.md` — quiet-operation core rule | ADAPT | `skills/manager-setup/references/onboarding.md` (continuity offer) | "Work first. Notify second."; "notify only when there is a meaningful delta or useful next action. It is fine to do work and stay quiet." |
| Heartbeat proposal block + success/fallback scripts | ADAPT (per-runtime: scheduled tasks / thread automations) | `skills/manager-setup/references/onboarding.md` | "If there is nothing useful, I will stay quiet."; "Do not tell the user an automation was created unless the automation tool succeeds."; "Call the automation tool only after a clear yes." |
| Good/bad notify reasons | ADOPT VERBATIM | `skills/manager-setup/references/onboarding.md` | "generic digests with no judgment"; "weakly supported guesses dressed up as insight"; "instead of inventing an interruption" |
| Monitor-thread topology, 9:00/4:00 lanes | REJECT (topology) | — (times survive as push windows in core Continuity) | — |
| `memory-guidance.md` — "Preserve durable meaning, not motion" | ALREADY PORTED | seed "Keeping This Current" | — |
| Seven-section chat-memory model | SUPERSEDED by ADR 012 | — (memory lives in vault files) | — |
| Keep / don't-keep lists + 90-day evidence window | ADAPT | `skills/manager/references/vault-model.md` | "Keep recent pressure separate from durable identity and context."; "one-off wording quirks from a single message" (don't-keep) |
| People discipline (no one-mention people, no shallow maps) | ALREADY PORTED | `skills/manager/SKILL.md` People | — |
| Fact / self-report / inference taxonomy | ADAPT | seed "Keeping This Current" | "If an inference materially affects future behavior, either keep it tentative or ask the user before making it durable." |
| Correction protocol (stop acting on the older read) | ALREADY PORTED (ADR 011 strengthens it) | core Contradiction Rule | — |
| `assistant-thread-template.md` — pinned-chat contract | ADAPT | `skills/manager-setup/references/manager-task-template.md` | "bring me useful judgment, not giant summaries"; "do not imply you checked sources you could not access"; "distinguish facts from your read of the situation when that distinction matters"; "what looks easy for me to lose track of" |
| `agents/openai.yaml` interface manifest | ALREADY PORTED | `skills/manager-setup/agents/openai.yaml`, `skills/manager/agents/` | "stays in your corner" (keep in short_description) |

## Onboarding

| Upstream artifact/function | Disposition | Target | Wording to carry |
|---|---|---|---|
| `onboarding/SKILL.md` — 9-step flow + definition of done | ADAPT | `skills/manager-setup/SKILL.md` | "handled, declined, or unavailable"; "Every turn should end with a clear question, next step, setup offer, or final recap." |
| `first-meeting-flow.md` — 6-phase choreography | ADAPT | `skills/manager-setup/references/first-meeting-flow.md` | "Make this feel like a capable assistant saying hello, not a setup wizard."; "When context exists, read before asking the user to steer."; "If context is thin, say so and begin the interview."; "Do not end completed onboarding with another configuration question." |
| Close recap headings | ADOPT VERBATIM | `skills/manager-setup/references/first-meeting-flow.md` | "**Here Is The Map I Am Carrying**" … "**You Can Just Talk To Me Now**"; closing line "You can just talk to me now." |
| `question-bank.md` — six interview questions + loop discipline | ADOPT VERBATIM | `skills/manager-setup/references/first-meeting-flow.md` | All six questions verbatim; "Rambling is welcome; I will do the cleanup."; "ask the next still-missing question"; "safe to ignore unless you bring them up" |
| `shared-memory-vault.md` — vault pitch + extend-in-place | ADAPT | `skills/manager-setup/references/manager-model.md` | "This chat is where we talk. The check-in is what brings me back. The [Manager] is the plain-file memory I maintain so durable work context does not live only inside one chat."; "Extend the existing repo in place instead of creating another vault root."; "raw email/chat dumps, one-off names, weak guesses, or activity logs" |
| `starter-capabilities.md` — check-in pitch, help defaults | ADAPT | `skills/manager-setup/references/onboarding.md` | "If something matters, I will bring it here. If nothing useful changed, I will stay quiet."; "Recommend from the user's actual map, not a generic menu."; "open-loop maps", "what-changed briefs", "prep-gap checks" |
| Monitor-lane menu (Daily/People/Project monitors) | REJECT (topology) | — | — |
| `setup_shared_memory_vault.py` scaffolder | ALREADY PORTED | `skills/manager-setup/scripts/bootstrap_manager.py` | — |
| `ROOT_AGENTS_TEMPLATE` — Source Order, writing rules | ADAPT | seed "Keeping This Current" / "Start Here" | Source order: vault notes → self-report and corrections → connected context → chat; "If nothing meaningful changed, do not churn the vault."; "Use absolute dates and label inference when it matters."; "Keep weak guesses tentative until the user confirms them or repeated evidence supports them." |
| `USER_CONTEXT_TEMPLATE` | ADAPT | `templates/manager/agent/USER_CONTEXT.md` | "Draft or propose first. Act only after the user explicitly approves that specific external or shared action." |
| `TODO_TEMPLATE` (Active/Waiting/Completed) | SUPERSEDED by ADR 007 | — (core stack: Now/Next/Waiting/Later/Someday in `templates/manager/TODO.md`) | — |
| `new_project_note.py` / `new_person_note.py` generators | REJECT (generators) | — (doctor validates; agent writes from skeletons) | — |
| Packet/person template wording inside those scripts | ADAPT | `skills/manager/references/vault-model.md` | "Why They Matter Now"; "a short, dated reason this relationship matters"; "evidence-backed collaboration patterns"; "Recurring Sources To Revisit"; "dated when timing matters"; "update the canonical note instead" |
| Obsidian wikilink router entries | REJECT (syntax) | — (plain Markdown links in `projects/index.md`) | — |

## Other skills

| Upstream artifact/function | Disposition | Target | Wording to carry |
|---|---|---|---|
| `.codex/skills/README.md` index model | SUPERSEDED by ADR 001 | — (marketplace + one plugin) | — |
| `new-project` skill (classify, slug, output contract) | ALREADY PORTED | `skills/manager/SKILL.md` Lifecycle | "Report the created folder and any missing fields that need human input." (worth adding to vault-model.md) |
| `new-person` skill | ALREADY PORTED | `skills/manager/SKILL.md` People | — |
| `write-like-me-bootstrap` — posture model + privacy boundary | ALREADY PORTED (references exist) | `skills/manager-setup/references/write-like-me*.md` | Verify these carry: "Cluster writing into postures rather than one generic voice."; "Compare Slack and email. Preserve differences instead of flattening them."; "Keep synthetic examples synthetic; do not quote private Slack or email."; "Default to drafting the message, not explaining the style." |
| `write-like-me` onboarding offer script | ADOPT VERBATIM | `skills/manager-setup/references/onboarding.md` | "I can also bootstrap a write-like-me skill from your sent email and Slack messages, split by posture like quick replies, pushback, delegation, intros, and status updates. Want me to do that?" |
| `ultragoal` | REJECT (separate-layer) | — (optional layer owning `WORKLOG.md`, per core; `$manager` only defends the boundary) | — |
| `loop` | REJECT (runtime-specific) | — (core Continuity replaces it per-runtime) | — |
| `gh-*`, `audit-ai-code/frontend`, `yeet` | REJECT (off-scope) | — | — |
| `audit-ai-writing`, `simple-html-artifact` | REJECT (off-plugin) | — (ship in `content-tools@wirenet`) | — |

## Seed polish (templates/manager/AGENTS.md)

1. Verification in handoffs — before: "Lead with what changed and what needs attention." → after: "Lead with what changed, what was verified, and what still needs attention."
2. Anti-churn line — before: "Write only when a future task would otherwise misunderstand…" → after: append "If nothing meaningful changed, do not churn the Manager." to close "Keeping This Current".
3. Canonical-file preference — the seed has no adjacent-notes rule; add: "Prefer updating the canonical existing file over creating adjacent notes."
4. Dates and inference — before: "no activity logs, raw messages, transcripts, or speculation presented as fact." → after: "…or speculation presented as fact. Use absolute dates and label inference when it matters."
5. Symptom/cause — add to Collaboration: "If a request points at a symptom, look one level deeper for the cause before patching."
6. Blocked validation — add to Collaboration: "When validation is blocked, say exactly what was not run and why."

## Setup-station spec (build order for `skills/manager-setup`)

1. Setup-state model from `onboarding/SKILL.md`: brand_new / partial / established, classified quietly; established means skip.
2. Six-phase choreography from `first-meeting-flow.md`: hello (exact greeting, no prior narration) → state → first map (read before asking) → interview → offers → close.
3. Interview: the six `question-bank.md` questions verbatim, one at a time, per-answer map update, no menus or reply codes.
4. Vault offer from `shared-memory-vault.md`: chat/check-in/vault three-sentence pitch (localized to ~/Manager), extend-in-place rule, `bootstrap_manager.py` as the scaffolder.
5. Continuity offer from `heartbeat-philosophy.md` + `starter-capabilities.md`: propose one check-in grounded in the map, "What I Will Check / What I Would Flag Right Now / Question" block, create only after a clear yes, success message only after tool success, fallback script when the runtime lacks automations.
6. Global wiring + qmd registration (wirenet-only stations), each with its own approval.
7. Write-like-me offer using the verbatim upstream pitch, gated on enough authored messages.
8. People/pack proposals after connector scans: propose specifics, write only approved items (memory-guidance seeding gate: never seed before the first calibration answer).
9. Close from `first-meeting-flow.md`: rename/pin guidance, five bold recap headings, "You can just talk to me now." — never end on a configuration question; done only when every offer is handled, declined, or unavailable.

## wirenet-only (no upstream counterpart)

- Workspace bindings with two-way global wiring (`.wirenet/workspace-bindings.json`, managed global block, local binding line) — ADR 005.
- Contradiction rule as the read-time feedback loop — ADR 011.
- Vault carries its own OS; plugin-optional operation — ADR 012.
- Conventions over frontmatter; no status fields, no IDs in documents — ADR 004.
- `areas/` and the "does it end?" classification test; Someday stack — ADR 007.
- Doctor, staleness findings, orientation budget; contracts hold only code-enforced schemas — ADR 003.
- qmd retrieval layer as optional candidate routing — core contract.
- Base/Shelf organizational layer, clone-first, open-spec intent — ADR 008/009/010.
- Open-core, service-led delivery; single wirenet plugin marketplace — ADR 006/001.