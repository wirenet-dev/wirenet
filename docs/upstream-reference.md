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

WireNet may add deterministic setup, repair, migration, external-workspace
routing, installable plugins, and an OKF-compatible knowledge profile. Keep
those additions separate enough that upstream changes can still be reviewed by
intent instead of mechanically merged without inspection.

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
