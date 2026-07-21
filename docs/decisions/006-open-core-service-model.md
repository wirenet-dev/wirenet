# ADR 006: Open Core, Service-Led

Date: 2026-07-21 · Status: accepted

## Context

The vault is plain files and the repository is Apache-2.0, so nothing stops a
customer from leaving — or a large vendor from shipping something similar.
Portability cuts both ways.

## Decision

Embrace it. The product is open core and the business is service-led: WireNet
sells onboarding, operation, judgment, and the neutral memory layer across
vendors that no vendor will build for its competitors. Lock-in is explicitly
not the strategy; two-way portability is a feature we advertise.

## Consequences

If a major vendor ships native folder-memory, the foundation laid here carries
over instead of competing head-on. Revenue depends on service quality and the
organizational layer (base/shelf, managed installations), not on the file
format. Pricing and offer details stay in the Manager's business pack, not in
this repository.
