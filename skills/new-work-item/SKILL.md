---
name: new-work-item
description: "Create and scope a work item in the repository's tracker, with testable acceptance criteria and an explicit out-of-scope. Use when a request needs tracking, a brief, or a plan before work starts."
license: MIT
compatibility: "Works with a file-based work tracker such as work/items/ or an issue tracker such as GitHub Issues."
metadata:
  category: repo
  invocation: both
---
# New work item

Use this when a request should become tracked work: a feature, a bug, a refactor, or a research task. The output is one item with a goal, observable acceptance criteria, constraints, and out of scope.

A one-off change with no follow-up does not need an item. A decision that needs the human does not become an item; ask the human instead.

## Steps

1. Find the tracker. Look for `work/items/`, an issue template, or the repository's contribution guide. Use the tracker the repository already has; do not invent a second one.
2. Choose the form:
   - **Light:** under about an hour, one file or one issue, no design questions.
   - **Full:** needs a brief, a plan, or a review artifact.
3. Capture the request in the requester's words, then write:
   - **Goal:** one sentence on the outcome.
   - **Why now:** the problem or trigger.
   - **Acceptance criteria:** each one observable and checkable by someone who was not in the room. Prefer a command, a file, or a behavior over an adjective.
   - **Constraints:** time, compatibility, files, or decisions already made.
   - **Out of scope:** what this item will not do.
4. Link the related docs, decisions, and prior items. Check the index and the decision records before writing; do not duplicate an existing item.
5. Set the first action: who acts next and what they do first. If the request is ambiguous, stop and ask instead of choosing a reading.
6. Verify the item exists in the tracker, the criteria are checkable, and the next action names one owner.

## Verify

- The item has a goal, at least one acceptance criterion, and an explicit out-of-scope.
- Every criterion can be checked without asking the requester.
- The item is visible in the tracker's active list.
- No second tracker was created.

## In Repo-Template

Repo-Template keeps items in `work/items/`:

```bash
python3 tools/new_item.py <slug> --title "Human readable title"           # full item
python3 tools/new_item.py <slug> --title "Human readable title" --light   # one file
python3 tools/transition.py <id> planned --by <role> --next "<first action>"
```

The tool prints the path to `handoff.md` (or the single file). Do not invent the id; the tool allocates it.

## Stop and ask

- The request has two plausible readings, or the scope is unbounded.
- The work needs a decision the human must make, not a work item.
- The repository has no tracker and the user has not chosen one.
- The item would duplicate an existing item; improve that one instead.
