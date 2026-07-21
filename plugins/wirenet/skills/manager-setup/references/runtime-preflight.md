# Runtime Preflight

Quiet checks before materializing — surface only what blocks setup.

- **Runtime**: identify Claude Code or Codex; skills, automation surface,
  and global-instruction targets differ per runtime.
- **Connectors**: install the plugins where the user's work happens before
  deeper onboarding, so the first map can read the right context. Newly
  installed plugins need a fresh session — say so when it matters, not as a
  disclaimer up front.
- **Tools**: confirm `git` and `python3` are runnable. If git is missing on
  macOS, the Xcode Command Line Tools prompt will appear — warn the user
  before triggering it.
- **Location**: resolve `WIRENET_MANAGER_DIR`, then `~/Manager`. Never
  create a nested Manager inside an existing one; if the target has prior
  content, adopt in place (create only missing files).
- **qmd**: optional. If absent, skip retrieval registration quietly; the
  Manager works without it.
