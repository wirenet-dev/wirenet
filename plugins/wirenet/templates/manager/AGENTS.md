# Manager Instructions

This folder is the user's Manager: their durable work memory. Any agent
working here, or in a workspace bound to it, follows these rules. They work
with no wirenet software installed — the wirenet plugin adds setup, health
checks, and cross-workspace reach, never required behavior.

## Start Here

- Read `README.md`, `TODO.md`, and `projects/index.md` before acting; open
  only the packs, people, and sources the task needs.
- Read the nearest `AGENTS.md` before working in any subdirectory. Local
  rules supplement these; when they conflict, the more specific rule wins.
- Match the language of the existing documents in conversation and new
  prose. File names and system vocabulary stay English.

## What Lives Where

- Cross-project commitments and waiting items: `TODO.md`, in the user's
  stated order. Uncommitted ideas: its final `## Someday` section.
- Working style and boundaries: `agent/USER_CONTEXT.md`.
- Work that ends with a defined outcome: `projects/<slug>/README.md` — it
  must be able to say when it is done. A pack `AGENTS.md` exists only for
  real local deltas: recurring sources, safety gates.
- Ongoing responsibility with a standard but no end: `areas/<slug>/README.md`
  — what healthy means, the current state against it, related projects, a
  review cadence. Quiet is normal for areas.
- A bounded question with a decision criterion: `experiments/<slug>/`.
- Durable relationship context: `people/<slug>.md`. The relationship decides
  the file; the interaction decides the content — never sensitive facts
  irrelevant to it.
- Curated evidence: `sources/`. Durable scratch: `notes/`. Structured
  cross-project documents: `docs/`. Inactive work: `archive/`. Generated
  intermediates: `outputs/` (git-ignored). All created on first use.
- Machine-local state (bindings, health): `.wirenet/` — not for prose.

Classify with one question — does it end? A defined outcome is a project; a
standard to maintain is an area; a bounded question is an experiment.

## Keeping This Current

- Write only when a future task would otherwise misunderstand an outcome, a
  decision, an owner, a blocker, a deadline, a source, or the next step.
- Store what search cannot find: intent, status, decisions, relationships,
  pointers. Never record what an agent can derive from a workspace itself.
- Replace, don't append. A pack's status says how things stand now, in about
  one screen. History lives in git. Prefer updating the canonical existing
  file over creating adjacent notes.
- When reality contradicts a pack, propose the correction with your handoff —
  never work around it silently.
- Preserve durable meaning, not motion: no activity logs, raw messages,
  transcripts, or speculation presented as fact. Use absolute dates and
  label inference when it matters.
- Preview durable writes and get approval unless that exact change was
  already approved. Do not leave decisions only in chat when they will
  matter later. If nothing meaningful changed, do not churn the Manager.

## Lifecycle

- Status is location plus index group. `projects/index.md` is the only
  catalog: Active, Waiting / Blocked, Later, Ongoing (areas), Archived.
- Retire a project by moving it to `archive/` with its entry. Areas archive
  only when the responsibility itself ends — never for being quiet.
- Experiments end by conclusion, promotion to `projects/`, or archive; keep
  the original as origin evidence.

## Safety

- Never store secrets, credentials, account numbers, or private keys.
- External side effects — sending, publishing, meetings, payments, deleting,
  automations, sync — each need explicit approval. Connected accounts are
  not permission to act.
- Distinguish sent, received, drafted, discussed, and approved.
- Prefer small, reversible edits; ask before anything destructive or
  surprising.

## Collaboration

- Direct, practical, low-ceremony. Lead with what changed, what was
  verified, and what still needs attention.
- Make reasonable calls on minor, reversible questions; ask the smallest
  useful question otherwise.
- Push back plainly when a request risks churn, context loss, or leaked
  private data.
- If a request points at a symptom, look one level deeper for the cause
  before patching.
- When validation is blocked, say exactly what was not run and why.
