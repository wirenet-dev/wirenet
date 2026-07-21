# Container Typologies in Knowledge/Work-Management Systems — Research & Gap Analysis

## 1. How established systems solve "not everything is a project"

### PARA (Tiago Forte)
Four containers ordered by actionability: **Projects** (goal + deadline, completable), **Areas** (ongoing responsibility with a *standard to maintain*, no end date — health, finances, a team you manage), **Resources** (topics of interest, reference material, no responsibility attached), **Archive** (inactive anything). The load-bearing insight is the **Project/Area distinction test**: "Does this end?" If it ends, it's a project; if it must merely stay above a quality bar forever, it's an area. Forte explicitly names conflating the two as the most common failure mode: areas mislabeled as projects become zombie projects that never close and pollute the active list; projects mislabeled as areas never get a finish line and stall. Second insight: **Areas spawn projects** ("Health" spawns "Run half-marathon in October") — the area is the parent context; the project is the bounded excursion. Third: Resources vs Areas is a *responsibility* test, not a topic test — "cooking" is a Resource until you're a chef, then it's an Area.

### GTD (David Allen)
GTD separates by **altitude and commitment**, not folder: *Projects* (any outcome needing >1 action, reviewed weekly), *Areas of Focus* (20,000-ft horizon — roles and responsibilities used as a *lens during review* to generate projects, not a work container), *Someday/Maybe* (captured but explicitly not committed — the pressure-release valve preventing aspirations from contaminating the active list), *Reference* (zero-action material, filed for retrieval only), plus *Calendar* (time-bound) and *Next Actions* lists. GTD's key move: **areas of focus are review prompts, not storage** — you don't "work in" an area; you check it periodically to ask "am I neglecting anything here? What project should exist?" And Someday/Maybe is a first-class citizen: uncommitted ≠ deleted.

### org-mode conventions
Typically one file (or subtree) per long-lived context — `work.org`, `health.org`, `finance.org` — with projects as headings *inside* those files. Everything is an outline node; TODO state (`TODO/NEXT/WAIT/SOMEDAY/DONE`), tags, and properties do the typing, not directory location. Recurring routines are handled natively via **repeating timestamps** (`SCHEDULED: <2026-07-21 Mon ++1w>`) and habit tracking — routines live inside the area file that owns them. `refile` + agenda views mean the container is soft; queries are the real interface. Lesson: **typing via metadata scales better than typing via location, but only if there's a query layer**.

### Johnny.Decimal
`Area (10-19) → Category (11) → ID (11.01)`. Areas are the *top level of everything* — projects don't get their own hierarchy; a project is just IDs within the category it serves. Hard rules: max 10 areas, max 10 categories per area, nothing lives outside the tree, every item has exactly one address. Lesson: **exhaustiveness and uniqueness of address is what kills routing ambiguity** — its whole pitch is "you always know where a thing goes because there is exactly one legal place." Cost: rigid, and bounded projects that span areas are awkward.

### Notion/Obsidian community practice
Dominant Notion pattern: a **Projects database and an Areas database with a relation between them** — every project links to its parent area; tasks link to projects; notes link to either. Routines live as templates/recurring tasks under the area. Obsidian community (PARA-flavored vaults, Zettelkasten hybrids, "ACE", LYT) converges on: folders for *lifecycle* (active/archive), links and tags for *topic*, MOCs (Maps of Content) as soft area-hubs that index notes without containing them. Recurring checklists live as **templates** invoked repeatedly, distinct from the log of instances. Lesson: mature vaults separate **the standing entity (area hub), the bounded effort (project), the reusable procedure (template/checklist), and the append-only log (journal/instances)** — four different lifecycles.

### Agent-memory products
Claude Code auto-memory types memories as roughly **user** (durable preferences/working style), **project** (facts about this codebase/effort), **feedback** (corrections — "don't do X again"), **reference** (stable external facts). This mirrors the CoALA cognitive taxonomy that dominates the field: **semantic** (durable facts about user/entities), **episodic** (what happened in past sessions), **procedural** (how to do things — workflows, checklists), plus working memory. Two lessons transfer directly: (a) **procedural memory is its own type** — "how I do my monthly close" is neither a fact nor a project; (b) the router works because each type has a **crisp admission test** evaluated at write time, and every memory matches exactly one test.

## 2. Gap analysis of the current taxonomy

