---
last_edited: 2026-06-15
---

# Agent Asset Instructions

This directory contains repo-local skills, plugin metadata, and assets. Use skills in place; do not copy them into global tool state unless the user explicitly asks.

## Skills

`skills/` contains Codex-style skills with `SKILL.md` entrypoints. Read the selected skill before using any scripts or references inside it.

Keep skill frontmatter limited to:

- `name`
- `description`
- `last_edited`

Use natural trigger phrases in the description because the description is the recall surface.
