# ADR 003: contracts/ Holds Only Schemas That Code Enforces

Date: 2026-07-21 · Status: accepted

## Context

v0.2 kept large hand-written JSON "behavior contracts" describing the product
in parallel to prose docs and tests — three surfaces that could drift apart.

## Decision

The product has three contract layers: (1) prose contracts in `docs/`
(constitution, for humans and agents), (2) convention checks in the doctor
(executable rules over the Markdown world), (3) JSON Schemas in `contracts/`
**only** for machine-state JSON files that code validates: installation
config, instance manifests, and (pending) workspace bindings. Descriptive
behavior contracts are prose, not JSON.

## Consequences

`contracts/routing/` is deleted. The installation schemas are currently
enforced only indirectly (hand-written checks mirror them); a test that
validates examples against the schemas closes that gap at the tests station.
The bindings schema is added once the v1 format is fixed.
