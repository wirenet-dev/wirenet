# Enterprise Knowledge Platforms: What a File-Based, Agent-First "Base" Should Borrow

## 1. DataHub (open source, LinkedIn lineage)

**Core metadata concepts**
- **Entity / Aspect / URN model**: Entities (Dataset, Dashboard, Chart, DataJob, DataFlow, User, Group, GlossaryTerm, Domain...) are identified by a stable URN (stringified primary key, e.g. `urn:li:dataset:(urn:li:dataPlatform:snowflake,db.schema.table,PROD)`). Metadata is attached as **aspects** — atomic, independently-writable bundles like `Ownership`, `GlobalTags`, `GlossaryTerms`, `InstitutionalMemory` (links to docs), `Status`, `SubTypes`. Aspects are reusable across entity types; the schema is defined in PDL and validated at write time.
- **Relationships**: named edges (`OwnedBy`, `DownstreamOf`) derived from foreign-key fields in aspects, forming a traversable graph; lineage is just a relationship type.
- **Versioned vs. timeseries aspects**: ownership/tags/docs are versioned with a full audit trail; profiles/usage stats are timestamped events.

**Knowledge IN**: a Python ingestion framework with ~70+ source connectors, running push (Kafka/HTTP emit from pipelines) or pull (scheduled crawlers). Everything is a Metadata Change Event flowing through Kafka.

**Knowledge OUT**: search UI, GraphQL/Rest.li APIs, and since 2025 an official **MCP server** (DataHub Cloud v0.3.12+ and self-hosted): search across entity types with filters, fetch any entity's metadata, traverse lineage up/downstream, list SQL queries per dataset. Block (Square) uses it to give coding agents data context.

**What makes it heavy**: 5+ services (React UI, Play frontend, Java GMS, two Kafka consumer apps) plus MySQL + Elasticsearch + Kafka (+ optionally neo4j). Schema-first PDL modeling, entity registry YAML, connector maintenance, event-bus operations. You run a distributed system to store what is, semantically, a few MB of facts.

## 2. Atlan

**Core metadata concepts**
- Asset model derived from Apache Atlas typedefs: assets with owners, descriptions, README, tags, classifications, glossary links, plus **custom metadata** structures scoped per asset type.
- **Certification as a first-class, three-state field**: `VERIFIED` / `DRAFT` / `DEPRECATED` (or empty) — simple, visible trust signal on every asset.
- **Metadata completeness scoring**: assets are scored on whether they have description, owner, certificate, glossary links — gamifying curation.
- **"Active metadata"**: metadata is not documentation but a live control/context plane — changes (deprecation, classification, quality status) propagate outward to consuming tools and agents; agents get the *current* state at inference time rather than a stale copy.

**Knowledge IN**: connector crawlers (warehouses, BI, dbt, orchestrators), bulk import/export via files, automation "playbooks" for enrichment at scale, and now "context agents" that enrich metadata.

**Knowledge OUT**: search/discovery UI, APIs, and the **Atlan MCP server** ("catalog-as-AI-infrastructure"): agents in Claude/Cursor/Copilot search assets, traverse lineage, read glossary definitions, check certification/classification status, even curate metadata back. Positioning shifted in 2025-26 to "the context layer for AI."

**What makes it heavy**: SaaS platform, per-source connectors, access-control policy engine (metadata policies, personas, purposes), workflow orchestration, scoring dashboards — all aimed at large data teams with dedicated stewards.

## 3. Collibra

**Core metadata concepts**
- An **operating model**: Communities → Domains → Assets, with configurable asset types, attributes, and relation types. The org chart is encoded into the catalog.
- **Roles and accountability**: Data Owner (accountable), Data Steward (curates), plus custom roles per domain. Ownership is a governance responsibility, not just a name field.
- **Workflow-driven certification**: asset certification, term approval, access requests, and policy exceptions flow through BPMN-style configurable workflows; certified assets surface in a "Data Marketplace" as trusted-for-reuse.
- Business glossary, policies linked to assets, audit trails, compliance reporting.

