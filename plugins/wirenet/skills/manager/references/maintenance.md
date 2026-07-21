# Maintenance

Ongoing health, plugin updates, and retrieval upkeep. Setup runs once via
`$manager-setup`; everything recurring lives here.

## Health

- Run the plugin doctor when the user reports something broken, after
  structural moves (create, archive, promote, rebind), or before a release
  demo. It checks: every pack has a resolving `projects/index.md` entry,
  bindings resolve to existing paths, no seeded empty placeholders, no
  archived pack carrying new active state.
- Staleness: an active project quiet for ~90 days without a waiting handoff
  is a finding; an area is measured against its own review cadence instead —
  idle is normal there, a missed review is the finding.
- Reclassification is two-stage: the doctor flags mechanical candidates
  (long-lived active pack, recurring activity, no visible completion state);
  the agent then applies the "does it end?" test to the README before
  proposing the move (`git mv` to `areas/` plus the index regroup) as a
  previewed diff. A declined proposal is remembered in `.wirenet/` and not
  re-raised.
- Fix findings as previewed proposals, smallest diff first. If the Manager is
  missing or structurally broken beyond small fixes, hand off to
  `$manager-setup` in repair mode instead of improvising structure.

## Guardrails

- Three layers: **invariants** (doctor errors — root files, resolving index,
  valid bindings, no secrets; always surfaced, repair offered), **conventions**
  (findings — sizes, groups, staleness; deviate consciously), and **free
  space** — the doctor checks only what the contract names and never comments
  on unknown folders, files, or sections. Local rules the user adds to their
  own `AGENTS.md` supplement the framework; framework changes arrive only as
  proposed diffs.
- **Accepted deviations**: when the user declares a finding intentional,
  record `{"check": ..., "match": ...}` in `.wirenet/accepted.json` — the
  doctor suppresses it from then on and reports only a quiet count. Never
  re-raise an accepted deviation.
- **One nudge per check-in**: the check-in runs the doctor quietly; errors
  always surface, but at most one new soft finding — the most relevant one.
  Never a wall of findings.

## Plugin Updates

- Check for updates only as a bounded public release check: on the first
  check-in of a fresh task or when the user asks — never as hidden polling.
  Reuse the result for the rest of the task.
- If an update exists, show the version and at most three release-note
  bullets, then offer the exact returned update command. Do not run it without
  explicit approval.
- After an approved update, tell the user to start a fresh session. A plugin
  refresh is never approval to migrate or rewrite personal Manager content;
  conventions arriving with a new plugin version are applied dry-run-first as
  their own approved step.

## Retrieval Upkeep

- Refresh or re-embed the `manager` qmd collection only as an explicit
  maintenance action, never implicitly — qmd may own other collections.
- If qmd is unavailable, ordinary Manager work continues through indexes and
  direct reads; mention the limitation only when the user asks about search.

## Boundaries

Maintenance never touches personal prose without approval, never configures
remotes, sync, or automations on its own, and never writes into external
workspaces beyond the approved binding line.
