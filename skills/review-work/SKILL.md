---
name: review-work
description: "Independently verify that finished work meets its acceptance criteria and the repository's rules, with evidence for every claim. Use when a change is ready for review and you did not build it."
license: MIT
compatibility: "Requires git and the repository's test commands."
metadata:
  category: engineering
  invocation: both
---
# Review work

Use this when work is ready for an independent check. The review is a different mind from the build; that is the point. If you built the change, stop and hand it to someone else.

## Steps

1. Read the brief, issue, or acceptance criteria first, then the handoff, then the diff. Do not start from the author's summary.
2. Run the repository's checks and tests yourself. Do not trust pasted output.
3. Check each acceptance criterion and record the evidence: the command, the output, the file, or the link. "Looks right" is not evidence.
4. Check the rules: decisions respected, ownership respected, generated files in sync, docs updated when behavior changed.
5. Look for what the criteria do not cover: unintended files, half-finished sections, leftover placeholders, secrets, unintended deletions, tests that pass for the wrong reason.
6. Rank findings by severity using [references/severity.md](references/severity.md). Each finding states what, where, why it matters, and a recommended fix.
7. Write the verdict:
   - **approve:** all criteria met, no blocker or major finding;
   - **changes requested:** fix the findings and re-review;
   - **reject:** the approach is wrong; re-plan or drop it.
8. Hand the review back through the tracker's state transition. Do not fix the findings yourself.

## Verify

- The review names the exact commit or diff it checked.
- Every acceptance criterion has evidence.
- The checks were run by the agent doing the review, not copied.
- Findings are ranked and actionable.
- The verdict matches the findings.

## In Repo-Template

- Write `review.md` with `python3 tools/item_file.py <id> review`.
- Move an approved item with `python3 tools/transition.py <id> verified --by <role> --evidence "<what you ran>" --next "..."`.
- Move a changes-requested item back to `in-progress` with the role that built it as owner.
- Detail: `agents/protocols/review.md`.

## Stop and ask

- You built the change; you are not independent.
- The acceptance criteria are missing or wrong.
- You find a security, data-loss, or irreversible problem.
- The diff changes files the brief did not mention and the change is not explained.
