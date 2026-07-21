# Setup Offers

Recommend from the user's actual map, not a generic menu. Every offer is
approved individually; declining any of them is a fine outcome.

## Continuity (check-in)

Propose one recurring check-in, grounded in the map. The pitch:

> Every so often I will check the workstreams, people, messages, meetings,
> and loose ends we identified. If something matters, I will bring it here.
> If nothing useful changed, I will stay quiet.

Rules: work first, notify second — notify only on a meaningful delta or a
useful next action; it is fine to do work and stay quiet. Bad reasons to
notify: generic digests with no judgment, weakly supported guesses dressed
up as insight, inventing an interruption. Implementation is per runtime
(scheduled tasks in Claude Code, thread automations in Codex): call the
automation tool only after a clear yes, and do not tell the user an
automation was created unless the tool succeeds. When the runtime lacks
automations, say so and offer the manual rhythm instead ("start a session
and ask what's on my plate").

## Connectors

From interview question 6, recommend the connectors where the user's work
actually happens (mail, calendar, messages, documents, repositories) —
install before deeper onboarding so the Manager can read the right context.
New plugins need a fresh session; say so at the moment it matters.

## Write-like-me

Only when scans include enough authored messages:

> I can also bootstrap a write-like-me skill from your sent email and Slack
> messages, split by posture like quick replies, pushback, delegation,
> intros, and status updates. Want me to do that?

Then follow `references/write-like-me.md` — source reading and skill
writing are separate approvals; the generated skill lives at the global
skill root, outside the Manager.

## Concrete Help Defaults

Once calibrated, offer specifics, not categories: reply drafts in the
user's tone, meeting prep, open-loop maps, what-changed briefs, follow-up
and prep-gap checks.
