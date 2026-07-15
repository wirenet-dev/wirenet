---
last_edited: 2026-07-15
---

# Guided First Run

Use this flow only for a brand-new or materially incomplete Manager setup. Make
it feel like a capable work companion learning the user's world, not a setup
wizard. Read available context before asking, ask one useful question at a time,
and explain each approval gate in plain language.

## Setup State

Classify quietly:

- `brand_new`: no healthy Manager, calibrated work map, source setup, or Manager
  task exists. Run the full flow.
- `partial`: a Manager exists but one or more first-run outcomes are missing.
  Fill only those gaps.
- `established`: the Manager, work map, and daily-use path are already useful.
  Skip onboarding and handle the requested health check, repair, or upgrade.

The installed bootstrap skill cannot run before its plugin exists. If a clean
task only has the public repository or an Appshot, follow the root README's
installer contract first. Install the marketplace and plugin after approval,
restart ChatGPT if requested, and continue the guided first run in a fresh task.
Never clone the product repository into the personal Manager.

## 1. Establish The Local Baseline

Explain the plugin, runtime, and knowledge boundary in one short paragraph.
Run the bootstrap, Doctor, QMD, discovery, and global-guidance operations in the
order defined by the parent skill. Preview every system change before applying
it. Do not mix the deterministic setup operations with inferred memory writes.

## 2. Build The First Work Map

After the Manager is healthy, ask:

```text
What's on your plate right now? Rambling is welcome; I will organize it with you.
```

Use the answer to learn only what matters for the first useful map:

- active, waiting, paused, and safely ignored work;
- the next few priorities and likely dropped balls;
- important people and handoffs;
- where project files currently live;
- which communication and work sources would materially improve awareness.

Return a compact map and ask what is wrong or missing. Then propose the specific
`TODO.md`, Project Pack, Experiment Pack, people, or user-context changes that
would preserve the calibrated map. Ask before writing inferred durable content.
Do not create empty packets, people notes, or shelf documents merely to complete
onboarding.

## 3. Communication And Work Sources

Inspect which relevant plugins or connectors are already installed, enabled,
and connected. Recommend capabilities from the user's actual map rather than a
generic catalog. Useful categories include:

- email or messages for client asks and unresolved replies;
- calendar for commitments, conflicts, deadlines, and preparation gaps;
- files and documents for canonical briefs and decisions;
- repositories or project trackers for delivery state and blockers.

Keep three separate approval gates:

1. install or enable a plugin;
2. connect an account or service;
3. read approved sources to propose durable Manager context.

Default to read-only orientation. Never send or reply to messages, change
meetings, edit shared documents, create cloud resources, or write inferred
memory without explicit approval for that specific action. The Manager remains
useful with local files alone when the user skips communication setup.

## 4. Explain Daily Use

Give the user four concrete examples, adapted to the setup:

- `What is on my plate?` reads the current stack and relevant packets.
- `Track this workspace` classifies an external folder and creates or updates a
  Project or Experiment Pack after approval.
- `Open my Manager` opens the read-only WireNet Inspector.
- `Update the Manager with this handoff` proposes one durable reconciliation.

Explain that this task can become the Manager home for portfolio work and
connected-source awareness. Work may still happen in any external folder; the
approved global managed block recalls `$wirenet-manager-sync` only when a
meaningful durable handoff would otherwise be lost.

## 5. Offer The First Manager Check-In

After the work map and approved source scope are clear, offer one core recurring
check-in in the current task. Recommend an hourly quiet heartbeat unless the
user prefers a daily cadence or no automation. Ask explicit approval before
creating it.

Use the scheduled-task or automation tool with the current task as destination.
Do not emit raw automation syntax or create a detached thread. Use a prompt with
this contract, adapted to the approved setup:

```text
Use $wirenet-manager. Read ~/Manager/TODO.md and only the relevant active Project or Experiment Packs. Check only the connected sources I approved for meaningful new asks, commitments, deadlines, blockers, decisions, preparation gaps, or dropped follow-ups. Preserve my stated task order. Notify me only when there is a useful delta or next action; otherwise stay quiet. Never send messages, change meetings, edit shared documents, create cloud resources, or write inferred durable memory without my explicit approval for that action.
```

If local Manager files are part of the check, explain that the computer and
ChatGPT desktop app must be running. Offer to rename or pin the current task as
the Manager home, but treat each task change as an explicit approval. Do not
create separate project or people monitors during the core first run unless the
user asks for them.

## 6. Close The First Run

End with a concise recap:

- Manager path and Doctor result;
- QMD availability and collection name, when configured;
- Project and Experiment Packs created or deliberately skipped;
- communication sources connected or deferred;
- global managed blocks installed or declined;
- current Manager task and check-in state;
- the smallest useful next action.

The first run is complete only when every relevant item above is handled,
declined, or explicitly deferred. End with: `You can just talk to your Manager
now.`
