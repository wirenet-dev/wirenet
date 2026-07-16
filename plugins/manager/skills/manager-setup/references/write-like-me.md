---
last_edited: 2026-07-16
---

# Personal Write-Like-Me Setup

Create a reusable personal behavior skill without copying raw private messages
into durable files. This capability is packaged with wirenet Manager because it
is part of the first-meeting experience, but its generated output is personal
global behavior rather than Manager knowledge.

## Default Output

Write the generated skill to `~/.agents/skills/write-like-me/` unless the user
chooses another global skill root. Never place it inside `~/Manager`: Manager
holds portable knowledge and runtime routing, not generated behavior.

Use:

- `SKILL.md` for the drafting workflow;
- `references/style-profile.md` for compact voice and posture guidance;
- `agents/openai.yaml` for skill UI metadata.

Read `write-like-me-skill-template.md` and
`write-like-me-profile-template.md` before drafting the files.

## Existing Skill First

1. Check `~/.agents/skills/write-like-me/` before proposing generation.
2. Inspect only the current workspace and other user-approved project roots for
   existing `.agents/skills/write-like-me/` or legacy
   `.codex/skills/write-like-me/` profiles. Never scan the whole home directory.
3. If a global skill exists, validate it and offer a focused refresh only when
   new evidence or user corrections justify one.
4. If only a repo-local profile exists, offer to migrate it to the global path.
   Preserve its grounded style profile and synthetic examples, normalize its
   `SKILL.md` to current official frontmatter, and preview the destination diff.
5. Never overwrite or silently merge an existing global profile. Ask which
   version should remain canonical when two profiles differ materially.

## Source Scan

Use only source scopes the user explicitly approved for this purpose. Prefer:

- Slack messages authored by the user in channels, DMs, and group DMs;
- sent email replies, follow-ups, asks, intros, escalations, updates, and admin;
- recent writing, usually the last 90–180 days;
- older evidence only when it clarifies a stable posture.

If a source is unavailable, name the gap and continue with available evidence or
offer to retry later.

## Workflow

1. Resolve whether this is a reuse, migration, refresh, or fresh source scan.
2. For a fresh scan or evidence-backed refresh, identify user-authored messages
   and separate them by channel and intent.
3. Cluster writing into postures such as quick reply, pushback, delegation,
   status update, email reply, intro, scheduling, and repair.
4. Infer pacing, directness, warmth, humor, formality, asks, tradeoffs,
   disagreement, urgency, recurring moves, and things the user avoids.
5. Preserve differences between channels and audiences.
6. Draft the generated skill and style profile using synthetic examples only.
7. Show a concise posture preview and the exact destination.
8. Ask before creating or updating the global personal skill.
9. After approval, write the files and validate the generated skill with the
   official skill validator when available.

## Privacy And Safety

- Never store raw Slack or email excerpts, names, deals, secrets, account
  details, or private source links in the generated skill.
- Keep source evidence as compact descriptors such as `sent email follow-ups,
  March–June 2026`.
- Treat source reading and writing the generated skill as separate approvals.
- Preview changes before replacing an existing personal style profile.
- Keep only current official `SKILL.md` frontmatter fields; do not carry legacy
  `last_edited` metadata into a migrated skill.
- Do not install or enable the generated skill without approval when the runtime
  treats that as a separate action.