Current containers: `projects/<slug>/`, `experiments/<slug>/`, `people/`, `notes/`, `sources/`, `docs/`, `archive/`, `TODO.md`, `agent/USER_CONTEXT.md` (plus `outputs/` local-only). This is a **Projects + Resources + Archive** system — it has PARA's P, R, A but **no Area container**, and the strain is already visible in the real portfolio: "Personal Finance" sits in `projects/` despite having no completion state, and "WireNet Base/Shelf" needed a special carve-out ("repositories but not Project Packs") because nothing else fit.

What fails to hold cleanly:

1. **Ongoing responsibilities (finances, health, a team, an org you run).** Forced into `projects/`, they become zombie packs: status fields like "next step" and "done when" are meaningless, they never archive, and the agent can't distinguish "this project is stalled" from "this area is idling normally." This is precisely PARA's named anti-pattern.
2. **Recurring routines/checklists (procedural knowledge).** A monthly invoicing checklist has no home: it's not a project step, not evidence (`sources/`), not a person, and in `notes/` it decays into scratch. No container distinguishes *the procedure* from *the log of runs*. Agent-memory research treats procedural memory as a first-class type for exactly this reason.
3. **Reference collections with a maintenance duty.** `sources/` is defined as *retained evidence* (backing a claim/decision) and `docs/` as cross-project profiles. A curated collection you actively maintain — vendor comparisons, a reading list, tax-rule reference — is neither evidence nor a profile. It leaks into `notes/`.
4. **Learning threads.** "Getting deeper into Rust" has no decision criterion (not `experiments/`), no completion (not `projects/`), and produces durable notes plus a running "where I am" state. Currently it would shatter across `notes/` + `TODO.md` with no owner.
5. **Relationships beyond work.** `people/` is scoped "arbeitsrelevant, evidenzbasiert" — family, the Erbengemeinschaft, personal relationships either get excluded or the scope rule quietly erodes. (The IFA/Erbengemeinschaft matter shows both gaps 1 and 5 at once.)
6. **Someday/Maybe.** No pressure-release valve. Uncommitted ideas either pollute `TODO.md` (which is defined as an *ordered stack* of committed work) or get lost in `notes/`.
7. **Standing life/business dashboards** ("Persönliche Operationen" as a category) exist only as prose in the README — the grouping layer above projects has no addressable home an agent can update.

`notes/` is the tell: any container defined as "durable scratch" becomes the default sink for every unclassifiable type above, and a sink is where agent routing dies — the agent can always *justify* writing there, so retrieval can never *rely* on anything being anywhere else.

## 3. Alternative container models

Design constraint throughout: **an agent must decide the write target from a decidable test on the content, with exactly one legal answer.** Overlapping semantics, not folder count, is what confuses agents.

### Model A — Minimal: reinterpret existing folders (no new top-level dirs)
- `projects/<slug>/` admits two pack types via frontmatter: `type: project` (requires `done_when:`) and `type: area` (requires `standard:` instead; never archives; may list `spawned_projects:`). Alternatively keep only `type: project` and let long-lived slugs carry `lifecycle: ongoing`.
- Routines → `docs/routines/<slug>.md` (procedure = cross-project structured doc; run-logs stay in `outputs/`).
- Reference collections → `docs/reference/`.
- Learning threads → `experiments/` with the decision criterion relaxed to a review date.
- Someday/Maybe → a `## Someday` section at the bottom of `TODO.md`.
- Non-work people → widen `people/` scope, mark `sphere: personal`.

**Pros:** zero migration; folder map stays small; existing links/index intact.
**Cons for agent routing: poor.** The project/area distinction — the single most decision-relevant fact — becomes invisible at the filesystem level and lives in frontmatter the agent must open files to see. `docs/` becomes semantically overloaded (profiles + procedures + reference), recreating the sink problem one level down. Learning threads in `experiments/` violates that container's own admission test ("decision criterion"), teaching the agent that admission tests are soft — the worst possible lesson for a router. Acceptable only as a stopgap.

