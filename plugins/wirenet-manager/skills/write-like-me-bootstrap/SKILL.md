---
name: write-like-me-bootstrap
description: Create or refresh a global personal write-like-me skill from the user's approved authored email and Slack writing. Use during WireNet Manager onboarding after source access is approved, or when the user asks the Manager to learn their voice, infer writing postures, analyze sent messages, or generate a reusable personal drafting skill.
---

# Write Like Me Bootstrap

Create a reusable personal behavior skill without copying raw private messages
into durable files. This capability is packaged with WireNet Manager because it
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

Read `references/generated-skill-template.md` and
`references/style-profile-template.md` before drafting the files.

## Source Scan

Use only source scopes the user explicitly approved for this purpose. Prefer:

- Slack messages authored by the user in channels, DMs, and group DMs;
- sent email replies, follow-ups, asks, intros, escalations, updates, and admin;
- recent writing, usually the last 90–180 days;
- older evidence only when it clarifies a stable posture.

If a source is unavailable, name the gap and continue with available evidence or
offer to retry later.

## Workflow

1. Identify user-authored messages and separate them by channel and intent.
2. Cluster writing into postures such as quick reply, pushback, delegation,
   status update, email reply, intro, scheduling, and repair.
3. Infer pacing, directness, warmth, humor, formality, asks, tradeoffs,
   disagreement, urgency, recurring moves, and things the user avoids.
4. Preserve differences between channels and audiences.
5. Draft the generated skill and style profile using synthetic examples only.
6. Show a concise posture preview and the exact destination.
7. Ask before creating or updating the global personal skill.
8. After approval, write the files and validate the generated skill with the
   official skill validator when available.

## Privacy And Safety

- Never store raw Slack or email excerpts, names, deals, secrets, account
  details, or private source links in the generated skill.
- Keep source evidence as compact descriptors such as `sent email follow-ups,
  March–June 2026`.
- Treat source reading and writing the generated skill as separate approvals.
- Preview changes before replacing an existing personal style profile.
- Do not install or enable the generated skill without approval when the runtime
  treats that as a separate action.
