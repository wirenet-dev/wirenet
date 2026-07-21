# wirenet

**Your assistant remembers your work — across tools, sessions, and projects,
on your machine.**

wirenet gives every person a **Manager**: a local folder of plain Markdown
that any agent reads before it acts and keeps current after you approve it —
a place for what you are working on, what you have decided, who you work
with, and what comes next. Plain files, versioned with git, owned by you.
It works with Claude Code and the ChatGPT app (Codex), and — because it is
just files — with any agent that can read a folder.

## Fast Start — Claude Code

```text
/plugin marketplace add wirenet-dev/wirenet
/plugin install wirenet@wirenet
```

Start a new session and say: **"Set up my Manager."**

## Fast Start — ChatGPT app (Codex)

Open **Plugins**, find **wirenet**, and install it. Or from the CLI:

```sh
codex plugin marketplace add wirenet-dev/wirenet --ref stable
codex plugin add wirenet@wirenet
```

Restart the app, start a new session, and say: **"Set up my Manager."**

An agent reading this page can walk the whole path: add the marketplace,
install the plugin, ask the user to start a fresh session, and begin the
first meeting. No git knowledge, no terminal skills, and no cloning are
required of the user.

## What You Get

- **A Manager** (`~/Manager`) built in a guided first meeting: your current
  stack, your projects and ongoing responsibilities, the people you work
  with, and your working style — maintained by your agents, with every
  durable write previewed and approved.
- **Two skills**: `manager` (the daily companion: what is on my plate,
  handoffs, follow-ups, health) and `manager-setup` (first meeting, adopting
  an existing folder, repair).
- **A doctor** that checks conventions — never your content — and proposes
  fixes instead of performing them.
- **No lock-in, by design**: the Manager works with no wirenet software
  installed. The plugin delivers, extends reach, and maintains; your folder
  never depends on it. Copy the folder and you have everything.

## How It Works

The product essence lives in [docs/product.md](docs/product.md), the
governing behavior contract in
[docs/core-contract.md](docs/core-contract.md), and every architectural
decision in [docs/decisions/](docs/decisions/). The theoretical grounding is
named in [docs/foundations.md](docs/foundations.md).

## For Developers And Operators

This repository is the product monorepo: the plugin under
[plugins/wirenet/](plugins/wirenet/) (skills, references, seed templates,
scripts), machine-enforced schemas under [contracts/](contracts/), and tests
under [tests/](tests/). `bin/wirenet` is an operator tool for people who
work with this repository — installing and using the Manager never requires
it. Development conventions: [AGENTS.md](AGENTS.md).

## Lineage And License

wirenet began as a deliberate downstream of Jason Liu's
[personal-monorepo-template](https://github.com/jxnl/personal-monorepo-template)
and keeps its best ideas — the vault that carries its own operating
instructions, durable meaning over activity, approval before shared-memory
writes. Apache-2.0.
