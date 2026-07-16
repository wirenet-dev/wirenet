---
name: yeet
description: Publish the current repository changes by reviewing scope, staging intentionally, creating a clear commit, pushing the current branch, and opening a pull request. Use only when the user explicitly asks for the complete commit-push-PR flow or explicitly invokes $yeet. Do not trigger from a request that mentions only one part of that sequence.
---

# Yeet

Run the complete publication flow only after explicit activation.

1. Confirm repository, branch, remote, authentication, and the intended change
   scope. Do not publish unrelated user work.
2. Inspect tracked, staged, and untracked changes completely. Stop for secrets,
   generated debris, conflicts, ambiguous work, or a branch that should not be
   published.
3. Run relevant validation and report failures before deciding whether the
   change is ready.
4. Stage files by coherent intent and create a concise semantic commit. Never
   use a blanket stage command without reviewing every included file.
5. Push the current non-protected branch without force.
6. Open a pull request with a grounded summary and test evidence. Prefer draft
   status when review or validation remains incomplete.

Never amend, rebase, force-push, merge, or change a protected branch unless the
user separately asks for that exact action.
