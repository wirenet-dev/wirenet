---
name: loop
description: Create, inspect, update, pause, resume, or stop a recurring heartbeat automation in the current Codex task. Use when the user explicitly invokes $loop or asks this task to keep checking, try again later, follow up, monitor changing state, retry on a cadence, or continue until a clear condition is met. Do not use when the work can be completed immediately without waiting.
---

# Loop

Turn a plain-language request into one quiet recurring automation attached to
the current task. Keep the automation self-contained and stop it cleanly when
its purpose is complete.

## Create A Loop

1. Infer the concrete task, useful cadence, completion condition, and
   notification threshold from the request and current conversation.
2. Continue immediately instead when no passage of time or external state
   change is needed.
3. Use the requested cadence when sensible. Otherwise choose one that matches
   the source's plausible change rate, urgency, cost, and noise risk. Ask one
   concise question only when cadence or completion would materially change the
   behavior.
4. Write a self-contained automation prompt that preserves:
   - the exact work and approved scope;
   - the evidence to inspect;
   - the completion or stop condition;
   - when to notify and when to stay quiet;
   - all existing safety and approval boundaries.
5. Find and use the available automation tool. Create one active heartbeat on
   the current task; do not create a new task, detached cron job, or duplicate
   matching automation.
6. After creation succeeds, rename the current task to `loop: <short task>`
   when a task-title tool is available.
7. Report only the loop name, cadence, purpose, and completion condition.

## Run A Heartbeat

On each heartbeat, do the scoped work before deciding whether to notify.

- If meaningful state changed but the completion condition is not met, report
  only the useful delta and smallest next action.
- If nothing useful changed, use the runtime's quiet heartbeat response.
- If the completion condition is verified, report the result, delete the active
  automation, and rename the task to `done: <short task>` when possible.
- Do not mark the loop done after a failed run, temporary retry, missing source,
  or unchanged external state.

## Manage A Loop

For inspect, cadence changes, prompt changes, pause, resume, or deletion, resolve
the existing automation and use the matching automation-tool operation. Preserve
fields the user did not ask to change. Prefer updating an existing matching
loop over creating another one.

Restore the `loop:` title when resuming. Delete the automation when the user says
the task is obsolete or asks to stop it.

## Boundaries

- A loop changes timing, not authorization. It must not send messages, change
  meetings, edit shared documents, spend money, publish, or perform another
  external action without the approval that action already requires.
- Do not broaden the monitored scope merely because the loop repeats.
- Explain plainly when the runtime cannot create automations. Never substitute
  raw scheduler syntax or claim background execution succeeded.
- Local heartbeats require the relevant Codex runtime and computer to be
  available.
