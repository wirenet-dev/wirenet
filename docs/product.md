---
last_edited: 2026-07-21
---

# wirenet: What It Is And Why

## The Problem

People who work with AI assistants have their working memory everywhere and
nowhere. Every tool keeps its own memory, so Claude knows nothing of Codex and
both forget between sessions. Context accumulates inside vendor products and
belongs to the vendor, not the person. Technical users solve this by building
themselves vault systems in git; everyone else never will.

## The Thesis

Coding agents are becoming a new operating layer between people and machines —
the interface through which work happens. When the interface shifts, the
substrate shifts with it: the durable ground of work is no longer only code
but versioned, checked prose. Instructions, knowledge, and conventions live in
git, are linted, tested, and released like software — markdown as code. Code
itself remains part of the picture, increasingly written by agents under
expert direction.

In that picture, wirenet is not a note folder with skills. It is the **home
directory of the agentic operating system**: the one place every agent
respects, where a person's work, relationships, priorities, and preferences
persist regardless of which interface is in front of them. The runtimes
(Claude Code, Codex, whatever follows) are the kernel — deliberately not ours.
wirenet is userland.

Checked like code does not mean typed like code: the personal vault stays
prose governed by conventions, and machine-readable typing appears only where
machines truly need it (see `decisions/004`).

## The Bet

1. **Files are the universal interface.** A folder of plain Markdown can be
   read by every tool that exists and every tool that will exist.
2. **Agents are now good enough to maintain the memory themselves.** The user
   only talks; the agent routes, writes, and keeps things current.
3. **Approval-gated writes make agent-maintained memory trustworthy.** The
   user stays the owner of every durable change.

## The Product

*Your assistant remembers your work — across tools, sessions, and projects,
on your machine.*

A folder (`~/Manager`), one daily skill, optional local retrieval, and an
interview-style onboarding, delivered as one installable plugin for Claude
Code and Codex. The full behavior is defined in
[`core-contract.md`](core-contract.md).

## Who It Is For

Individuals first: knowledge workers who use AI assistants daily and want
their context to be durable and their own — today including a first client
team of six people, each using it individually. Small knowledge-intensive
teams next, once shared context earns its own layer.

## Growth Path

1. **Multi-device for one person** — a private git remote with safe push
   windows; the smallest sync problem, solved first.
2. **Team collaboration** — a shared knowledge base and skill shelf per
   organization. Working principle, still up for debate: conventions stay
   personal, typing returns at the shared layer — a team catalog earns the
   machine-readable structure (OKF) that a personal vault does not.

## Business Model

Open core, service-led. The product repository is Apache-2.0 and the vault is
plain files, so portability is deliberately two-way: customers can leave as
easily as they arrive. What WireNet sells is everything a file format cannot
ship — onboarding, operation, judgment, and the neutral layer across vendors
that no vendor will build.

## Non-Goals

- No cloud service and no app of our own; local files and existing runtimes.
- No schemas or required metadata in the personal core.
- No activity log; durable meaning only.
- No automation, sync, or external side effect without explicit approval.
- Windows is not a supported platform yet. The core is built portable (plain
  files, Python, git); support becomes a promise only when a real Windows
  customer makes it one.
