# Proposal: Flexibility and the Org Knowledge Interface

> **Status:** decided 2026-07-21 — see ADR 007–009 and 011. Kept as provenance, no longer living.

Status: draft for review · Author: agent, for the wirenet product owner · Date: 2026-07-21
Governing baseline: `docs/core-contract.md` (v0.5), `docs/product.md`, ADRs 003–004.

## Summary

Two recommendations, one per problem:

1. **Flexibility: add one container — `areas/<slug>/` — and nothing else.** Every mature system that survived contact with real life (PARA, GTD, org-mode, Notion practice) grew an explicit home for *ongoing responsibilities with a standard to maintain but no end date*. The Manager today is Projects + Resources + Archive with no Area, and the strain is already live (a "Personal Finance" pack that can never complete; the Base/Shelf carve-out). Areas sit flat and parallel to projects, own their routines and maintained references, and are admitted by a single decidable test: **"Does it end?"** No frontmatter typing — location stays the type, per ADR 004. Migration is moving about two packs.

2. **Org interface: the Base is a second git repo of typed Markdown entities, consumed by cloning it locally and indexing it as a second qmd collection.** Borrow exactly four ideas from enterprise catalogs — stable IDs, one accountable owner per entity, three-state certification (`verified/draft/deprecated`), typed links — expressed as minimal frontmatter plus conventions, validated by a doctor. Certification is a reviewed git merge; the PR *is* the workflow engine. MCP becomes the cross-boundary access path later, exposing the same four-tool surface (search, get-entity, follow-links, define-term) the entire catalog industry converged on in 2025/26. Personal layer stays prose; typing returns only here, exactly as ADR 004 anticipates.

## The Flexibility Model

### The container model (recommended)

Keep the v0.5 tree and add one lazily-created top-level folder:

```text
areas/<slug>/
├── README.md            required: what "healthy" means, current state vs that
│                        standard, related projects, review cadence
├── routines/<name>.md   optional: procedures/checklists this area owns
└── reference/…          optional: curated material this area maintains
```

Routing becomes a short decision sequence with exactly one legal answer per item — the property that makes agent routing reliable:

| Question (asked in order) | Target |
|---|---|
| Ends with a defined outcome? | `projects/<slug>/` |
| Bounded question with a decision criterion? | `experiments/<slug>/` |
| Responsibility with a standard to maintain, no end? | `areas/<slug>/` |
| Repeatable procedure? | `routines/` of its owning area or project |
| About a person? | `people/` |
| Evidence backing a claim or decision? | `sources/` |
| Cross-project profile or structured doc? | `docs/` |
| Durable, none of the above? | `notes/` (now genuinely residual) |

Consequences and sharpened rules:

