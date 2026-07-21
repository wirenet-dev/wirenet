# DDIA/Petrov → Git-Markdown Knowledge Architecture

## 1. Log/state duality: git history as event log, working tree as materialized state

- **Mapping.** The commit DAG is the append-only log (DDIA ch. 11; Petrov's WAL); the working tree is the materialized state obtained by "replaying" to HEAD. Precisely: git is a *snapshot-per-commit* store, not a delta log — each commit points to a full tree; diffs are derived on read, deltas only appear in packfile compression. So it is an event log of *state transitions*, closer to state-machine replication snapshots than to a redo log of operations.
- **Operational consequences.**
  - State is disposable, log is precious: any checkout is recoverable from history, so back up the remote (the log), not working trees.
  - Recovery = checkout (redo from log); audit and debugging = log replay (`git log -p`, `blame`); this is event sourcing's "the log is the truth."
  - History rewrite on shared branches is log truncation under replication — forbidden; rebase/squash only on private branches. `git gc`/squash-merge is **compaction**: acceptable only where replay fidelity (who decided what, when) isn't needed.
  - Commit granularity is event design: one semantic change per commit, message = event metadata. The Manager's approval-before-write rule is a write-path gate on the log, which is the correct place to gate.

## 2. qmd as materialized view over derived data

- **Mapping.** BM25 + vector index = secondary indexes / materialized view (DDIA ch. 3, 12); Markdown files are the system of record. "Canonical Markdown wins over a stale index" is exactly DDIA's rule that derived data is *redundant and rebuildable*, never authoritative.
- **Rebuildability requirement.** The index must be reconstructible from a clean checkout by one deterministic command, with no information living only in the index. Consequences:
  - Index corruption or ranking bugs are fixed by rebuild, never by hand-editing the index; never write from index back to files (one-way dataflow).
  - The index must record what it was built from — ideally the commit hash — so staleness is *detectable*, not just suspected; `qmd status` should answer "as of which commit?"
  - Changing the embedding model or chunking is a schema migration of the view: full reindex, and results across the migration aren't comparable.
  - Retrieval should end with a read of the canonical file (`get` after `query`) — that is read-repair against staleness: search may be stale, quotes must not be.

## 3. Replication and consistency: what clone + pull actually gives

- **Model.** Multi-leader asynchronous replication: every clone accepts writes; the private remote is a convergence point, not a primary that serves "latest." Approved push windows are deliberately *widened, bounded* replication lag. Git's content-addressed Merkle DAG makes fetch an anti-entropy protocol (Dynamo-style Merkle diffing), and parent hashes encode happens-before — a causality graph, effectively version vectors per branch.
- **Guarantees you actually get.** Locally: read-your-writes, monotonic reads, and a stable snapshot (a checkout is snapshot isolation — internally consistent as of one commit). Across devices: eventual consistency only, and *only upon pull* — no convergence happens without an explicit sync action, unlike gossip systems.
- **What you don't get.** No linearizability, no "freshest wins" reads across devices; two devices can both be "correct" at different commits.
- **Honest staleness = as-of semantics.** Never claim current truth; claim "true as of commit `abc123` (pulled 2026-07-21T09:00)." Agents should stamp answers with the commit they read from, and sync before decisions that depend on another device's recent writes. This turns unavoidable staleness from a lie into a disclosed property — the same move as DDIA's framing of async replicas.

## 4. Conflict resolution: CRDTs vs. mediated merge for prose

- **CRDTs guarantee convergence, not correctness.** A text CRDT merges concurrent edits character-wise into *some* deterministic result — fine for live co-editing, wrong for asynchronous knowledge curation, because the unit of conflict is a **claim**, not a character. Two devices editing "deadline: Friday" → "Thursday" vs. "moved to next week" will converge under a CRDT to interleaved text nobody wrote and nobody reviewed. DDIA's warning applies: automatic last-write-wins or merge functions silently discard intent; silent convergence on semantic conflicts is data loss wearing a success face.
- **What git 3-way merge + agent gives us.** The merge base identifies true concurrency (vs. fast-forward); non-overlapping hunks auto-merge safely because file structure approximates claim independence; overlapping edits *halt and surface* — refusing to guess is the feature. Layering an agent on top gives a semantic merge function with a human override: the agent proposes a resolution with reasoning, the owner accepts or edits. That is conflict resolution promoted from a storage-layer heuristic to a reviewed write.
- **Certification-as-merge.** Branch + PR + human-owner merge is a commit protocol with a human coordinator: writes to team-canonical state are proposals until certified. This matches DDIA's point that keeping conflicting versions and resolving them explicitly (Dynamo's siblings) beats silent resolution — the PR *is* the sibling presentation UI. The doctor belongs here as a pre-merge invariant check, since Markdown has no schema enforcement in the storage engine.

## 5. Design rules

1. **Files are the sole system of record**: every index, cache, or view must be rebuildable from a clean checkout by one command and must record the commit hash it was built from.
2. **Every retrieved answer carries as-of provenance** (source commit + index freshness), and detected staleness is disclosed, never papered over.
3. **Shared-branch history is append-only**; rewrites, squashes, and compaction are permitted only on private branches or with explicit owner sign-off.
4. **Convergence is not correctness**: overlapping semantic edits must never auto-merge; they surface as conflicts with an agent-proposed, human-certified resolution.
5. **The doctor is a constraint checker at the merge gate**: conventions are enforced pre-merge so that certification (merge by owner) implies validity, not merely acceptance.