# ADR 013: The Product Face Is "Manager"

Date: 2026-07-21 · Status: accepted

## Context

ADR 001 named the plugin id `wirenet` for clean Claude Code invocations
(`wirenet:manager`). But the id is not what users read: the ChatGPT app
renders the manifest's `displayName` in the composer mention and on the
plugin tile. "wirenet" tells users who made it; "Manager" tells them what
it is — and the persona duality (the folder and the role share one name)
only pays off if the trigger reads like addressing the role.

## Decision

Split id from face. The id stays `wirenet` (repository, marketplace,
Claude Code prefix — ADR 001 unchanged). The face becomes **Manager**:
`displayName: "Manager"`, developer **WireNet**, the mention `@Manager`,
the greeting "Hi, I'm your Manager." Three naming tiers: WireNet the
company, wirenet the system, Manager the product face (product.md § Naming).

## Consequences

"@Manager, was liegt an?" addresses a role, not a brand — the strongest
reading of the persona model. Claude Code keeps `wirenet:manager`. Flag for
a later public-directory push: "Manager" alone is generic in open search;
for Personal/Workspace distribution (the current channel) that is
irrelevant, and the developer name carries the brand.
