# Knowledge graphs vs. a Markdown entity graph — research notes

## 1. What RDF/OWL/SKOS/property graphs offer that this design misses

- **Global identifiers & merge semantics (RDF).** IRIs make two files about the same entity provably the same node; grep-land has no `owl:sameAs`, so duplicate entities silently fork. Mitigable with discipline, not tooling.
- **Schema validation (RDFS/SHACL).** Nothing stops `depends-on:` pointing at a deleted file, a typo'd verb (`depend-on:`), or a link into the wrong directory/kind. SHACL-style checks are what you'd hand-roll as a lint script.
- **Inference (OWL).** Transitive closure (`depends-on` chains), inverse properties (auto-derive "depended-on-by"), class subsumption. Grep gives you 1-hop; multi-hop needs a loop and gets O(n^hops) and error-prone past 2 hops.
- **Real queries (SPARQL/Cypher).** "Entities owned by X, status stale, transitively depended on by anything shipping this quarter" is one Cypher query; in grep it's a script with joins you maintain by hand.
- **Reified/qualified edges (property graphs).** Your links can't carry attributes: since-when, confidence, who-asserted. `depends-on: foo (since 2026-03)` is parseable prose, not data.
- **Federation.** SPARQL can join your graph with external vocabularies/datasets. Almost never needed for org memory.

## 2. Where formal tooling earns its keep — thresholds & real-world evidence

Rough thresholds (each independently sufficient):
- **~1–2k entities or ~5k+ links**: dedup and dangling-link rot outpace human review; you need at least a lint pass, if not a store.
- **Query complexity**: the day someone needs regular 3+-hop traversal or joins across entity kinds *interactively*, grep loses. One-off multi-hop is fine as a script.
- **Multiple writers with divergent vocabularies**: ontology work is fundamentally about agreement between people; solo/small-team files don't need it.
- **External consumers**: the moment another system must read your graph, formats (JSON-LD, RDF) beat conventions.

Evidence for the lightweight side:
- **schema.org** deliberately refused to be a "global ontology": multiple domains/ranges "purely pragmatic," optimized for publisher simplicity over computational cleanliness — and won where richer predecessors (full RDF/microformats wars) failed ([schema.org data model](https://schema.org/docs/datamodel.html), [Iliadis 2025](https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24744)).
- **SKOS beat OWL** for real vocabularies precisely by dropping formal semantics — "Semantic Web light" — becoming the interop standard for thesauri while OWL stayed niche ([SKOS with OWL: Don't be Full-ish](https://www.researchgate.net/publication/221218473_SKOS_with_OWL_Don't_be_Full-ish), [You probably don't need OWL](https://www.bobdc.com/blog/dontneedowl/)). Your GLOSSARY.md is basically SKOS `prefLabel`+`definition`, which is the part that survived contact with practice.
- **Shirky, "Ontology Is Overrated" (2005)**: pre-coordinated categories fail when the corpus and its readers change; links + search degrade gracefully where taxonomies shatter. Your design is on the right side of this.
- **Wikipedia's category system** is the cautionary middle: an informal folksonomy that grew graph-like semantics nobody enforces — cycles, inconsistent hierarchies — showing that *implicit* ontology without validation rots. Verbs need a registry even if nothing enforces it.
- **Roam/Obsidian at scale**: vaults run fine to ~10k notes; what breaks first is not storage or search but *link discipline* — orphan pages, synonym drift ("acme-corp" vs "Acme"). The community's fix (Dataview/juggl plugins = a query layer over frontmatter) is exactly the BM25+index move you already made. Lesson: the query layer, not the ontology, is what people actually retrofit.

Net: formal tooling earns its keep at **team-scale writing + interactive multi-hop querying + external consumption**, not at any particular entity count. Below that, a 50-line lint script buys 80% of SHACL.

## 3. Cheap conventions that future-proof for graph export (adopt now)

1. **Stable, immutable, globally unique ids** — `id:` in frontmatter, never reused, never renamed even if the file moves; links target ids (or filenames that equal ids). This is the one thing you cannot retrofit. It maps 1:1 to IRIs later (`org:person/jdoe` → a URI namespace).
2. **Closed verb registry with inverses** — one `VERBS.md`: each verb, one line, its inverse (`depends-on` / `depended-on-by`), and whether transitive. Don't *enforce* inverses in files; just declare them. This is your future edge-type schema, and it makes `supersedes` chains machine-walkable on export day.
3. **One machine-parseable link line format** — commit to exactly `- verb: target-id — optional free-text note` and nothing else in `## Links`. A 20-line parser then emits valid JSON-LD/Cypher whenever you want. (Optional 4th, nearly free: GLOSSARY terms get ids too, so definitions become `skos:Concept`s.)

## 4. Deliberately keep informal

- **No class hierarchy.** Directory = kind, flat. Subtyping is where OWL projects go to die; add a `kind:` refinement key only when a real query needs it.
- **No cardinality/domain/range rules.** Let any verb connect any kinds; lint for *dangling* targets only, not "invalid" ones.
- **Prose bodies.** The paragraph under the frontmatter is the payload; never try to structure it. Search (BM25+vectors) is your reasoner over prose — that's the modern answer to most of what OWL inference promised.
- **Confidence, provenance, temporal validity** — keep as free-text in the link note, not fields. Reify only if a consumer ever needs it.
- **The glossary's rigor.** One plain-English line per term; resist `broader`/`narrower` scaffolding until two terms actually collide.

Sources: [schema.org data model](https://schema.org/docs/datamodel.html) · [Iliadis, "One schema to rule them all" (JASIST 2025)](https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24744) · [SKOS with OWL: Don't be Full-ish](https://www.researchgate.net/publication/221218473_SKOS_with_OWL_Don't_be_Full-ish) · [You probably don't need OWL (bobdc)](https://www.bobdc.com/blog/dontneedowl/) · [W3C: Using OWL and SKOS](https://www.w3.org/2006/07/SWD/SKOS/skos-and-owl/master.html) · Shirky, "Ontology Is Overrated" (2005)