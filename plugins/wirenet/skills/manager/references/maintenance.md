# Maintenance

Ongoing health, plugin updates, and retrieval upkeep. Setup runs once via
`$manager-setup`; everything recurring lives here.

## Health

- Run the plugin doctor when the user reports something broken, after
  structural moves (create, archive, promote, rebind), or before a release
  demo. It checks: every pack has a resolving `projects/index.md` entry,
  bindings resolve to existing paths, no seeded empty placeholders, no
  archived pack carrying new active state.
- Fix findings as previewed proposals, smallest diff first. If the vault is
  missing or structurally broken beyond small fixes, hand off to
  `$manager-setup` in repair mode instead of improvising structure.

## Plugin Updates

- Check for updates only as a bounded public release check: on the first
  check-in of a fresh task or when the user asks — never as hidden polling.
  Reuse the result for the rest of the task.
- If an update exists, show the version and at most three release-note
  bullets, then offer the exact returned update command. Do not run it without
  explicit approval.
- After an approved update, tell the user to start a fresh session. A plugin
  refresh is never approval to migrate or rewrite personal vault content;
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
