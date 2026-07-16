---
name: simple-html-artifact
description: Build or refine a self-contained, information-first HTML page for a report, brief, explainer, reference, note index, lightweight dashboard, or other static artifact. Use when comprehension and inspection matter more than marketing, application architecture, or a production frontend. Do not use when the request needs a multi-page app, backend, authentication, persistent state, or a framework-specific product implementation.
---

# Simple HTML Artifact

Create one browser-openable HTML file unless the task clearly needs more. Keep
the implementation small enough to inspect, share, archive, and repair without a
build system.

## Frame The Page

Before styling, decide:

- who will read it and what they need to do;
- the one question the page should answer first;
- the best primary surface: prose, comparison, timeline, checklist, map, graph,
  table, or annotated example;
- the visual posture, such as technical reference, editorial brief, field
  guide, museum label, or operating sheet.

Lead with useful information in the first viewport. Do not substitute a large
hero, slogan, or generic call to action for the page's actual subject.

## Organize For Retrieval

Use this reading path by default:

1. title, scope, and a concrete takeaway;
2. the primary working surface;
3. evidence, examples, caveats, or source notes;
4. compact reference material or next actions.

Use a table only when every row shares comparable attributes. Use two columns
only for a real pair such as overview/detail, before/after, claim/evidence, or
controls/results. Use a diagram only when position or connection carries
meaning.

## Implement Simply

- Prefer semantic HTML and a small amount of CSS.
- Use system fonts and native controls unless brand or content requires more.
- Add JavaScript only for a necessary interaction such as filtering, sorting,
  disclosure, copying, or graph selection.
- Avoid package installation, frameworks, build tooling, and application state
  for a static artifact.
- Keep text readable, keyboard order logical, contrast sufficient, and narrow
  screens usable without horizontal overflow.
- Preserve an existing artifact's content and design logic unless those are the
  problem being fixed.

## Avoid Template Drift

Remove generic product-page patterns: gradient heroes, decorative glows,
frosted panels, icon-card grids, invented metrics, vague CTAs, repeated rounded
containers, and charts that imply unsupported precision. Use spacing,
typography, alignment, and one purposeful accent before adding borders or
shadows.

Do not invent examples, percentages, citations, freshness, or completeness to
make the page look finished. Mark assumptions and placeholders explicitly.

## Verify

Before handing off:

1. open the page in a browser;
2. check the first viewport, mobile width, keyboard focus, links, labels, and
   long-content behavior;
3. remove unused JavaScript, placeholder text, decorative structure, and
   repeated visual shells;
4. improve the weakest hierarchy or content decision before polishing color;
5. confirm the result remains a simple artifact rather than an accidental app.