### Model B — Explicit Areas (recommended): add `areas/<slug>/`, sharpen everything else
- **`areas/<slug>/`** — ongoing responsibility, no completion state. Pack contract: `standard:` (what "healthy" means), current status vs standard, owned routines, related projects, review cadence. Examples: `personal-finance`, `wirenet-org`, `health`, `erbengemeinschaft`. Learning threads are areas with a curriculum (or, if genuinely bounded, projects — the "does it end?" test decides).
- **`areas/<slug>/routines/`** — checklists/procedures owned by the area (procedural memory lives with its owner, org-mode-style). Project-specific runbooks stay in the project pack; truly cross-cutting agent procedures go in `agent/`.
- `people/` — drop the work-only scope; every durable relationship, `sphere:` field for work/personal/family.
- `TODO.md` gains a `## Someday` fence (or `SOMEDAY.md`) so the ordered stack stays committed-only.
- Everything else unchanged; `projects/` admission test tightens to "has a completion state, else it's an area or gets rejected."

Routing table becomes a decision tree with no overlaps:
`Does it end with a defined outcome?` → project. `Is it a bounded question with a decision criterion?` → experiment. `Is it a responsibility with a standard to maintain?` → area. `Is it a repeatable procedure?` → routines/ of its owning area or project. `About a person?` → people. `Evidence for a claim?` → sources. `Cross-project profile?` → docs. `None of the above and durable?` → notes (now genuinely residual).

**Pros:** matches the strongest cross-system consensus (PARA areas, Notion area↔project relation, org area-files, Johnny.Decimal areas-on-top); the write test is a short decidable sequence; kills the three live anomalies (Personal Finance, Base/Shelf carve-out, IFA matter) cleanly; `notes/` shrinks back to a true residual; archives stay meaningful (areas don't archive, projects do). One new folder + one index — migration is moving ~2 packs.
**Cons:** one more top-level container to document; agent needs the project-vs-area test in AGENTS.md (cheap — it's one question); area packs risk bloating into mini-wikis without a size discipline; project↔area cross-links need a convention (`area:` frontmatter key on projects) to avoid double-writing status.

### Model C — Maximal: lifecycle-typed root (full PARA/CoALA hybrid)
Top level reorganized by lifecycle/memory-type: `areas/` (standing responsibilities, each containing its projects, routines, and reference as subfolders — Johnny.Decimal style), `projects/` only for efforts spanning areas or belonging to none, `experiments/`, `library/` (all reference: merges `sources/` + reference collections, typed by frontmatter as evidence vs reference), `journal/` (episodic: dated session/decision logs, append-only), `procedures/` (all checklists/routines, flat), `people/`, `agent/`, `archive/`, `TODO.md` + `SOMEDAY.md`.

**Pros:** theoretically cleanest mapping to memory types (semantic=library/people, episodic=journal, procedural=procedures, task state=TODO); every lifecycle has exactly one home; episodic memory (currently homeless — session history lives nowhere) gets a container.
**Cons for agent routing: worse than it looks.** Nesting projects under areas reintroduces ambiguity ("which area owns this cross-cutting project?" — the exact question flat `projects/` currently never asks); centralizing `procedures/` divorces routines from their owners so the agent must join two containers to answer "how do I run the finance close?"; the migration invalidates every existing link and index in a system that is 3 days into v0.2; and more containers means more admission tests the agent can get wrong. High ceremony, marginal routing gain over Model B.

## Recommendation
**Model B.** The research converges hard: every mature system that survived contact with real life grew an explicit Area/standing-responsibility container, kept it *flat and parallel to* projects (not above them), attached procedures to their owners, and preserved a strict "does it end?" admission test. That test is a single yes/no question — the cheapest possible routing rule for an agent — and it is exactly the question the current taxonomy cannot ask.

Sources: [The PARA Method — Todoist guide](https://www.todoist.com/productivity-methods/para-method), [PARA Method summary and book notes (Thomas Frank)](https://thomasjfrank.com/productivity/books/the-para-method-by-tiago-forte-summary-and-book-notes/), [PARA Method — Workflowy](https://workflowy.com/help/para-method/), [The PARA Method (Shortform summary)](https://www.shortform.com/summary/the-para-method-summary-tiago-forte), [Types of AI Agent Memory (Atlan)](https://atlan.com/know/types-of-ai-agent-memory/), [The 7 Types of Agent Memory (MarkTechPost)](https://www.marktechpost.com/2026/06/21/the-7-types-of-agent-memory-a-technical-guide-for-ai-engineers/), [Agent Memory: Why Your AI Has Amnesia (Oracle)](https://blogs.oracle.com/developers/agent-memory-why-your-ai-has-amnesia-and-how-to-fix-it)