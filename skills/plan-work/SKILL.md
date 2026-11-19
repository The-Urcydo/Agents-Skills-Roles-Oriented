---
name: plan-work
description: "Turn a brief or request into an ordered plan with risks, sequencing, tasks, and verification. Use when the work is larger than a few steps or the brief needs decomposition before building."
license: MIT
metadata:
  category: productivity
  invocation: both
---
# Plan work

Use this when the work is too large for one session or the brief needs decomposition before anyone builds. A small task with a clear brief does not need a separate plan; `new-work-item` is enough.

## Steps

1. Read the brief, issue, or request and its acceptance criteria. If the goal is ambiguous, the scope is unbounded, or a criterion is missing, stop and ask instead of planning around the gap.
2. Restate the goal and the acceptance criteria in your own words. List the constraints, decisions already made, and out of scope.
3. Check what the repository already says: the docs index, decision records, and prior work. Do not plan a duplicate.
4. Choose the approach. Name the files, components, or interfaces involved. If a design decision is needed before building, hand it to the decision owner or record it first.
5. List the risks and unknowns with a likelihood and a mitigation. Include what would make the plan wrong.
6. Sequence the work: what must happen first, what can run in parallel, and what must wait for a merge.
7. Write ordered tasks. Each task should be small enough for one session and end with a check the agent doing the work can run. When a task goes to another agent or session, write its context pack with `write-task-context`.
8. Define how the plan will be tested: the commands, the observable behavior, and the evidence the verifier will need.
9. Record the plan in the host's tracker or in a plan document next to the item, and link it from the handoff. If the host has a plan template, use it.
10. Hand off the plan to the agent doing the work. Do not start building; the plan is the planning artifact.

## Verify

- The plan names the goal and every acceptance criterion.
- Each risk has a mitigation; each unknown has a way to resolve it.
- Every task is small enough for one session and has a verification step.
- The sequence names dependencies and what can run in parallel.
- The out-of-scope is explicit.
- The handoff links the plan and names the first action.

## Stop and ask

- The brief or acceptance criteria are missing, ambiguous, or contradictory.
- The plan needs a decision the human must make, such as spend, production access, or a reversal of an accepted decision.
- The scope cannot be bounded without inventing a requirement.
- A task needs a security review that has not been decided.
- The plan would change an accepted decision; propose a superseding record first.

The plan and task templates are in [references/plan-template.md](references/plan-template.md).
