# Instance Templates

Seeds for materializing WireNet element instances. They are product assets:
`wirenet init <element>` (or the corresponding skill) copies them into a new
instance; no standalone template repository is a source of truth.

- `base/` — OKF knowledge bundle seed for a shared Base (formerly the
  `wirenet-base` repository).
- `shelf/` — skill shelf seed (formerly the `wirenet-skills` repository).

The Manager seed remains at `plugins/manager/templates/manager/`, owned by the
Manager plugin bootstrap.
