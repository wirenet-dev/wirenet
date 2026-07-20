---
last_edited: 2026-07-20
---

# wirenet Manager v0.4.6

- New Project and Experiment Pack concepts now use one metadata field per
  durable meaning. Redundant scope aliases, per-concept `okf_profile`, `name`,
  and `summary` are gone; standard OKF `title` and `description` serve indexes,
  search, and display consistently.
- New `scripts/tidy_frontmatter.py` safely normalizes existing packets after a
  clean Git checkpoint. It previews affected files, preserves personal prose
  and unknown producer metadata, and requires a healthy Manager Doctor result.
- Onboarding can keep awareness, semantic commits, and safe push windows in one
  current Manager task instead of requiring a separate push automation.
