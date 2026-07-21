---
last_edited: 2026-07-21
---

# Instance Templates

Seeds for materializing WireNet element instances. They are product assets:
`wirenet init <element>` (or the corresponding skill) copies them into a new
instance; no standalone template repository is a source of truth.

- `base/` — OKF knowledge bundle seed for a shared Base (formerly the
  `wirenet-base` repository).
- `shelf/` — skill shelf seed (formerly the `wirenet-skills` repository).

The Manager seed remains at `plugins/manager/templates/manager/`, owned by the
Manager plugin bootstrap.

On `--apply`, `wirenet init base|shelf` copies the selected seed and adds a
runtime `.wirenet/instance.json` containing the installation ID, owner, element,
and product template origin. The manifest contains no credentials or instance
knowledge. Starter concepts that later need seeded upgrades should carry their
own explicit origin/version metadata; reserved `index.md` and `log.md` files do
not receive concept frontmatter.
