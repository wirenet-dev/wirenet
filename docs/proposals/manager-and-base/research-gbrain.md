# GBrain — Summary

## What it is
GBrain (source: `/Users/gitt/Developer/gbrain`) is an open-source "brain layer" for AI agents, built by Garry Tan (YC). It is a personal/organizational knowledge system that goes beyond retrieval: markdown pages in a git repo ("brain repo") are synced into Postgres (PGLite locally, or Postgres+pgvector at scale) and exposed to agents via CLI and MCP (30+ tools). Its three signature capabilities, shipped together in one box:

- **Synthesis layer** (`gbrain think`): returns a cited, composed answer rather than a list of chunks, with explicit **gap analysis** — what the brain does *not* know, what is stale, what contradicts.
- **Self-wiring knowledge graph**: every page write extracts entity refs/wikilinks into typed edges (`works_at`, `attended`, `invested_in`, …) with zero LLM calls; graph traversal gives a benchmarked +31.4 P@5 lift over vector-only RAG.
- **Autonomous "dream cycle"**: cron-driven overnight ingestion, enrichment, dedup, citation fixing, contradiction detection via a Postgres-native job queue ("Minions"), plus 43 agent skills and schema packs so the brain's page-type taxonomy can adapt to (or be learned from) the user's actual filesystem.

Hybrid search combines vector + BM25 + RRF + reranker + graph signals, with per-stage `--explain` attribution and an eval framework (LongMemEval, BrainBench, retrieval-quality CI gates).

## Goal of the local pilot
The Manager experiment (`/Users/gitt/Manager/experiments/gbrain-pilot/README.md`, active, created 2026-07-18) asks one bounded question: **does an isolated GBrain pilot improve synthesis, graph recall, or gap analysis compared to QMD** (the existing local markdown search engine), without touching canonical knowledge sources? Decision criterion: only continue/promote if documented tasks show clear benefit over QMD *and* privacy, restore, and isolation checks pass. The [WireNet Client Runtime] project is noted as the future product-relevance link.

## Current state
- GBrain is installed at a pinned detached commit (repo checked out 2026-07-13).
- No Postgres instance yet; backend choice and search mode (keyword-only vs. model-backed) are open decisions.
- Next move: pick a backend and a cheap first search mode, then define a small vetted corpus and 15–25 representative questions.
- Hard safety bounds (`AGENTS.md`): single local user, isolated runtime, copied/vetted markdown sub-corpus only; **no** live Manager/vault paths, Gmail, Calendar, Drive, or client data; HTTP loopback-only until auth/backup/isolation tests pass; DB, models, paid search, and extra users each require separate approval.

## Relationship to organizational knowledge access
GBrain explicitly positions itself as a **company brain**, not just a personal one:

- **Per-user scoping**: each team member gets a login-scoped slice; queries only return what that user is allowed to see, fuzz-tested across all read paths (search, list, lookup, multi-source reads) with zero leaks claimed.
- **Federated multi-user setup**: OAuth 2.1 (PKCE, DCR-style client registration), scope-gated access (`read`/`write`/`admin`), rate limiting; a company-brain tutorial targets 10–50 person teams (~90 min setup).
- **Brain ⊥ source axes**: a *brain* is a database (personal brain, or a team mount you joined); a *source* is a repo inside it. You can publish public subsets, share team mounts, or run thin clients against a colleague's brain server — a model for layering personal and shared organizational knowledge in one system.
- **Cross-source boost**: search signals include corroboration across team brains.

## Ideas relevant for pairing a personal agent-maintained memory folder with an organizational KB
1. **System of record stays markdown-in-git; the DB is a derived index.** The canonical knowledge remains plain files (like `~/Manager`); GBrain syncs, never owns. This maps directly onto keeping the Manager folder canonical while any retrieval layer stays disposable/rebuildable.
2. **Brain vs. source separation**: personal memory folder = one source; organizational KB = another source or a mounted team brain; both queryable through one interface with clear routing (`.gbrain-source` dotfiles, documented precedence chain).
3. **Per-user access scoping at the retrieval layer**, so a shared org brain and a private personal brain can coexist without leakage — the key trust primitive for personal+org pairing.
4. **Gap analysis as a first-class output**: answers state what the memory does *not* cover and which channels it cannot see — exactly the failure mode of a personal memory folder next to a larger org KB (stale or missing context flagged instead of silently wrong).
5. **Typed-edge auto-linking with zero LLM cost**: entity graphs (people, companies, projects) built from wikilinks on every write; enables "who works on X / what's open with Y" queries a folder full of markdown plus vector search cannot answer.
6. **Schema packs / agent-authored schema**: the taxonomy adapts to the folder's actual structure (`schema detect/suggest/review-candidates`) rather than forcing a layout — relevant for indexing an existing Manager-style folder without restructuring it.
7. **Thin-client / team-mount topology**: a personal agent can hold its own local brain and additionally mount the org KB read-scoped over MCP — one query surface, two ownership domains.
8. **Cron consolidation ("dream cycle")**: agent-maintained memory needs maintenance (dedup, citation repair, contradiction checks) as scheduled background work, not ad-hoc chat effort.
9. **Evaluation-before-adoption pattern** (from the pilot itself): compare against the incumbent (QMD) on a fixed vetted corpus with 15–25 representative questions and explicit privacy/restore/isolation gates before any canonical source is connected.

Key files: `/Users/gitt/Manager/experiments/gbrain-pilot/README.md`, `/Users/gitt/Manager/experiments/gbrain-pilot/AGENTS.md`, `/Users/gitt/Developer/gbrain/README.md` (notably sections "What this looks like", "Your brain's shape", "Capabilities", "Architecture"), `docs/tutorials/company-brain.md`, `docs/architecture/brains-and-sources.md`, `docs/architecture/topologies.md`.