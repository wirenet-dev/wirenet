# ADR 001: One Marketplace, One Core Plugin Named "wirenet"

Date: 2026-07-21 · Status: accepted

## Context

v0.4.6 shipped three plugins (`manager`, `workflows`, `content-tools`) and the
core plugin's skills invoked as `manager:manager` and `manager:manager-setup`
in Claude Code. Customers should be able to say "install wirenet" and be done.

## Decision

The marketplace stays `wirenet`; the core plugin is renamed `manager` →
`wirenet`. Skills keep their names `manager` and `manager-setup`, because
Codex resolves skills in a flat `$`-namespace where generic names like
`setup` would collide. Claude Code invocations become `wirenet:manager` and
`wirenet:manager-setup`. `workflows` and `content-tools` leave the v0.5
marketplace and may return later as extensions.

## Consequences

Existing installations must reinstall once (cheapest before the first
external demo). The brand plugin is the core plugin; extensions install as
`<name>@wirenet` beside it.
