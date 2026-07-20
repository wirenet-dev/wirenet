---
last_edited: 2026-07-20
---

# First-Bootstrap Demo Runbook

Runbook for a live first bootstrap with a new user (dry run on your own
machine first, then the real person on their machine). The acceptance
contract behind it is `docs/acceptance-onboarding.md`; this page is the
minimal choreography.

## Preconditions

- Release published: `stable` points at the intended tag; CI green.
- The guest uses their own machine and their own ChatGPT/Codex account
  (or Claude Code); nothing is pre-installed.
- Host keeps `docs/acceptance-onboarding.md` open as observer checklist and
  captures friction silently instead of steering.

## The Two Commands

Codex / ChatGPT Work:

```sh
codex plugin marketplace add wirenet-dev/wirenet --ref stable
codex plugin add manager@wirenet
```

Claude Code:

```text
/plugin marketplace add wirenet-dev/wirenet
/plugin install manager@wirenet
```

Then, in a fresh task:

```text
$manager-setup Richte meinen lokalen Manager ein und starte danach das Onboarding.
```

## Expected Path

1. Runtime preflight resolves Python and Git without a developer setup.
2. Bootstrap shows one dry-run preview, applies only after approval, and ends
   with Doctor `ok: true`.
3. QMD is offered, never forced.
4. First meeting opens with the exact hello in the guest's language and builds
   a map before asking to read any connected source.
5. Every install/connect/read/write approval is asked separately.
6. Non-English guests are offered a one-time translation of the seeded
   `README.md`/`TODO.md` bodies.
7. Automation setup recommends one current-task hourly check-in and separately
   offers semantic local commits plus safe 09:00/16:00 push windows in that same
   task; it does not create a second push automation unless the guest prefers
   exact standalone scheduling.

## Known Caveats

- The seed body ships in English; the translation offer in the first meeting
  covers it. Do not apologize for it in the demo — let the flow handle it.
- Local checks and check-ins require the guest's computer and desktop app to
  be running; say so when automations come up.

## Fallback Plan

- Marketplace add fails → verify the guest is on the `stable` ref and the
  repository is reachable; fall back to demonstrating on the host machine in a
  sandbox directory (`bootstrap_manager.py --manager-dir <sandbox>`).
- Bootstrap or Doctor fails → capture the JSON output, stop the technical
  path, and continue the conversation on the guest's real work instead; the
  failure is acceptance-test evidence, not a demo emergency.

## After The Session

Record observed friction against the acceptance matrix rows, then route
durable findings into the wirenet-manager Project Pack. No client claims from
a single demo; the guest is feedback, not a case study.
