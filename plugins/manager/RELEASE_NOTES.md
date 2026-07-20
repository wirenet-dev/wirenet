---
last_edited: 2026-07-20
---

# wirenet Manager v0.4.5

- Project and Experiment Pack concepts, and their packet-level `AGENTS.md`
  sidecars, now use only `created_at` and `updated_at` in frontmatter. The
  redundant `timestamp` and `last_edited` fields — always set to the same
  value as the others — are gone from newly generated content.
- New `scripts/tidy_timestamps.py` removes those redundant fields from
  existing packets: preview, clean Git checkpoint, apply, Doctor-valid,
  idempotent. `$manager-setup` offers it once Doctor is healthy.
