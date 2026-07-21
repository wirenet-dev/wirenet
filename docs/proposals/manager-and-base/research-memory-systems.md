# Agent-Memory Systems: Structure & Conventions Survey

## 1. akitaonrails/ai-memory (cross-vendor handoff)

**Structure**
```
<data_dir>/
├── wiki/    # markdown source of truth, git-versioned; <wiki_root>/<workspace_id>/<project_id>/…
├── raw/     # immutable sanitized transcript segments
├── db/      # SQLite (FTS5 + embeddings)
├── models/  # local embedding models
└── logs/
```
A `.ai-memory.toml` marker in ancestor directories pins workspace/project identity (stable UUIDs).

**Write triggers / policy** — Automatic: lifecycle hooks (prompt, tool events, session boundaries) fire-and-forget; PreCompact triggers optional LLM consolidation; session end always writes rule-based summary pages + handoffs even without an LLM. Manual: `memory_write_page`, with `--pinned` exempting a page from decay. Per-repo `ignore_paths` filters capture.

**Index/retrieval** — FTS5 over the compiled wiki + graph-neighbor RRF + optional vector RRF; a Rust server serializes all writes through one SQLite writer; agents access via MCP/HTTP. SessionStart hooks inject pending handoffs before the first prompt.

**Staleness/hygiene** — The richest of any system surveyed: background auto-improvement scheduler reviews completed sessions per project (watermarks + per-session claims prevent rework); a rule-based "curator" reports stale slots, duplicate titles, dangling links (report-only by default, `--stage` queues an approval proposal); decay sweep removes unpinned auto-captured pages; `require_approval = true` gates proposals.

**Does well** — Typed cross-vendor handoffs (summary, open questions, next steps) injected into the next session of a *different* agent CLI (Claude Code, Codex, Cursor, Gemini CLI, etc.), plus a zero-LLM fallback path.
**Weakness** — Requires an always-on server process; some agents discard sessionStart stdout so handoffs need a manual MCP call; heavyweight compared to plain files.

## 2. MihaiBuilds/memory-vault

**Structure** — Not a file-layout system: a Python service (`src/memory_vault/`, `web/` dashboard, Docker). Memories live in Postgres as chunks, not user-visible files.

**Write triggers / policy** — Fully manual/explicit: CLI `memory-vault ingest file.md`, REST `/api/ingest/*`, MCP `remember` tool, dashboard upload. Async queue-based ingestion; versioned, forward-only migrations.

**Index/retrieval** — Hybrid: pgvector HNSW (384-dim MiniLM embeddings) + Postgres tsvector/GIN full-text, merged with Reciprocal Rank Fusion; query enrichment generates up to 3 query variations. MCP tools: `recall`, `remember`, `forget`, `memory_status`.

**Staleness/hygiene** — Soft-delete only (`forget`); entities deduped by `(lower(name), type, space)`; no automatic cleanup — re-ingesting a corrected chunk leaves old extracted entities orphaned.

**Does well** — Everything in one Postgres instance (vectors + FTS + relations + knowledge graph), CPU-only, and every dashboard answer cites the exact source memories.
**Weakness** — Opaque storage (DB, not markdown/git), no auto-capture, English-only NER, no alias merging ("Postgres" ≠ "PostgreSQL"), no cleanup after deletes.

## 3. jaredrhod/ai-memory-vault (Obsidian)

**Structure** — Template-driven Obsidian vault:
- `CLAUDE.md` — boot config, deliberately kept *outside* the vault in the Claude Code working dir
- `VAULT-INDEX.md` — operating manual, inside the vault
- `01 - Daily Notes/Daily Note Template.md` — numbered-folder convention; daily notes
- `MEMORY.md` — pointer file in `~/.claude/projects/...`
- Folders organized around real projects, plus a profile note and "Jobs" (recurring-task definitions)

**Write triggers / policy** — Interview-driven bootstrap: templates ship with `[FILL IN: ...]` markers the AI populates by interviewing the user; daily notes "write themselves"; profile updates as the AI learns; jobs tie updates to recurring tasks.

