---
name: audit-ai-code
description: Audit AI-generated or AI-shaped backend and general implementation code for duplicated helpers, hard-coded fixtures, speculative abstraction, broad exception handling, configuration sprawl, hallucinated dependencies, local-convention drift, brittle tests, unsafe behavior, and unnecessary complexity. Use after an agent implementation or when the user asks to de-slop, simplify, modularize, parameterize, or review maintainability. Diagnose first; edit only when the user asks for changes.
---

# AI Code Audit

Inspect the repository's own conventions and the complete relevant diff before
judging the implementation. Separate real defects from unfamiliar but valid
local patterns.

## Review

Check in this order:

1. correctness, safety, data loss, permissions, secrets, and error behavior;
2. invented APIs, dependencies, configuration, or assumptions;
3. test-only constants, hard-coded fixtures, duplicated helpers, and branches
   added merely to satisfy one example;
4. broad wrappers, fallback chains, mode flags, configuration bags, and
   abstractions that obscure the actual operation;
5. mismatch with existing modules, naming, types, logging, and test style;
6. performance or maintenance costs large enough to matter.

## Findings

Lead with concrete findings ordered by severity. Give the file and narrow line
range, explain the failure mode, and recommend the smallest durable fix. Group
repeated symptoms under one cause. Do not create findings merely to fill a
report.

If no material problem remains, say so and name any validation gap. When asked
to fix the code, preserve behavior, remove the smallest amount of accidental
complexity, and run proportionate tests.
