---
name: write-handoff
description: "Update a handoff record so a fresh session or another agent can continue without the old context. Use before stopping work, switching roles, or changing a work item's state."
license: MIT
compatibility: "Works with any tracker that keeps a handoff note; a single Markdown file is enough."
metadata:
  category: productivity
  invocation: both
---
# Write a handoff

Use this when work will continue in another session, another role, or after a pause. The next session has no memory; the handoff is the memory.

## Steps

1. Open the handoff record the tracker uses. If there is none, create one next to the work item or in the branch's pull request description.
2. Write for a reader who has the repository but not your conversation:
   - **Current state:** one paragraph on where things stand now.
   - **Decisions made:** choices that must not be re-litigated, with a link to the decision record when there is one.
   - **Dead ends already tried:** what failed and why, so nobody repeats it.
   - **Next action:** one sentence naming the next owner and the first thing they do.
   - **Evidence:** the commands run and their result, or a link to the run.
   - **Docs for the scribe:** `none, behavior unchanged.` when no behavior changed and no doc describes what was touched; otherwise the docs and changelog the change needs. The agent that produced the work writes this line; later roles read it and never rewrite it.
3. Add a **do not** list for anything the next agent must avoid: files, assumptions, or approaches.
4. Keep it short. Aim for under 60 lines; it is current state, not a diary. History lives in git.
5. If the tracker has a state transition, use its tool instead of editing the state by hand.
6. Verify the handoff answers: where are we, what is decided, what failed, what next, and what must not happen.

## Verify

- A reader can name the next action without opening the old conversation.
- Every claim has evidence or a file path.
- The state in the tracker matches the state in the handoff.
- The **do not** list is current.
- The docs-for-the-scribe line is present, or the host's equivalent is recorded.

## In Repo-Template

The handoff is `work/items/<id>/handoff.md`, or `work/items/<id>.md` for a light item. Move the item with:

```bash
python3 tools/transition.py <id> <status> --by <role> --next "<one sentence>" [--owner <role>] [--evidence "<command or link>"]
```

`in-review`, `verified`, and `done` require evidence. Do not edit `status` by hand.

## Stop and ask

- The state change is not allowed by the tracker's rules.
- You cannot show evidence for a claim the next agent needs.
- The next action depends on a decision the human has not made.
- The handoff would contain a secret or a personal path.