**Index/retrieval** — "AI Priming": the vault declares which notes to read for which job (e.g., before writing a marketing email, read copywriting notes + customer avatar + company KB). No search index, no vectors — pre-configured mappings only.

**Staleness/hygiene** — Essentially undocumented; claimed "self-maintaining" with no concrete mechanism.

**Does well** — Job-to-notes priming: an explicit, human-auditable statement of *which* context each task class needs — cheap and highly predictable.
**Weakness** — No retrieval fallback when a task doesn't match a configured job; mappings are manual and won't scale to large vaults.

## 4. fellanH/context-vault

(Main repo now returns 404 on GitHub/API — apparently taken private; findings from context-vault.com docs and cached descriptions: "markdown + SQLite + embeddings, local-first, via MCP.")

**Structure** — Plain markdown files in user-controlled, git-versionable folders; memory *kinds* — `insight`, `decision`, `pattern`, `reference`, `event`/`contact` — with custom kinds derived from vault subdirectory names (folder = category). Entries carry a `bucket:<project>` tag for namespacing and a two-tier level: `working` (active context) vs `durable` (long-term).

**Write triggers / policy** — The standout: a versioned **agent-rules file** (v1.0) installed into the agent's config that enumerates concrete save triggers: "Solved a non-obvious bug (root cause not apparent from the error)", "Discovered undocumented API/library/tool behavior", "Found a working integration pattern requiring non-obvious configuration", "Hit a framework limitation and found a workaround", "Made an architectural decision with tradeoffs worth preserving." `context-vault setup --upgrade` refreshes rules (overwrites customizations — warned).

**Index/retrieval** — SQLite sidecar index over the markdown (WAL mode, hybrid FTS5 + embedding search). MCP tools `session_start()`, `get_context(query)`, `save_context`; rules instruct the agent to call `session_start()` or `get_context("<project or task context>")` before investing effort.

**Staleness/hygiene** — Recall tracking: the vault records which entries get retrieved and which stay dormant, surfacing dead weight. No documented pruning/archival policy beyond that.

**Does well** — Behavioral spec as data: explicit, testable write-trigger rules plus working/durable tiering, so "what deserves a memory" isn't left to model vibes.
**Weakness** — Canonical repo disappeared (single-maintainer fragility); daemon dependency (Node 22+, auto-updating from npm); hygiene stops at measurement — nothing acts on dormant entries.

## 5. ClawVault (clawvault.dev/markdown-memory)

**Structure** — `memories/` directory of markdown files with category prefixes (`decisions`, `projects`, `lessons`, `preferences`), concise titles, explicit link references. E.g. `clawvault store --category decisions --title "Queue Strategy" --content "Use FIFO queue..."`.

**Write triggers / policy** — Manual, deliberate CLI writes only; every write is a git commit with a descriptive message ("Document queue strategy memory update"). Version control *is* the update policy.

**Index/retrieval** — Markdown plus a semantic retrieval index layered on top: `clawvault vsearch "queue retry policy"` — "Markdown plus retrieval indexes so memory stays transparent without sacrificing recall quality."

**Staleness/hygiene** — None beyond git audit/review; no decay, archival, or pruning guidance.

**Does well** — Cleanest articulation of the transparency thesis: human-readable files as the source of truth, disposable indexes on the side, git history as the audit trail.
**Weakness** — Entirely manual capture (memories are only as complete as user discipline); no concurrency/conflict story for multiple agents; no staleness handling at all.

## 6. Claude Code auto-memory

**Structure**
```
~/.claude/projects/<project>/memory/     # <project> derived from the git repo; shared across worktrees
├── MEMORY.md          # concise index, loaded every session
├── debugging.md       # topic file, loaded on demand
├── api-conventions.md
└── ...
```
Complemented by the human-authored CLAUDE.md hierarchy (managed policy → `~/.claude/CLAUDE.md` → project `./CLAUDE.md` → `CLAUDE.local.md`, concatenated root-down; `.claude/rules/*.md` with optional `paths:` frontmatter for lazy path-scoped loading; `@path` imports).

**Write triggers / policy** — Claude decides mid-session what's durable ("Saved 2 memories"); explicit "remember X" requests route to auto memory; instructions go to CLAUDE.md. Not every session writes. Division of labor is explicit: human writes rules (CLAUDE.md), agent writes learnings (memory/).

