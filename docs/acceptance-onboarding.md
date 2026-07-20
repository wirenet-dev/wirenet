---
last_edited: 2026-07-20
---

# Onboarding Acceptance Matrix

Acceptance contract for the clean-user onboarding test: a separate fresh macOS
user on the developer's machine, no existing personal Manager context, plugin
installed from the `stable` ref. Every row must end in pass, explicitly
deferred, or documented friction; silent partial success is a failure.

| # | Stage | Acceptance criterion | Evidence |
| --- | --- | --- | --- |
| 1 | Install | Marketplace add + plugin install succeed from `stable` without a developer setup | command transcript |
| 2 | Preflight | Runtime preflight resolves Python and Git from the bundled runtime or PATH, stops cleanly otherwise | preflight output |
| 3 | Bootstrap | Dry-run preview shown before any write; `--apply` creates `~/Manager` matching the seed; no product repo clone | preview + diff |
| 4 | Doctor | `ok: true` immediately after bootstrap | doctor JSON |
| 5 | QMD (optional) | Offered, not forced; failure leaves the Manager fully usable | conversation log |
| 6 | First meeting | Exact hello, first map before any connected-source read, one question at a time | conversation log |
| 7 | Approval gates | Install, connect, read, and write approvals are asked separately; no gate skipped or bundled | conversation log |
| 8 | Packs | At least one Project Pack created via preview → approval; index and bindings consistent afterwards | doctor + files |
| 9 | Automation | Offers one current-task hourly check-in; for Git-tracked Managers, separately offers semantic commits and safe 09:00/16:00 push windows in the same heartbeat, with no second push task by default | conversation log + automation card |
| 10 | Handoff | Recap follows the reference structure and ends with "You can just talk to your Manager now" | conversation log |
| 11 | Continuity | A second, fresh task answers "What is on my plate?" correctly from the Manager alone (cold-start test) | second-task transcript |
| 12 | Upgrade | A later stable release is detected with concise notes; Marketplace refresh requires approval; any workspace migration requires a clean checkpoint and finishes with installed version, migration result, and Doctor-valid success report | update check + updater output |

Friction observations to capture explicitly: number of approval prompts before
first visible value (target: one bundled preview), whether a short-path exit
after stage 9 felt available, and every moment the user had to understand an
internal term (schema, OKF, binding) to proceed.
