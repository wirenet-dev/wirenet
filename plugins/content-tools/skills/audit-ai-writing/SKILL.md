---
name: audit-ai-writing
description: Audit AI-shaped or AI-assisted prose, Markdown, documentation, articles, and chatbot drafts for weak audience modeling, generic filler, unsupported claims, leaked tool residue, placeholders, malformed markup, citation mismatch, and false-positive authorship assumptions. Use when the user asks whether writing sounds like AI, wants an AI-slop audit, needs citations or markup checked, or wants a focused cleanup plan. Edit the source only when the user asks for changes.
---

# AI Writing Audit

Review the text as an editor, not as an AI detector. Find objective quality
problems first and avoid claiming authorship from style alone.

Read `references/review-patterns.md` before auditing a substantial document or
checking citations.

## Review Order

1. **Reader model:** Does the text understand what the audience knows, doubts,
   needs to decide, and should do next?
2. **Substance:** Are claims concrete, scoped, current, and appropriately
   supported?
3. **Writing:** Remove generic scene-setting, inflated significance, empty
   balance, repeated cadence, and abstract filler.
4. **Residue:** Find leaked tool tokens, chatbot framing, placeholders, tracking
   parameters, broken links, and wrong target-format markup.
5. **Sources:** When relevant, verify that sources exist, metadata is accurate,
   and the cited material supports the nearby claim.
6. **Repair:** Recommend the smallest change that improves reader usefulness
   without flattening the writer's voice.

## Findings

Lead with the most consequential findings. For each one, provide:

- issue and exact evidence;
- priority: `P0`, `P1`, or `P2`;
- why it matters to this reader or publication surface;
- a plausible non-AI explanation when relevant;
- the smallest repair;
- confidence and file/line location when available.

Use `P0` for fabricated sources, materially unsupported claims, consequential
quote/number/name errors, or markup that breaks meaning. Use `P1` for recurring
audience failures, claim scaffolding, source drift, or unsupported causal and
quantitative language. Use `P2` for isolated filler, tone, or formatting.

Return a short ranked set rather than cataloging every symptom. Group repeated
instances under their shared cause. Provide a replacement draft only when the
user requests rewriting; otherwise give patch-ready guidance.

## Guardrails

- Do not infer AI authorship from a detector score, formal tone, polished
  grammar, translation artifacts, or a single vocabulary choice.
- Treat weak theory of mind as a document problem, not a psychological claim
  about the writer.
- Distinguish an inaccessible source from a fabricated one. Mark unsupported
  checks as unverified.
- Never invent citations while repairing citation failures.
- Preserve channel, audience, house style, language, and the writer's useful
  idiosyncrasies.
- Do not shame the writer or perform detector-score theater.