**Index/retrieval** — No search index at all. First 200 lines / 25KB of `MEMORY.md` load into every session; topic files are read on demand with ordinary file tools, navigated via the index. Hard mechanical enforcement: after each write the harness measures `MEMORY.md`; near-limit → reminder to compress ("one line per entry, move detail into topic files, merge or drop stale entries"); over-limit → error forcing a rewrite, because overflow is silently dropped on next load. Frontmatter and HTML comments are stripped before counting.

**Staleness/hygiene** — The size ceiling *is* the hygiene mechanism: staying under 200 lines forces continuous merge/drop of stale entries. Plain markdown, fully user-editable via `/memory`; `/doctor` proposes CLAUDE.md trims (cuts what's derivable from the codebase, keeps pitfalls/rationale).

**Does well** — The index-budget pattern: a hard, mechanically enforced cap on the always-loaded surface, with unlimited depth in lazily-read topic files.
**Weakness** — No search: recall depends on the index mentioning the topic file; machine-local (not synced or team-shared); heuristic write policy means silent gaps in what gets captured.

## 7. Letta / MemGPT

**Structure (classic hierarchy)** — Three tiers, per the MemGPT "LLM-as-OS" design:
- **Core memory**: labeled blocks (`persona`, `human`, custom) pinned in-context to the system prompt; each block has label, description, value, and a character `limit`; blocks can be attached/detached and shared between agents.
- **Recall memory**: full conversation history, persisted in a DB, evicted from context but searchable via `conversation_search`.
- **Archival memory**: general long-term store backed by a vector DB, accessed via `archival_memory_insert` / `archival_memory_search`.

**Write triggers / policy** — The agent edits its own memory with tools (`core_memory_append`, `memory_replace`, `memory_insert`, archival inserts) whenever it judges information durable; context-overflow pressure pushes content down-hierarchy. "All state … persisted in a database, so never lost, even once evicted from the context window."

**Index/retrieval** — In-context blocks are always visible; everything else is agentic paged search (vector + text) that the agent invokes itself.

**Staleness/hygiene** — Sleep-time/background agents. In the current git-versioned **MemFS** successor: `$MEMORY_DIR/` with `system/` (loaded every turn), `reference/` (discoverable, lazy-loaded), `skills/`; every change is a git commit; "dreaming" subagents review conversations after N messages or at compaction and consolidate lessons in git *worktrees* so they never block the main agent; a `/doctor` "memory doctor" audits placement, duplication, and token usage; large reorganizations back up the repo before splitting/merging files.

**Does well** — The tiered attention model (always-in-context vs on-demand) plus offline consolidation ("dreaming") — memory quality improves without interrupting work. Notably, Letta's own evolution converged on exactly the git-versioned markdown-folder design.
**Weakness** — Classic block model bound sizes awkwardly (fixed char limits force lossy rewrites); self-editing without approval gates can corrupt persona/facts; historically platform-coupled rather than plain files (fixed only in MemFS).

---

## Comparison table

| System | Storage | Capture | Index/retrieval | Always-loaded surface | Hygiene | Approval gate |
|---|---|---|---|---|---|---|
| ai-memory | Markdown wiki + SQLite, git | Automatic (hooks) + manual | FTS5 + graph RRF + optional vectors | SessionStart handoff injection | Decay sweep, curator, auto-improve scheduler | Optional (`require_approval`), staged proposals |
| memory-vault | Postgres (opaque) | Manual (ingest/`remember`) | pgvector + tsvector, RRF | None (query-only) | Soft-delete; no auto-cleanup | No |
| ai-memory-vault (Obsidian) | Obsidian markdown | Interview + daily notes | Manual job→notes priming, no search | CLAUDE.md + MEMORY.md pointer | None documented | Implicit (human owns vault) |
| context-vault | Markdown + SQLite sidecar | Rules-driven agent saves | Hybrid FTS5 + embeddings, MCP | `session_start()` retrieval | Recall tracking (measure only) | No |
| ClawVault | Markdown, git | Manual CLI | Semantic `vsearch` over markdown | None | Git history only | Via git review |
| Claude Code auto-memory | Markdown folder per repo | Agent-judged, mid-session | None; index + on-demand file reads | MEMORY.md (200 lines / 25KB, enforced) | Size cap forces merge/drop; `/doctor` | User can edit/delete; no pre-write gate |
| Letta/MemGPT | Blocks+vector DB → MemFS (git markdown) | Self-editing tools + dreaming | Block pinning + paged vector/text search; MemFS lazy tree | Core blocks / `system/` dir | Dreaming, memory doctor, reorganize-with-backup | No (worktree isolation instead) |

---

## Takeaways for a git-versioned Markdown folder maintained by coding agents with approval gates

1. **Enforce a hard budget on the always-loaded index.** The single most convergent pattern (Claude Code's 200-line/25KB `MEMORY.md`, Letta's `system/` vs `reference/`, MemGPT's core-block limits): a tiny pinned index with unlimited depth in lazily-read files. Make the cap *mechanical* (a lint/CI check on the index file), not advisory — the size ceiling doubles as the staleness forcing-function, since every addition must displace or merge something.

2. **Ship write-trigger rules as versioned data, not vibes.** context-vault's enumerated triggers ("non-obvious bug root cause", "undocumented behavior", "decision with tradeoffs") are the best-in-class answer to "when should the agent write?" Encode a concrete trigger list in the repo itself, version it, and review changes to it like code.

3. **Type entries by folder, and separate `working/` from `durable/`.** Kind-as-directory (decision/pattern/insight/reference) plus context-vault's working-vs-durable tiering gives you a cheap promotion/expiry model: working entries default to decay, durable entries require deliberate promotion — which maps naturally onto an approval gate.

4. **Use git mechanics as the approval gate.** ClawVault and Letta MemFS show the shape: agent writes land as commits (or staged proposals/branches), humans review diffs; Letta's dreaming subagents work in **git worktrees** so background consolidation never contends with the live session, and big reorganizations snapshot the repo first. Proposal-as-branch + human merge is your approval gate for free.

5. **Do consolidation offline, not inline.** ai-memory's curator/decay sweeps and Letta's dreaming both separate *capture* (cheap, during work) from *consolidation* (batch, background, gated). A periodic "curator" pass that reports duplicates, dangling links, and stale entries — report-only by default, staging one approval-ready proposal — is directly copyable from ai-memory.

6. **Measure recall, then prune what's never read.** context-vault's recall tracking (which entries get retrieved vs stay dormant) is the missing feedback loop in almost every system. Even a crude retrieved-at log per file turns pruning from guesswork into data; feed dormant entries to the curator pass.

7. **Keep any search index as a disposable sidecar.** Every markdown-first system that added search (context-vault, ClawVault, ai-memory) kept SQLite/FTS5/embeddings strictly derived and rebuildable, never committed — markdown stays the source of truth, git stays clean, and index loss is a non-event. Conversely: with a good index file and typed folders, you may not need search at all at small scale (Claude Code proves index + on-demand reads suffices).

8. **Write for handoff, not just recall.** ai-memory's typed session handoffs (summary, open questions, next steps, injected at next session start) are what make memory useful across agents and vendors. A conventional `HANDOFF.md` (or per-project handoff section) that any agent reads first and rewrites last is cheap and makes the folder agent-agnostic — validated by Letta independently converging on git-versioned markdown as its end state.

Sources: [akitaonrails/ai-memory](https://github.com/akitaonrails/ai-memory), [MihaiBuilds/memory-vault](https://github.com/MihaiBuilds/memory-vault), [jaredrhod/ai-memory-vault](https://github.com/jaredrhod/ai-memory-vault), [context-vault.com](https://context-vault.com/) ([agent rules](https://context-vault.com/docs/agent-rules); GitHub repo fellanH/context-vault currently 404), [clawvault.dev/markdown-memory](https://clawvault.dev/markdown-memory), [Claude Code memory docs](https://code.claude.com/docs/en/memory), [Letta MemFS](https://docs.letta.com/concepts/memfs/index.md) and [memory configuration](https://docs.letta.com/configuration/memory/index.md).