---
last_edited: 2026-07-16
---

# Runtime Preflight

Resolve local executables before previewing or applying technical Manager work.
The user should not need to install or understand development tooling.

## Resolution Order

1. When the Codex app exposes bundled workspace dependencies, load them and
   prefer its Python, Git, and package-manager paths.
2. Otherwise use executable paths already available on `PATH`.
3. Never install system Python, Git, Xcode command-line tools, Node.js, or a
   package manager implicitly.
4. If Python or Git cannot be resolved, stop before writing Manager files and
   explain that the local Codex runtime is incomplete.

Invoke every Python helper with the resolved Python executable. Pass the Git
executable to bootstrap and upgrades with `--git-bin`. When the resolved Git
directory is a Codex fallback directory, prepend it to `PATH` for related local
Git operations in the same task.

For QMD, prefer an existing healthy `qmd`. When installation is approved, pass
an available package manager explicitly with `--npm-bin` or `--pnpm-bin`.
Because QMD officially targets npm, the bundled `pnpm` fallback bootstraps a
pinned npm and then installs QMD with its required native build scripts into a
dedicated user-local wirenet directory. It does not change shell startup files.
QMD remains optional; failure must not invalidate an otherwise healthy Manager.

Report only the human result: runtime ready, Manager created or repaired, and
any optional retrieval limitation. Do not turn executable discovery into a
developer-facing setup lesson unless manual intervention is genuinely required.
