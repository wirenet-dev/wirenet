---
last_edited: 2026-07-16
---

# Generated Write-Like-Me Skill Shape

Create `~/.agents/skills/write-like-me/SKILL.md` with this compact contract:

```md
---
name: write-like-me
description: Draft, rewrite, critique, or reply in the user's personal writing voice across email, chat, updates, intros, pushback, delegation, and scheduling. Use when the user asks to write like them, make text sound like them, draft a reply, critique voice fit, or select the right posture for a message.
---

# Write Like Me

Read `references/style-profile.md` before drafting, rewriting, or critiquing.

1. Identify the channel and audience.
2. Select the closest writing posture.
3. Draft in that posture.
4. Ask only when goal, audience, channel, or stakes would materially change it.
5. For critique, identify what feels unlike the user and provide a tighter rewrite.

Never reveal private source messages. Default to useful copy rather than style
analysis. When the user corrects the voice, update the profile after approval.
```

Create matching `agents/openai.yaml` metadata with a short, drafting-oriented
description and default prompt.
