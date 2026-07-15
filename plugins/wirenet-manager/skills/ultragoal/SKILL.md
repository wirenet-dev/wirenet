---
name: ultragoal
description: Design, critique, activate, or run a persistent Codex goal. Use only when the user explicitly names UltraGoal, explicitly invokes `$ultragoal`, or explicitly asks to create, set, start, or activate a persistent goal. Never infer activation from importance, duration, complexity, or vague requests to keep working.
---

# UltraGoal

Run persistent goals only after explicit user activation. A good UltraGoal has
an observable finish line, a verifier that can fail, and enough durable state
to recover after interruptions.

## Modes

- **Design:** Draft or critique a goal without activating it.
- **Activate:** Ground and red-team the goal, then call `create_goal`.
- **Run:** Continue an active goal until it is verified, genuinely blocked, or
  the user changes direction.

Never call `create_goal` from vague planning language. Never set a token budget
unless the user explicitly requests one.

## Resolve Durable State

1. Resolve the current WireNet Manager through `WIRENET_MANAGER_DIR`, then
   `~/Manager`.
2. If the current workspace is outside Manager, use
   `$wirenet-manager-sync` to resolve its Project Pack. If it is untracked, do
   not activate until the user classifies it.
3. If the task is already inside a Project Pack, use that packet.
4. If no Manager or Project Pack applies, follow the nearest repository
   conventions without creating a Manager binding implicitly.

Within a WireNet Project Pack:

- `GOAL.md` holds the stable outcome, baseline, constraints, completion
  criteria, verifier, and approval gates.
- `WORKLOG.md` is owned exclusively by an explicitly active UltraGoal. Create
  it only when durable recovery across attempts is useful.
- `RESULT.md` holds the final outcome and verification.
- `log.md` remains an optional sparse Manager chronology. Do not mirror the
  detailed WORKLOG into it.

Every Project Pack concept must preserve the packet's `project_id`. A new
`WORKLOG.md` uses `type: "Goal Worklog"`, the Project Pack schema, and
`producer: "ultragoal"` so the Manager Doctor can verify ownership.

## Define The Goal

Ground:

- the observable outcome;
- the current baseline;
- the strongest independent verifier;
- relevant regression and safety checks;
- the iteration loop after a failed verifier;
- approval gates for irreversible, public, shared, or costly actions;
- the blocker standard and exact completion proof.

Prefer an ordinary task when the work is one-shot, primarily taste-dependent,
requires repeated preference decisions, or lacks a credible verifier.

## Activate Last

Before activation, check that success cannot be faked by weakening the verifier,
narrowing scope, hiding failures, or substituting mocks without approval.

When activation was explicitly requested:

1. Write or update durable goal state only when the repository convention or
   user request authorizes it.
2. Call `create_goal` as the final activation step with a compact objective,
   preferably `Complete and verify the objective defined in <absolute GOAL.md
   path>.`
3. Report the exact active objective and continue under active-goal discipline.

## Active-Goal Discipline

- Inspect goal state when resuming or after material steering.
- Iterate by changing one meaningful thing, running the verifier, recording
  evidence, and choosing the next action.
- Preserve partial results and the next action in `WORKLOG.md` when recovery
  requires them.
- Mark complete only after the objective and completion proof are satisfied.
- Mark blocked only after the required repeated external-blocker threshold and
  when no meaningful progress remains.
- On completion, distill the durable outcome into `RESULT.md` and reconcile the
  Project Pack through `$wirenet-manager-sync` when future work would otherwise
  resume incorrectly.
