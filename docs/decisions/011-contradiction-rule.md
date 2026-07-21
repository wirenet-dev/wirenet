# ADR 011: The Contradiction Rule

Date: 2026-07-21 · Status: accepted

## Context

The system's highest-precision error signal is the moment a reader notices a
pack no longer matches reality. Calendar heuristics guess; read-time
contradiction knows. Yet nothing obliged an agent to act on it — it could
quietly route around a stale pack, discarding the signal and leaving the trap
armed for the next reader. Each such encounter erodes the trust stock the
product actually sells (foundations.md, Meadows' vicious loop).

## Decision

When observed reality contradicts a pack during any task, the agent must
propose the correction — silent workarounds are forbidden. Proportionality:
the proposal arrives with the task's normal handoff, immediately only when
the contradiction blocks the task itself; "this pack contradicts X — please
review" is a valid minimum when the right fix is unknown. The rule mandates
proposing, never writing: preview and approval apply as always. The Base
layer inherits the rule verbatim — a contradicted entity yields a draft PR to
its owner.

## Consequences

Read-repair for prose: the missing feedback loop from readers to the stock is
closed. One sentence each in the core contract, the manager skill, and the
workspace-sync reference; later the base contract. Small in text, large in
effect on the only metric that matters — whether future tasks can trust what
they read.
