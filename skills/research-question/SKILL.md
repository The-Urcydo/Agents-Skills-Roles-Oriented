---
name: research-question
description: "Answer a question with verified sources, confidence, and gaps, without deciding for the caller. Use when a plan or decision depends on facts that are missing or uncertain."
license: MIT
compatibility: "Requires access to the repository and, when the question is external, the web."
metadata:
  category: productivity
  invocation: both
---
# Research a question

Use this when a caller needs facts before deciding. You reduce uncertainty; you do not decide and you do not take over the caller's work item.

## Steps

1. Restate the question in one sentence and confirm it with the caller. A vague question produces a vague answer.
2. Check what the repository already says: the docs index, decisions, prior research, and the code. Do not ask the web what the repository already answers.
3. Gather sources. Prefer primary and current ones. Record each claim with its source and date.
4. Mark anything inferred as an assumption, and say what would confirm or refute it.
5. Write the answer first, then the evidence, then the gaps and the confidence. A reader who reads only the first paragraph gets the answer.
6. Reply to the caller in at most five lines: where the note is, the answer, the confidence, and the gaps that matter.
7. Leave the caller's work item, status, and next action untouched.

## Verify

- The question is restated in the note.
- The answer is in the first paragraph.
- Every claim has a source or is marked as an assumption.
- The gaps and the confidence are explicit.
- The caller's item is unchanged.

## In Repo-Template

- Create `research.md` with `python3 tools/item_file.py <id> research`.
- Do not run `python3 tools/transition.py`; the caller keeps the item.
- Raw notes go in `work/research/`.
- If a finding must outlive the item, say so; the caller records it and a separate docs change promotes it.

## Stop and ask

- The sources disagree on something that changes the decision.
- The answer needs access you do not have.
- The question is actually a decision; hand it back to the caller.
- The answer would expose a secret or personal data.
