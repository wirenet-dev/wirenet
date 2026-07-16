---
name: audit-ai-frontend
description: Audit AI-generated or AI-shaped frontend code, screenshots, and UI diffs for generic visual patterns, component and token drift, one-off CSS, hard-coded fixture screens, weak responsive behavior, inaccessible interaction, brittle layout, poor copy, and missing reuse. Use when the user asks to de-slop a UI, review frontend architecture, improve responsiveness or accessibility, componentize a screen, or align an implementation with an existing design system. Diagnose first; edit only when requested.
---

# AI Frontend Audit

Inspect the running interface or screenshots together with the relevant code.
Read the project's design primitives and conventions before proposing a new
system.

## Review

Check:

1. whether the page serves the reader's primary job and presents real content
   before decoration;
2. reuse of existing components, tokens, spacing, typography, and interaction
   patterns;
3. hard-coded data, repeated markup, oversized page components, boolean-prop
   sprawl, and CSS that should be a reusable primitive;
4. keyboard navigation, focus, semantics, labels, contrast, touch targets, and
   reduced-motion behavior;
5. narrow and wide viewport resilience, text expansion, overflow, empty states,
   loading, errors, and realistic content volume;
6. generic AI aesthetics such as decorative gradients, excessive cards,
   arbitrary icons, invented metrics, vague copy, and visual hierarchy made
   entirely from borders.

## Findings

Lead with the highest-impact issues and point to the smallest relevant code
range or visual region. Explain the user-facing consequence and the smallest
repair that fits the existing system. Distinguish taste from accessibility,
correctness, and maintainability. When asked to implement, verify the result in
the browser at representative viewport sizes.
