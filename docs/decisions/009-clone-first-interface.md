# ADR 009: Base Access Is Clone-First; MCP Is a Later Transport

Date: 2026-07-21 · Status: accepted

## Context

Two ways to give agents org knowledge: a hosted retrieval service (Glean
model) or a local clone. A curated Base for 50–100 people is 5–50 MB of
Markdown — seconds to clone, milliseconds to pull. What breaks repos is
binaries and mirrored exports, which the Base model forbids.

## Decision

Every member clones the org's Base; setup registers it (with approval) as a
second qmd collection beside `manager`. That yields the industry's converged
four-tool surface with zero infrastructure: search = qmd, get-entity = read
the file, follow-links = grep the verbs, define-term = `GLOSSARY.md`. Offline
is full operation — the clone is the product; answers carry their as-of (last
pull), and pulls ride the approved push-window mechanism. Permissions are the
git host's, deliberately coarse: read = clone, write = PR, certify = the
owner's merge. MCP opens later as a pure transport change — the same four
tools over a server — gated on **both**: a real cloneless consumer exists
(contractor, hosted assistant, mobile), and the gbrain-pilot evaluation has
passed. Service-first is rejected as the foundation: it centralizes
availability, breaks offline, requires auth before the first fact, and logs
what every employee asks — with the clone, questions stay on the device.

## Consequences

No server to run, secure, or bill before the first team works. Freshness is
honest instead of assumed. Query privacy becomes a stated product advantage.
The interface contract is transport-independent from day one.
