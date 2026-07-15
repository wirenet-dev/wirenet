---
last_edited: 2026-07-15
---

# Jason Liu Upstream Reference

WireNet Manager is a deliberate downstream of Jason Liu's
`jxnl/personal-monorepo-template`. Preserve `upstream` as a fetch-only remote so
the original remains inspectable without giving it push access.

## Reference Boundary

Jason's template remains the reference for the plain-file workspace model:

- one local repository as durable Assistant memory;
- `projects/` for long-lived work and `experiments/` for spikes;
- `people/` for collaborator context;
- root and nested `AGENTS.md` files for durable agent guidance;
- repo-local skills for onboarding and repeatable workspace operations;
- Git for reviewable history.

WireNet adds deterministic bootstrap and health checks, external-workspace
routing, an installable plugin, and an OKF-compatible knowledge profile. Keep
those additions separate enough that upstream changes can still be reviewed by
intent instead of mechanically merged without inspection.

## Original Bootstrap And Communication Model

At upstream commit `df863768495aaf524a2bf9b5b25ef2622a2591a1`, Jason's fast
start still tells the user to press `Cmd+Cmd` and say
`Set me up with jxnl/personal-monorepo-template as ~/vault`. Codex clones that
repository, opens it as the vault, and then uses its repo-local `onboarding`
skill. There is no separate upstream skill named `bootstrap`.

The onboarding skill builds a first map, interviews the user, checks useful
connectors, proposes people and project files, offers a core check-in, and may
offer `write-like-me-bootstrap` from user-authored sent email and Slack. Its
memory guidance may use recurring evidence from roughly the last 90 days when
sources support it, but it defines no fixed mailbox import window and stores no
raw communication archive.

Jason's template also has no canonical `communication-and-files.md`, mail
bridge, or email bridge. Communication awareness is distributed across
connected sources, `agent/USER_CONTEXT.md`, `people/*.md`, project `README.md`
state, project `AGENTS.md` source routes, optional writing-style memory, and the
approved recurring Assistant check-in. WireNet preserves that behavior while
allowing an optional typed `docs/communication-and-files.md` instance concept
when a real cross-project source map deserves one.

## Mechanical Comparison

Refresh the upstream reference and print the current delta:

```sh
python3 scripts/compare_upstream.py --fetch
```

Use JSON for automation or a review artifact:

```sh
python3 scripts/compare_upstream.py --fetch --json
```

The report is read-only apart from updating the local remote-tracking ref. It
does not merge, rebase, reset, amend, stage, commit, or push anything.

## Semantic Routing Comparison

The Git comparison shows file and commit drift. The frozen routing contracts
show behavioral drift:

- [`routing/jason-liu-original.md`](routing/jason-liu-original.md) documents the
  original scaffold, producers, consumers, and routing behavior at upstream
  commit `df863768495aaf524a2bf9b5b25ef2622a2591a1`.
- [`routing/wirenet-manager-v0.2.md`](routing/wirenet-manager-v0.2.md) documents
  the same dimensions for the distributed plugin and generated Manager.
- [`routing/comparison-and-regression.md`](routing/comparison-and-regression.md)
  explains preserved, changed, added, and removed behavior.

The matching JSON contracts live under `contracts/routing/`. Compare them
without network or Git mutation:

```sh
python3 scripts/compare_routing_contracts.py
```

Do not update the frozen Jason contract merely because the local WireNet tree
changed. Refresh it only after inspecting a real upstream routing change.

## Upstream Review Rule

When `behind` is greater than zero:

1. Read each upstream commit and its file diff.
2. Classify it as inherited unchanged, adapted for WireNet, or intentionally
   rejected with a short reason.
3. Apply useful changes as focused WireNet commits; do not blindly merge the
   full branch after the product model has diverged.
4. Run the full Manager validation suite.

This keeps ancestry and comparison useful even if WireNet Manager becomes a
substantial product rather than a thin fork.
