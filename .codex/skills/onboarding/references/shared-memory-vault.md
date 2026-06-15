---
last_edited: 2026-06-15
---

# Shared Memory Vault

The vault is optional plain-file memory for durable work context outside one chat.

Default path: `~/vault`, unless the user names another folder or an existing vault should be reused.

Default shape:

```text
vault/
|-- AGENTS.md
|-- TODO.md
|-- agent/
|   `-- USER_CONTEXT.md
|-- people/
|-- projects/
|-- notes/
`-- sources/
```

Use it for:

- the user's working profile
- durable projects and workstreams
- important people
- open loops and decisions
- source routes future Assistant chats should know

Do not use it for raw email/chat dumps, one-off names, weak guesses, or activity logs.

## Setup

After the interview is calibrated:

1. Explain the vault in one short paragraph.
2. Ask before creating or extending it.
3. If approved, run `../scripts/setup_shared_memory_vault.py`.
4. Personalize `AGENTS.md` and `agent/USER_CONTEXT.md`.
5. Mention the path in the final recap.

If a vault already exists, inspect it first and preserve its structure.

## User-Facing Explanation

```md
**Shared Memory**

This chat is where we talk. The check-in is what brings me back. The vault is the plain-file memory I maintain so durable work context does not live only inside one chat.

**Question**

Want me to set that up?
```
