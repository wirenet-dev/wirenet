---
name: wirenet-manager-person
description: Create, find, update, correct, link, or review evidence-backed person concepts in WireNet Manager. Use when the user asks to remember a collaborator, client, teammate, owner, decision maker, communication preference, responsibility, relationship context, or durable human handoff. Do not use for one-off contacts, raw address books, or private communication archives.
---

# WireNet Manager Person

Maintain the smallest durable person context that will help a future task work
with someone correctly.

## Workflow

1. Resolve Manager from `WIRENET_MANAGER_DIR`, then `~/Manager`. Use
   `$wirenet-manager-bootstrap` if it is missing or unhealthy.
2. Read the Manager content language and
   `../wirenet-manager/references/content-routing.md`.
3. Search for an existing canonical `people/*.md` concept by name, alias, and
   relevant project link before proposing a new file. Use the `manager` QMD
   collection only as candidate routing, then read the complete concept.
4. Keep only work-relevant durable context: role, relationship, responsibilities,
   confirmed preferences, decisions, current handoffs, useful project links,
   and source boundaries.
5. For a new person, preview plugin-root `scripts/create_person_note.py` with a
   grounded one-sentence context. Ask before applying it.
6. For an existing person, propose the smallest semantic diff. Preserve unknown
   metadata and established prose. Add a section only when real information
   earns it.
7. Use normal Markdown links to connect the person concept to relevant Project
   Packs. Create `people/index.md` only after real volume makes a catalog useful.

## Evidence And Privacy

Distinguish confirmed facts, user corrections, and uncertain inference. Ask
before reading Gmail, Slack, calendar, Drive, or another connected source for
person context. Do not store raw messages, private attachments, personal trivia,
credentials, account details, or sensitive facts irrelevant to the work.

Do not create a person concept merely because a name appeared once. Preview
inferred durable writes and obtain approval unless the user already approved
that exact note or update.