**Knowledge IN**: connectors + heavy manual stewardship — stewards document assets, propose terms, run approval workflows. Collibra even runs a human certification program (Steward → "Ranger") because operating the tool is a skill.

**Knowledge OUT**: catalog/marketplace UI, APIs, and a **Collibra MCP server** (2025, incl. Databricks Marketplace listing; 100+ customers): agents query the business glossary, discover governed assets, retrieve asset detail with its governance context. 2026: "AI Command Center" for governing the agents themselves (real-time oversight, Giskard partnership).

**What makes it heavy**: the whole point *is* process — committees, workflows, role matrices, approval chains. Enormous org overhead before the first useful fact is captured; famously requires dedicated staff.

## 4. Glean

**Core metadata concepts**
- A **company knowledge graph** built automatically: nodes are people, documents, messages, tickets, projects; edges are triples like `(person, owns, ticket)` with edge properties for **timestamps, access control, confidence, provenance**. A newer "personal graph" clusters individual activity into tasks/projects.
- Entity importance inferred from evidence (titles, cross-links, access frequency) — no manual curation required.
- **Permissions-native**: ACLs from the source system are attached down to individual facts/edges; every retrieval is permission-trimmed per user from the first millisecond.

**Knowledge IN**: 100+ prebuilt connectors with a real-time crawler continuously ingesting content + metadata + permissions. Zero stewardship: extraction (noun extraction, frequency filtering, link analysis) replaces human curation.

**Knowledge OUT**: hybrid semantic+lexical search, RAG-based assistant with citations back to sources, agent platform (Agentic Engine 2, 2026: adaptive planning, parallel sub-agents), and **managed MCP servers** (Sept 2025 onward; expanded Mar 2026 with "enterprise-ready actions") exposing search/chat/document retrieval/agents to external AI hosts — Glean acts as both MCP server and MCP host, with a directory of 17+ third-party MCP servers behind central governance.

**What makes it heavy**: continuous crawling infrastructure, per-connector permission mirroring, embedding/index pipelines, per-seat SaaS. Its magic (automatic graph) is exactly the part that needs big infra.

## 5. The 2025/2026 MCP convergence

All four now expose their catalog/graph via MCP — the industry consensus is: **the catalog's real customer is now an agent, not a human browsing a UI**. Common MCP tool shapes across all vendors: (1) search assets/knowledge with filters, (2) get one entity with full context, (3) traverse relationships/lineage, (4) look up glossary definitions. That four-tool surface is the de facto standard interface — and it maps cleanly onto `grep`, `cat`, link-following, and a glossary file.

---

## What "Base" should steal (git-based, Markdown-first, agent-maintained)

1. **Stable IDs (URNs) for every entity** — DataHub's key insight. A canonical slug/path per entity (person, project, system, decision, term) that never changes even when files move. In practice: stable filenames + a frontmatter `id:`, so links survive refactors and agents can dereference reliably.
2. **The entity/aspect split — as document sections, not services.** One file per entity; standardized sections/frontmatter keys (`owner`, `status`, `tags`, `links`, `next-steps`) that are individually editable. Reusable aspect vocabulary across entity types (a person and a project both have `owner:`? no — but both have `status:` and `links:`). Agents can patch one aspect without rewriting the doc.
3. **Three-state certification, one field.** Atlan's `verified / draft / deprecated` is the minimum viable trust model: a `status:` frontmatter key plus `verified: 2026-07-21 by chef` line. Cheap to write, and it lets a querying agent weight sources — exactly what the Manager repo's "verified pack" commits already do informally.
4. **Owner as accountability, not decoration.** Collibra's one durable idea: every entity names exactly one accountable human (`owner:`) and optionally a steward (the agent). Staleness questions then have a routing answer.
5. **Typed links = lineage.** Relationships as plain Markdown links with a lightweight verb (`depends-on:`, `supersedes:`, `derived-from:`, `see:` in frontmatter or a Links section). That's the whole lineage graph; `grep` traverses it. Bidirectionality can be computed, not stored.
6. **InstitutionalMemory: point, don't copy.** DataHub's aspect that just holds *links to* canonical docs elsewhere. Base should be a thin index of pointers into external workspaces (matching the existing CLAUDE.md rule: no raw dumps into Manager), not a mirror.
7. **Glossary as a first-class file.** Every platform converged on a business glossary because shared vocabulary is the highest-leverage metadata. A single `GLOSSARY.md` / CONCEPTS.md with one definition per term, linkable by name.
8. **Freshness/provenance stamps on facts.** Glean attaches timestamp + confidence + provenance per edge. Markdown version: `as-of:` dates on volatile claims and git history as the free audit trail (git blame *is* the versioned-aspect store).
9. **The four-tool MCP query surface, locally.** Expose Base exactly the way the vendors' MCP servers do: search (qmd lex/vec already does this), get-entity, follow-links, define-term. No custom API needed — the file system plus a local index is the MCP server.
10. **Completeness scoring as a lint, not a dashboard.** Atlan's completeness score becomes a tiny CI/agent check: every entity file must have owner, status, one-line summary, and a reviewed-date newer than N days — agents fix violations as part of normal maintenance.