- **`projects/` admission tightens**: a pack without a completion state is rejected toward `areas/` — no more zombie packs whose "done when" is meaningless. Areas never archive; projects do. This keeps `archive/` meaningful and lets staleness heuristics differ (an idle area is normal; an idle active project is a finding).
- **Areas spawn projects** (PARA's key dynamic): "Health" is an area; "run a half-marathon in October" is a project. The project README links its parent area in prose ("Part of [Personal Finance](../../areas/personal-finance/)"); status lives only in the project, per one-fact-one-home.
- **Procedural memory lives with its owner**, not in a central `procedures/` folder — answering "how do I run the finance close?" must not require joining two containers. Run *logs* stay transient in `outputs/`.
- **`people/` drops the work-only scope.** Every durable relationship qualifies; work vs. family is prose in the file, not a routing rule. The current scope quietly erodes anyway.
- **`TODO.md` gains a final `## Someday` section** — GTD's pressure valve. The Now/Next/Waiting/Later stack stays committed-only; uncommitted ideas get a home that isn't `notes/`.
- **Learning threads** take the same test: bounded ("learn enough Rust to port the doctor") → project or experiment; open-ended ("get deeper into Rust") → area with a curriculum.
- **Catalog**: `projects/index.md` remains the only portfolio catalog and gains an **Ongoing** group listing area packs. One catalog, one read, full portfolio — no second index file.

**No status enums, no `type:` frontmatter, no IDs** — the container *is* the type, exactly as the v0.5 contract expresses lifecycle by location and grouping.

### Alternatives rejected

- **Reinterpret `projects/` via frontmatter (`type: area`)** — hides the single most routing-relevant fact inside files, overloads `docs/`, and teaches the agent that admission tests are soft. Rejected.
- **Full lifecycle-typed root (areas contain their projects; central `library/`, `journal/`, `procedures/`)** — reintroduces "which area owns this cross-cutting project?", invalidates every existing link, adds admission tests to get wrong. High ceremony, marginal gain. Rejected.

### Migration-light path

`areas/` joins the created-lazily list — no placeholder, no seeded content. Existing vaults migrate by `git mv` of the one or two misfiled packs (e.g. `projects/personal-finance/` → `areas/personal-finance/`) and re-grouping their index entries under **Ongoing**; the doctor proposes these moves as staleness-style findings, dry-run-first, approval-gated. Vaults that never need areas never see the folder.

## The Base Architecture

The Base is **a per-organization git repository of Markdown entity files** — a thin, typed index of what the org knows and who vouches for it. It points at canonical sources; it does not mirror them (DataHub's InstitutionalMemory insight, and the existing "no raw dumps" rule).

### Metadata model

Entity kind is the directory; each entity is one file:

```text
base/
├── README.md            what this Base covers, how to propose changes
├── GLOSSARY.md          one definition per term — the highest-leverage file
├── systems/<slug>.md    services, tools, repos, datasets
├── guides/<slug>.md     how-we-do-things (org-level procedures)
├── decisions/<slug>.md  org-level decisions with rationale
├── people/<slug>.md     roles and ownership context (org-visible facts only)
└── .wirenet/            machine state, derived indexes — never authored
```

Typing returns here — minimal, enforced frontmatter (four keys, no more):

```yaml
id: payments-service        # stable; survives file moves
owner: chef@gitthub.org     # exactly one accountable human (Collibra's one durable idea)
status: verified            # verified | draft | deprecated (Atlan's three states)
reviewed: 2026-07-21        # last human review date
```

Everything else is prose plus conventions: typed links as a `## Links` section with lightweight verbs (`depends-on:`, `supersedes:`, `see:`) — that *is* the lineage graph, traversable by grep; `as-of:` dates in prose on volatile claims; git blame as the free per-aspect audit trail. This satisfies ADR 003: the frontmatter schema lives in `contracts/` because the Base doctor actually enforces it.

### Certification and ownership

- **Certification is a merge.** Agents and members propose changes as branches/PRs; the entity's `owner` merges. Merging a change that sets `status: verified` and today's `reviewed` date *is* the certification act. No BPMN, no committees — "human approves the diff" is the entire workflow engine, which is already wirenet's approval-gate primitive at team scale.
- **Completeness is a lint, not a dashboard** (Atlan's score, shrunk): the Base doctor flags entities missing an owner, a one-line summary, or a `reviewed` date older than N days, and flags dangling links. Report-only; fixes are proposals.
- **Push-on-work, not crawlers**: the coding agent finishing a task in an org repo is the connector — it proposes the Base delta it just learned (a new dependency, a deprecation, a decision), same threshold discipline as the Manager's update contract.

### Sync boundaries: personal vs shared

- The Manager **references** Base entities (a link in a pack README); it never copies them. The Base **never reads** the Manager. Promotion of personal knowledge to the Base is always an explicit, human-approved PR — there is no automatic upward sync.
- One repo, one trust boundary. Content needing different access lives in a different Base repo — no row-level security in Markdown.

## The Interface

**Recommended: local clone + qmd, from day one.** Each member clones the org's Base; onboarding registers it as a second qmd collection (this proposal's own environment already runs `manager` + `base` collections — the pattern is proven). The personal agent then has the industry-standard four-tool surface with zero new infrastructure: **search** = qmd over the `base` collection; **get-entity** = read the file; **follow-links** = grep the Links verbs; **define-term** = `GLOSSARY.md`. Canonical Markdown beats a stale index, same rule as the Manager.

- **Offline**: fully functional — the clone is the product. Freshness is the last `git pull`; the agent treats pull-time as the Base's `as-of` and says so when answering from a stale clone. Pulls piggyback on the existing safe-push-window mechanism, separately approved.
- **Permissions**: git-host access control on the repo, nothing finer. Read access = clone access. Write access = PR rights; certification rights = merge rights of the owner. This is deliberately coarse and deliberately auditable.
- **MCP later, for cross-boundary access**: when a Base must serve people or agents who cannot hold a clone (contractors, other orgs, a hosted WireNet offering), stand up an MCP server exposing exactly the same four tools over the same repo — the interface contract doesn't change, only the transport. GBrain's thin-client/team-mount topology and per-user scoping are the reference design here, and the running gbrain-pilot experiment is the evaluation gate before any such server touches canonical knowledge (evaluation-before-adoption, fixed corpus, privacy/isolation checks).

Alternative rejected as primary: **MCP-service-first** (Glean model). It centralizes availability, breaks offline, requires auth infrastructure before the first fact is captured, and contradicts local-first. It is the extension, not the foundation.

## What We Deliberately Reject

- **Event-bus/service stacks** (Kafka, Elasticsearch, GMS, consumer apps): git commits are the change events; `git log` is the audit stream.
- **Connector fleets and continuous crawlers**: the working agent is the connector; capture is push-on-work.
- **Workflow engines and approval chains**: PR review replaces BPMN certification flows entirely.
- **Role matrices, communities/domains hierarchies, steward certification programs**: one `owner` field plus git permissions; encoding an org chart into the knowledge base is pure overhead at our scale.
- **Per-fact ACL mirroring** (Glean's permission graph): repo = boundary; split repos instead.
- **Schema-first modeling languages** (PDL, entity registries): four frontmatter keys enforced by a doctor, everything else conventions — the schema stays social except where code validates it (ADR 003).
- **Search infrastructure as a hard dependency**: qmd stays a disposable, rebuildable sidecar; the Base must work with nothing but `grep`.
- **Always-on daemons in the personal core**: no server process; the survey's server-dependent systems (ai-memory, context-vault) are the cautionary tales.
- **Activity logs and transcript capture**: durable meaning only, both layers.

## Open Questions

1. **Base bootstrap for the first client team (six individuals)**: seed from an interview like `$manager-setup`, or grow purely push-on-work from their existing Manager usage? Leaning push-on-work with a one-session seeded `GLOSSARY.md`.
2. **Person identity across layers**: how does `people/anna.md` in a Manager relate to `people/anna.md` in the Base — link by slug convention, or leave unlinked until it hurts?
3. **Owner unavailability**: what happens to certification when an entity's owner leaves or stalls — a fallback owner field, or org policy outside the repo?
4. **Area review cadence**: should the doctor nudge area reviews on a per-area cadence (stated in the area README), or is the 90-day staleness heuristic enough? Leaning per-area cadence, since "idle is normal" makes the generic heuristic blind.
5. **Shelf coupling**: does the Shelf live inside the Base repo or beside it? Leaning beside (skills are installable artifacts with releases; knowledge is not), but the certification model should be shared.
6. **MCP trigger condition**: define the concrete demand signal (first cloneless consumer) that opens the MCP layer, so it isn't built speculatively.

## Impact on v0.5

**Change now (small, additive, contract-safe in spirit but requires contract edits):**

1. Add `areas/<slug>/` to the contract's created-lazily list; define its meaning and the "does it end?" routing test in the `$manager` skill's `vault-model.md` reference. One new folder, no new frontmatter, no migration for existing v0.5 vaults — consistent with "grow on first use".
2. Tighten the `projects/` admission test ("has a completion state") and add the **Ongoing** group to `projects/index.md` semantics.
3. Add the `## Someday` section to `TODO.md`'s definition.
4. Widen `people/` scope wording from work-relevant to durable relationships.
5. Extend the doctor: propose (never perform) project→area reclassification for packs with no completion state.

**Change later (separate layer contracts, per the existing Optional Layers clause):**

6. A `base-contract.md` defining the Base repo model above — the "Base/Shelf synchronization" layer the core contract already reserves. Includes the four-key frontmatter schema in `contracts/` (ADR 003-compliant) and the Base doctor.
7. qmd multi-collection registration (`manager` + one collection per cloned Base) as an onboarding option in that layer.
8. An MCP access layer, gated on Open Question 6 and on the gbrain-pilot evaluation outcome.

**Explicitly unchanged:** ADR 004 stands and is strengthened — the personal core gains zero frontmatter from this proposal; typing appears only in the shared Base layer, which is the exact boundary the ADR drew.