# ADR 005: Workspace Bindings Are an Optional, Private Routing Table

Date: 2026-07-21 · Status: accepted

## Context

Bindings looked like a hard 1:1 claim "this project's knowledge lives in this
folder". Real projects keep knowledge in many places (several folders, mail,
cloud documents), some packs need no folder at all, and shared repositories
must not carry personal pointers.

## Decision

`.wirenet/workspace-bindings.json` is a private, machine-local routing table:
slug → **zero or more** local paths, plus an ignore list. It answers exactly
one question — "an agent works in folder X; which pack does this belong to?" —
and makes no statement about where knowledge lives. Knowledge locations of
every kind stay prose sources inside the pack. Bindings also keep absolute
paths out of portable documents and let shared repos stay clean of personal
pointers.

## Consequences

Multiple folders per project are a feature, not an exception; knowledge-first
packs stay unbound. The v1 format and its schema (`contracts/manager/`) are
fixed at the seed/migration station; `bin/wirenet check_bindings` and the
doctor follow the new format.
