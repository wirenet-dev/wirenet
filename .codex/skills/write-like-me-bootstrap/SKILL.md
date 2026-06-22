---
name: write-like-me-bootstrap
description: Bootstrap a durable "write like me" skill from the user's own Slack and email writing. Use during Assistant onboarding, after Slack/Gmail or email connectors are available, or when the user asks to learn their voice, infer writing style, create a personal writing persona, generate a write-like-me skill, analyze sent messages, or capture different writing postures across email and Slack.
last_edited: 2026-06-15
---

# Write Like Me Bootstrap

Create or update a repo-local writing-style skill from the user's real authored
messages. The output should help future assistants draft in the user's voice
without copying raw private messages into durable files.

## Default Output

Write the generated skill to `.codex/skills/write-like-me/` unless the user asks
for a different name. Use:

- `.codex/skills/write-like-me/SKILL.md` for the durable drafting workflow
- `.codex/skills/write-like-me/references/style-profile.md` for compact voice, posture, and examples
- `.codex/skills/write-like-me/agents/openai.yaml` if the repo uses skill UI metadata

Use `references/style-profile-template.md` as the target shape.
Use `references/generated-skill-template.md` as the starting shape for the
generated `SKILL.md`.

## Source Scan

Use connected Slack and email sources when available. Prefer authored messages:

- Slack messages sent by the user in channels, DMs, and group DMs
- sent email, replies, follow-ups, scheduling notes, intros, escalations, and updates
- recent enough writing to reflect the current voice, usually the last 90-180 days
- older writing only when it clarifies stable style or an important posture

If a connector is unavailable, say what is missing and proceed with available
sources or ask whether to retry later.

## Privacy Boundary

Do not save raw Slack or email excerpts in durable files. Use short synthetic
examples that preserve style without exposing private content, names, deals,
secrets, or account details. Keep source evidence as compact descriptors such as
`sent email follow-ups, March-June 2026` or `Slack replies in project channels`.

Ask before writing or updating the generated skill. Reading connected context for
this bootstrap is allowed only when the user has asked for onboarding or this
skill, and writing still requires explicit approval.

## Analysis Workflow

1. Identify the user's authored messages and separate them by channel and intent.
2. Cluster writing into postures rather than one generic voice. Useful default
   postures:
   - quick Slack reply
   - decision or pushback
   - delegation or ask
   - executive/status update
   - email reply
   - intro or relationship note
   - scheduling/admin note
   - apology, correction, or repair
3. For each posture, infer:
   - when to use it
   - sentence length and pacing
   - directness, warmth, humor, and formality
   - how the user frames asks, tradeoffs, disagreement, and urgency
   - phrases or moves to reuse as patterns, not verbatim quotes
   - things the user avoids
4. Compare Slack and email. Preserve differences instead of flattening them.
5. Draft the generated `write-like-me` skill and profile.
6. Present a concise preview of the inferred postures and ask for approval before
   writing files.
7. After approval, create or update the generated skill in this repo.

## Generated Skill Requirements

The generated `write-like-me` skill should:

- trigger for drafting, rewriting, critiquing, or replying in the user's voice
- route by channel and posture before drafting
- ask only when audience, channel, or goal would materially change the draft
- default to concise, useful drafts rather than style analysis
- include a critique mode that says what feels unlike the user
- preserve privacy by never revealing the source messages used for bootstrapping
- tell future assistants to update the profile when the user corrects voice,
  posture, or audience assumptions

## Onboarding Behavior

During Assistant onboarding, suggest this bootstrap after the first connected
Slack/email scan finds enough authored writing to infer voice. The offer should
be concrete:

```text
I can also bootstrap a write-like-me skill from your sent email and Slack messages, split by posture like quick replies, pushback, delegation, intros, and status updates. Want me to do that?
```

If the user says yes, run the source scan, show the posture preview, and ask
before writing the generated skill.
