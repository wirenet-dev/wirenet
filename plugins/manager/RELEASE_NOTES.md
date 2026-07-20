---
last_edited: 2026-07-20
---

# wirenet Manager v0.4.4

- Manager and Doctor can check the latest published stable release without
  changing the local workspace, and wrapped GitHub notes are now presented as
  complete sentences.
- An available update is shown with concise user-facing notes and requires
  approval before the Marketplace is refreshed.
- After an update, `$manager-setup` reports the installed version, any approved
  workspace migration, and the final Doctor result.
- Workspace `plugin_version` now explicitly records the plugin version that
  created or last structurally migrated the workspace; update availability uses
  the installed plugin manifest instead.