## What to explicitly reject

- **Event-bus/service architecture** (Kafka, Elasticsearch, MySQL, GMS, consumer apps): git commits *are* the change events; git log is the audit stream.
- **Connector fleets and continuous crawlers**: the coding agent working in a repo is the connector — it writes back what it learned at the end of a task (push-on-work, not scheduled pull).
- **Workflow engines and approval chains** (Collibra's BPMN certification flows): replace with "human approves the diff" — PR review or the existing preview-before-write rule is the entire workflow engine.
- **Role matrices, communities/domains hierarchy, steward certification programs**: at small scale there is one owner field and git permissions; encoding an org chart into the knowledge base is pure overhead.
- **Per-fact ACL mirroring** (Glean's permission graph): a repo has one trust boundary; if something needs different access, it belongs in a different repo — don't build row-level security in Markdown.
- **Schema-first modeling languages** (PDL typedefs, entity registries): conventions in a `CONVENTIONS.md` plus a lint script beat a type system; let the schema stay social, enforced by the maintaining agent.
- **Embedding/index infrastructure as a hard dependency**: keep search (qmd) as a disposable, rebuildable cache over the files — the Markdown must remain the single source of truth that works with nothing but `grep`.

Sources: [DataHub metadata model](https://docs.datahub.com/docs/metadata-modeling/metadata-model) · [DataHub MCP server](https://docs.datahub.com/docs/features/feature-guides/mcp) · [Block × DataHub MCP](https://datahub.com/blog/datahub-mcp-server-block-ai-agents-use-case/) · [DataHub architecture](https://blog.damavis.com/en/tutorial-datahub-1-architecture/) · [Atlan MCP](https://atlan.com/know/what-is-atlan-mcp/) · [Atlan active metadata for agents](https://atlan.com/know/active-metadata-ai-agent-memory/) · [Atlan metadata completeness](https://docs.atlan.com/product/capabilities/discovery/references/metadata-completeness) · [Atlan custom metadata](https://docs.atlan.com/product/capabilities/governance/custom-metadata/concepts/what-is-custom-metadata) · [Collibra governance overview](https://thedatagovernor.com/what-is-collibra/) · [Collibra MCP server](https://www.collibra.com/blog/enabling-governed-ai-everywhere-with-collibra-model-context-protocol-server) · [Collibra AI Command Center](https://www.collibra.com/company/newsroom/press-releases/collibra-launches-ai-command-center-to-scale-agentic-ai) · [Glean knowledge graph](https://www.glean.com/blog/knowledge-graph-agentic-engine) · [Glean permissions-aware AI](https://www.glean.com/perspectives/security-permissions-aware-ai) · [Glean MCP servers (Sept 2025)](https://www.glean.com/blog/mcp-servers-septdrop-2025) · [Glean MCP actions (Mar 2026)](https://www.glean.com/blog/mcp-mar-drop-2026) · [Glean MCP docs](https://docs.glean.com/administration/platform/mcp/about)