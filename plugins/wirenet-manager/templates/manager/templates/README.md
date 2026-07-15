---
type: "Template Index"
schema: "wirenet-manager/v0.1"
visibility: local
status: active
last_edited: 2026-07-15
---

# Templates

The installed WireNet Manager plugin owns canonical generators and schemas.
This file documents the local Project Pack contract without copying the
plugin's executable logic into the personal Manager. Each packet has four state
documents and one reserved OKF `log.md`.

Use `$wirenet-manager-sync` or the plugin's `create_project_pack.py` helper to
create packets. This prevents local template copies from drifting across users.
